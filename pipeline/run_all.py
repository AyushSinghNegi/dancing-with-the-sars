"""Run the whole science pipeline on whatever crops exist, and write the app's inputs.

  python -m pipeline.run_all                     # real crops in data/crops -> data/derived
  MONSOONLENS_DEMO=1 python -m pipeline.run_all --synthetic   # synthetic, into data/demo only

Order: water (R5) -> slide zones (R6) -> validation (R9) -> second-track and elevation-map checks ->
threshold sensitivity -> evidence chips and field list ->
timeline (R8) ->
render overlays -> terrain3d (3D model files) -> flood chance level, what is near each zone, one radar image per
pass (own files: flood_baseline.json, nearby.json, pass_images.json) -> bounds.json + metrics.json (provenance for
every number).
"""
from __future__ import annotations

import argparse
import platform
import time

from . import common as K
from . import config as C
from . import nisar_io as io
from . import crosstrack, dem_check, evidence, render, sensitivity, slide_zones, terrain3d, timeline, validate, water

VERSION = "0.6.0"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true", help="build synthetic NISAR-format inputs first (demo only)")
    a = ap.parse_args(argv)
    t0 = time.time()
    if a.synthetic:
        assert C.IS_DEMO, "Synthetic data only runs with MONSOONLENS_DEMO=1"
        from . import crop, synthetic
        synthetic.build()
        crop.main(["--primary"])
    names = {m["name"] for m in K.manifest()}
    need = {io.crop_name(C.PRIMARY["before"]), io.crop_name(C.PRIMARY["after"])}
    if not need <= names:
        raise SystemExit(f"Missing crops {sorted(need - names)} in {C.CROPS}. Run: python -m pipeline.crop --primary")

    print("[run] water", flush=True)
    wstats, layers = water.run()
    print("[run] slide zones", flush=True)
    sz, _ = slide_zones.run(layers)
    print("[run] place names (OpenStreetMap)", flush=True)
    try:
        from . import places
        places.run()
    except Exception as e:  # names are a convenience; never block the science
        print(f"      skipped: {e}")
    print("[run] validation", flush=True)
    vsum, _ = validate.run()
    print("[run] second-track check (track 106)", flush=True)
    xt = crosstrack.run()
    print("[run] elevation-map check (NASADEM)", flush=True)
    dc = dem_check.run()
    print("[run] water-threshold sensitivity (+/- 1 dB)", flush=True)
    sens = sensitivity.run()
    print("[run] evidence chips and field check list", flush=True)
    ev = evidence.run()
    print("[run] timeline", flush=True)
    tl = timeline.run()
    print("[run] render", flush=True)
    rend = render.run()
    terr = None
    if (C.AUX / "aux_elevation.tif").exists():
        print("[run] terrain3d", flush=True)
        terr = terrain3d.run()
    # Add-ons with their own output files. They read what the steps above wrote, and never block the science.
    for label, mod in (("chance level for the flood matches", "flood_baseline"),
                       ("roads, railways and settlements near each zone (OpenStreetMap)", "nearby"),
                       ("one radar image per same-mode pass", "pass_images")):
        print(f"[run] {label}", flush=True)
        try:
            __import__(f"{__package__}.{mod}", fromlist=["run"]).run()
        except Exception as e:
            print(f"      skipped: {e}")

    man = {m["name"]: m for m in K.manifest()}
    sources = []
    for key in ("before", "after", "pair"):
        gid = C.PRIMARY[key]
        m = man.get(io.crop_name(gid))
        if m:
            sources.append({"role": key, "granule_id": gid, "valid_fraction": m["valid_fraction"],
                            "native_spacing_m": m.get("source_spacing_m"), "multilook": m.get("multilook"),
                            "url": C.find(gid).url})
    for key in ("before", "after", "pair") if xt else ():
        gid = C.CROSSCHECK[key]
        m = man.get(io.crop_name(gid))
        if m:
            sources.append({"role": f"check_{key}", "granule_id": gid, "valid_fraction": m["valid_fraction"],
                            "native_spacing_m": m.get("source_spacing_m"), "multilook": m.get("multilook"),
                            "url": C.find(gid).url})
    meta = {
        "demo": C.IS_DEMO,
        "demo_note": "SYNTHETIC radar values for development; not NISAR data" if C.IS_DEMO else None,
        "generated": K.now_iso(), "pipeline_version": VERSION, "python": platform.python_version(),
        "aoi": C.AOI, "grid": {"epsg": C.GRID_EPSG, "res_m": C.GRID_RES},
        "thresholds": {"water_db_bounds": C.WATER_DB_BOUNDS, "water_train_occurrence": C.WATER_TRAIN_OCCURRENCE,
                       "change_db": C.CHANGE_DB,
                       "permanent_water_occurrence": C.PERMANENT_WATER_OCCURRENCE,
                       "flood_max_slope_deg": C.FLOOD_MAX_SLOPE_DEG, "slide_min_slope_deg": C.SLIDE_MIN_SLOPE_DEG,
                       "slide_max_slope_deg": C.SLIDE_MAX_SLOPE_DEG, "slide_hh_rise_db": C.SLIDE_HH_RISE_DB,
                       "slide_hv_drop_db": C.SLIDE_HV_DROP_DB,
                       "slide_normalise_scene_shift": C.SLIDE_NORMALISE_SCENE_SHIFT,
                       "coherence_low": C.COHERENCE_LOW, "min_patch_pixels": C.MIN_PATCH_PIXELS},
        "sources": sources,
        "water": wstats, "slides": sz, "validation": vsum, "timeline_dates": len(tl),
        "crosstrack": None if not xt else {k: xt[k] for k in ("pair", "status_counts", "status_by_confidence",
                                                              "real", "chance", "lift_confirmed", "p_value", "buffer_m",
                                                              "zones_track106", "valid_fraction",
                                                              "scene_shift_db", "water_reliable")},
        "dem_check": None if not dc else {k: v for k, v in dc.items() if k != "generated"},
        "sensitivity": sens, "evidence": ev,
        **rend,
    }
    K.write_json(C.DERIVED / "bounds.json", {"bounds_latlon": rend["bounds_latlon"], "demo": C.IS_DEMO,
                                             "overlays": rend["overlays"], **({"terrain": terr} if terr else {})})
    K.write_json(C.DERIVED / "metrics.json", meta)
    print(f"[run] done in {time.time() - t0:.0f}s -> {C.DERIVED}")
    print(f"      new water {wstats['new_water_km2']:.1f} km2 | slide zones {sz['zones']} "
          f"({sz['high']} high) | validation {vsum}")


if __name__ == "__main__":
    main()
