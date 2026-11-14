"""R8: same-mode monsoon water series and HH/HV medians in explicit zones.

Writes timeline.csv (R8 zone medians), a compatibility alias zone_timeline.csv,
and water_timeline.csv (supplementary water series).
Incompatible acquisitions are excluded and listed in timeline_status.json.
"""
from __future__ import annotations
import csv
import numpy as np
from . import ancillary, zones
from . import common as K
from . import config as C
from . import nisar_io as io

ZONE_COLUMNS = ["zone_id", "zone_name", "review_status", "date", "polarization",
                "median_db", "valid_pixels", "zone_pixels", "granule_id"]
WATER_COLUMNS = ["date", "mode", "pol", "same_mode_as_primary", "threshold_db",
                 "classification_usable", "valid_fraction", "water_km2", "water_outside_permanent_flat_km2", "granule_id"]


def write_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(write=True):
    primary = C.parse_granule_id(C.PRIMARY["before"])
    aux = ancillary.load()
    occ, slope = aux["jrc_occurrence"], aux["slope"]
    perm = np.isfinite(occ) & (occ >= C.PERMANENT_WATER_OCCURRENCE)
    flat = np.isfinite(slope) & (slope <= C.FLOOD_MAX_SLOPE_DEG)
    rows, zone_rows, excluded = [], [], []
    footprints = list(zones.masks())
    reference_hh = K.lee_db(io.load_db(C.CROPS / f"{io.crop_name(C.PRIMARY['after'])}_HH.tif"))
    t, _ = K.water_threshold(reference_hh)
    for m in K.gcov_crops():
        if any(m[k] != primary[k] for k in ("track", "mode", "pol", "direction", "frame")):
            excluded.append({"granule_id": m["granule_id"], "reason": "incompatible acquisition"})
            continue
        if not C.IS_DEMO and not m.get("quality_rule"):
            excluded.append({"granule_id": m["granule_id"], "reason": "native quality check pending"})
            continue
        hh = K.lee_db(io.load_db(C.CROPS / f"{m['name']}_HH.tif"))
        valid = np.isfinite(hh) & np.isfinite(occ) & np.isfinite(slope)
        water = valid & (hh < t)
        extra = K.clean(water & ~perm & flat)
        rows.append({"date": m["date"], "mode": m["mode"], "pol": m["pol"], "same_mode_as_primary": True,
                     "classification_usable": bool(valid.any() and water.sum() / valid.sum() < C.WATER_MAX_DARK_FRACTION),
                     "threshold_db": round(t, 2), "valid_fraction": round(float(valid.mean()), 3),
                     "water_km2": round(float(water.sum() * K.PIXEL_KM2), 2),
                     "water_outside_permanent_flat_km2": round(float(extra.sum() * K.PIXEL_KM2), 2),
                     "granule_id": m["granule_id"]})
        for pol in ("HH", "HV"):
            path = C.CROPS / f"{m['name']}_{pol}.tif"
            values = hh if pol == "HH" else K.lee_db(io.load_db(path)) if path.exists() else None
            for props, mask in footprints:
                samples = values[mask & np.isfinite(values)] if values is not None else np.array([])
                zone_rows.append({"zone_id": props["id"], "zone_name": props["name"],
                                  "review_status": props.get("review_status", "not reviewed"),
                                  "date": m["date"], "polarization": pol,
                                  "median_db": float(np.median(samples)) if samples.size else None,
                                  "valid_pixels": int(samples.size), "zone_pixels": int(mask.sum()),
                                  "granule_id": m["granule_id"]})
    if write:
        write_csv(C.DERIVED / "water_timeline.csv", WATER_COLUMNS, rows)
        write_csv(C.DERIVED / "timeline.csv", ZONE_COLUMNS, zone_rows)
        write_csv(C.DERIVED / "zone_timeline.csv", ZONE_COLUMNS, zone_rows)
        K.write_json(C.DERIVED / "timeline_status.json", {"dates": [r["date"] for r in rows],
                     "excluded": excluded, "requested_dates": C.TIMELINE_DATES,
                     "missing_dates": sorted(set(C.TIMELINE_DATES) - {r["date"] for r in rows})})
    return rows


if __name__ == "__main__":
    for row in run():
        print(row)
