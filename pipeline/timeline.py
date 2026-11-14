"""Water area through the monsoon, one value per radar date (R8).

Uses every GCOV crop on the primary track. The water threshold is set per
date with the same method as the flood map (Kittler-Illingworth trained on JRC reservoir cores). Dates taken in a
different radar mode or polarisation are kept but flagged, because their
brightness is not directly comparable.

  python -m pipeline.timeline
Writes data/derived/timeline.csv.
"""
from __future__ import annotations

import csv

import numpy as np

from . import ancillary
from . import common as K
from . import config as C
from . import nisar_io as io


def run(write=True):
    primary = C.parse_granule_id(C.PRIMARY["before"])
    aux = ancillary.load()
    perm = np.nan_to_num(aux["jrc_occurrence"]) >= C.PERMANENT_WATER_OCCURRENCE
    flat = np.nan_to_num(aux["slope"], nan=90) <= C.FLOOD_MAX_SLOPE_DEG
    rows = []
    for m in K.gcov_crops():
        if m["track"] != primary["track"]:
            continue
        hh = K.lee_db(io.load_db(C.CROPS / f"{m['name']}_HH.tif"))
        valid = np.isfinite(hh)
        t, how = K.water_threshold(hh, aux["jrc_occurrence"])
        water = valid & (hh < t)
        extra = K.clean(water & ~perm & flat)
        same = m["mode"] == primary["mode"] and m["pol"] == primary["pol"]
        rows.append({"date": m["date"], "mode": m["mode"], "pol": m["pol"], "same_mode_as_primary": same,
                     "threshold_db": round(t, 2), "valid_fraction": round(float(valid.mean()), 3),
                     "water_km2": round(float(water.sum() * K.PIXEL_KM2), 2),
                     "water_outside_permanent_flat_km2": round(float(extra.sum() * K.PIXEL_KM2), 2),
                     "granule_id": m["granule_id"]})
    if write and rows:
        C.DERIVED.mkdir(parents=True, exist_ok=True)
        with open(C.DERIVED / "timeline.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return rows


if __name__ == "__main__":
    for r in run():
        print(r)
