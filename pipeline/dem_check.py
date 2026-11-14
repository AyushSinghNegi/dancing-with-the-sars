"""Elevation-map check: do the slide zones depend on which elevation map we use?

The slide rule needs slope (15-45 degrees) and slope direction (to drop radar layover and shadow).
Both come from an elevation map. The main run uses the Copernicus GLO-30 DEM. This check runs the
same rule, on the same radar pair, with NASA's NASADEM instead (put on our 40 m grid by RSN), and
records:

  * how close the two slope maps are (median difference, agreement on the 15-45 degree band)
  * for every zone: found again with NASADEM (within 80 m, as in the second-track check), or not,
    and why not (slope over 45 or under 15 degrees in NASADEM, or radar layover/shadow there)
  * how many zones NASADEM finds that the main run does not
  * whether the reported-landslide matches still hold

The main results do not change. Writes data/derived/dem_check.json and adds "nasadem" to each zone in
slide_zones.geojson.

  python -m pipeline.dem_check
"""
from __future__ import annotations

import csv
import json

import numpy as np
import rasterio
from scipy import ndimage as ndi

from . import ancillary
from . import common as K
from . import config as C
from . import slide_zones, validate

NASADEM = C.AUX / "aux_nasadem_elevation.tif"
NEAR_PX = C.CROSS_BUFFER_PX   # 80 m, the same allowance as the second-track check
REASONS = ("steeper than 45° in NASADEM", "gentler than 15° in NASADEM", "radar layover or shadow in NASADEM",
           "near the edge of the slope band in NASADEM")


def available() -> bool:
    return NASADEM.exists() and K.load_layer("slide_zone_ids") is not None


def load_nasadem():
    with rasterio.open(NASADEM) as d:
        elev = d.read(1).astype(np.float32)
        elev[elev == d.nodata] = np.nan
        source = d.tags().get("source", "NASADEM_HGT.001")
    # Same steps as the main elevation layer: slope from 40 m central differences, stored as whole degrees.
    slope = np.round(ancillary.slope_degrees(elev))
    return elev, slope, source


def _why(mask, slope_n, geom_bad_n):
    s = float(np.nanmean(slope_n[mask]))
    if s > C.SLIDE_MAX_SLOPE_DEG:
        return REASONS[0]
    if s < C.SLIDE_MIN_SLOPE_DEG:
        return REASONS[1]
    if geom_bad_n[mask].any():
        return REASONS[2]
    return REASONS[3]


