"""Run the whole science pipeline on whatever crops exist, and write the app's inputs.

  python -m pipeline.run_all                     # real crops in data/crops -> data/derived
  MONSOONLENS_DEMO=1 python -m pipeline.run_all --synthetic   # synthetic, into data/demo only

Order: water (R5) -> slide zones (R6) -> validation (R9) -> timeline (R8) ->
render overlays -> bounds.json + metrics.json (provenance for every number).
"""
from __future__ import annotations

import argparse
import platform
import shutil
from importlib.metadata import version
import time

from . import common as K
from . import config as C
from . import nisar_io as io
from . import render, slide_zones, timeline, validate, water, control, preflight

VERSION = "0.5.0"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true", help="build synthetic NISAR-format inputs first (demo only)")
    a = ap.parse_args(argv)
    t0 = time.time()
    if a.synthetic:
        if not C.IS_DEMO:
            raise SystemExit("Synthetic data only runs with MONSOONLENS_DEMO=1")
        from . import crop, synthetic
        synthetic.build()
        crop.main(["--primary"])
    readiness = preflight.report()
    if not readiness["ready_to_process"]:
        raise SystemExit("Inputs not ready: missing crops=" + str(readiness["missing_crops"]) +
                         "; quality checks pending=" + str(readiness["quality_pending"]) +
                         ". Run python -m pipeline.acquire --primary first.")
    names = {m["name"] for m in K.manifest()}
    need = {io.crop_name(C.PRIMARY["before"]), io.crop_name(C.PRIMARY["after"])}
    if not need <= names:
        raise SystemExit(f"Missing crops {sorted(need - names)} in {C.CROPS}. Run: python -m pipeline.crop --primary")

    print("[run] water", flush=True)
    wstats, layers = water.run()
    print("[run] slide zones", flush=True)
    sz, slide_mask = slide_zones.run(layers)
    controls = control.run(layers, slide_mask, K.load_pair()["coherence"])
    print("[run] validation", flush=True)
    vsum, _ = validate.run(water_usable=bool(wstats["classification_usable"]))
    print("[run] timeline", flush=True)
    tl = timeline.run()
    print("[run] render", flush=True)
    rend = render.run()

    man = {m["name"]: m for m in K.manifest()}
    sources = []
    for key in ("before", "after", "pair"):
        gid = C.PRIMARY[key]
        m = man.get(io.crop_name(gid))
        if m:
            sources.append({"role": key, "granule_id": gid, "valid_fraction": m["valid_fraction"],
                            "native_spacing_m": m.get("source_spacing_m"), "multilook": m.get("multilook"),
                            "quality_rule": m.get("quality_rule"),
                            "url": C.find(gid).url})
    # Publish reviewed reference inputs with the same run so the app only reads derived/.
    for name in ("rainfall.csv", "zones.geojson", "event_source_review.csv", "zone_landcover_review.json"):
        source = C.REFERENCE / name
        if source.exists():
            shutil.copy2(source, C.DERIVED / name)
    shutil.copy2(validate.events_path(), C.DERIVED / "events.geojson")
    meta = {
        "demo": C.IS_DEMO,
        "demo_note": "SYNTHETIC radar values for development; not NISAR data" if C.IS_DEMO else None,
        "generated": K.now_iso(), "pipeline_version": VERSION, "python": platform.python_version(),
        "aoi": C.AOI, "grid": {"epsg": C.GRID_EPSG, "res_m": C.GRID_RES},
        "thresholds": {"water_method": "otsu-linear-power-shared-after-date",
                       "water_threshold_linear": 10 ** (wstats["threshold_after_db"] / 10),
                       "water_threshold_db": wstats["threshold_after_db"],
                       "dem": "NASADEM_HGT.001", "validation_radius_m": C.VALIDATION_RADIUS_M,
                       "slide_min_patch_pixels": C.SLIDE_MIN_PATCH_PIXELS,
                       "water_max_dark_fraction": C.WATER_MAX_DARK_FRACTION, "change_db": C.CHANGE_DB,
                       "permanent_water_occurrence": C.PERMANENT_WATER_OCCURRENCE,
                       "flood_max_slope_deg": C.FLOOD_MAX_SLOPE_DEG, "slide_min_slope_deg": C.SLIDE_MIN_SLOPE_DEG,
                       "coherence_low": C.COHERENCE_LOW, "min_patch_pixels": C.MIN_PATCH_PIXELS},
        "sources": sources,
        "water": wstats, "slides": sz, "validation": vsum, "timeline_dates": len(tl),
        "controls": controls,
        "library_versions": {name: version(name) for name in
                             ("numpy", "scipy", "h5py", "rasterio", "pyproj", "shapely", "scikit-image",
                              "earthaccess", "xarray", "rioxarray", "geopandas", "matplotlib")},
        **rend,
    }
    K.write_json(C.DERIVED / "bounds.json", {"bounds_latlon": rend["bounds_latlon"], "demo": C.IS_DEMO,
                                             "overlays": rend["overlays"]})
    K.write_json(C.DERIVED / "metrics.json", meta)
    print(f"[run] done in {time.time() - t0:.0f}s -> {C.DERIVED}")
    print(f"      new water {wstats['new_water_km2']:.1f} km2 | slide zones {sz['zones']} "
          f"({sz['high']} high) | validation {vsum}")


if __name__ == "__main__":
    main()