def run(write=True):
    if not available():
        (C.DERIVED / "dem_check.json").unlink(missing_ok=True)   # never leave a stale check behind
        print("      NASADEM layer not found; skipping")
        return None
    layers = {k: K.load_layer(k) for k in ("hh_before", "hh_after", "hv_before", "hv_after",
                                             "water_after", "permanent", "valid")}
    coh = K.load_pair()["coherence"]
    aux = ancillary.load()
    elev_n, slope_n, source = load_nasadem()
    alt = slide_zones.detect(layers, coh, dict(aux, slope=slope_n, elevation=elev_n))
    ids = K.load_layer("slide_zone_ids").astype(np.int64)
    n = int(ids.max())

    # How close are the two slope maps, where we have radar data?
    ok = layers["valid"] & np.isfinite(aux["slope"]) & np.isfinite(slope_n)
    s_c, s_n = aux["slope"][ok], slope_n[ok]
    band_c = (s_c >= C.SLIDE_MIN_SLOPE_DEG) & (s_c <= C.SLIDE_MAX_SLOPE_DEG)
    band_n = (s_n >= C.SLIDE_MIN_SLOPE_DEG) & (s_n <= C.SLIDE_MAX_SLOPE_DEG)

    # Zone by zone
    buf = np.ones((2 * NEAR_PX + 1,) * 2, bool)
    near_alt = ndi.binary_dilation(alt["zones"], buf)
    found = np.bincount(ids.ravel(), weights=near_alt.ravel(), minlength=n + 1)[1:] > 0
    gj_path = C.DERIVED / "slide_zones.geojson"
    gj = json.loads(gj_path.read_text())
    reasons, by_conf = {}, {}
    for f in gj["features"]:
        p = f["properties"]
        i = int(p["id"][2:])
        bc = by_conf.setdefault(p["confidence"], {"found": 0, "zones": 0})
        bc["zones"] += 1
        if found[i - 1]:
            p["nasadem"] = "found"
            bc["found"] += 1
            p.pop("nasadem_reason", None)
        else:
            p["nasadem"] = "not found"
            p["nasadem_reason"] = _why(ids == i, slope_n, alt["geom_bad"])
            reasons[p["nasadem_reason"]] = reasons.get(p["nasadem_reason"], 0) + 1
    both_checks = sum(f["properties"].get("nasadem") == "found" and f["properties"].get("track106") == "confirmed"
                      for f in gj["features"])

    lab_alt, n_alt = ndi.label(alt["zones"], structure=np.ones((3, 3)))
    near_main = ndi.binary_dilation(ids > 0, buf)
    new_alt = int(sum(1 for j in range(1, n_alt + 1) if not near_main[lab_alt == j].any()))

    # Reported landslides: the same scoring as validate.run, once more with the NASADEM zones
    d_alt = validate._dist_m(alt["zones"])
    dist_main, nearest = ndi.distance_transform_edt(ids == 0, return_indices=True)
    slides = []
    with open(C.DERIVED / "validation.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["type"] not in validate.SLIDE_TYPES or row["observable"] != "yes":
                continue
            r, c, _ = K.lonlat_to_rowcol(float(row["lon"]), float(row["lat"]))
            radius = max(float(row["precision_m"]), validate.RADIUS["slide"])
            zid = int(ids[nearest[0][r, c], nearest[1][r, c]])
            slides.append({"id": row["id"], "place": row["place"], "main": row["result"],
                           "main_nearest_zone": f"SZ{zid:03d}",
                           "main_distance_m": int(round(float(dist_main[r, c]) * C.GRID_RES)),
                           "nasadem": "hit" if d_alt[r, c] <= radius else "miss",
                           "nasadem_distance_m": int(round(float(d_alt[r, c]))) if np.isfinite(d_alt[r, c]) else None})
    hit_zones = sorted({s["main_nearest_zone"] for s in slides if s["main"] == "hit"})

    out = {
        "generated": K.now_iso(),
        "main_dem": ancillary.SOURCES["dem"],
        "check_dem": source,
        "check_dem_url": "https://doi.org/10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001",
        "buffer_m": NEAR_PX * C.GRID_RES,
        "slope": {
            "median_abs_diff_deg": round(float(np.median(np.abs(s_c - s_n))), 1),
            "correlation": round(float(np.corrcoef(s_c, s_n)[0, 1]), 3),
            "band_agreement": round(float((band_c == band_n)[band_c | band_n].mean()), 3),
            "band_share_main": round(float(band_c.mean()), 3),
            "band_share_nasadem": round(float(band_n.mean()), 3),
        },
        "zones_main": n,
        "zones_nasadem": int(n_alt),
        "found": int(found.sum()),
        "not_found": int(n - found.sum()),
        "not_found_reasons": dict(sorted(reasons.items(), key=lambda kv: -kv[1])),
        "by_confidence": dict(sorted(by_conf.items(), key=lambda kv: ["high", "medium", "low"].index(kv[0]))),
        "new_in_nasadem": new_alt,
        "found_and_second_track": int(both_checks),
        "reported_slides": slides,
        "reported_slide_hits": {"main": sum(s["main"] == "hit" for s in slides),
                                "nasadem": sum(s["nasadem"] == "hit" for s in slides),
                                "scored": len(slides), "main_hit_zones": hit_zones},
    }
    if write:
        K.write_json(gj_path, gj)
        K.write_json(C.DERIVED / "dem_check.json", out)
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=1, ensure_ascii=False))
