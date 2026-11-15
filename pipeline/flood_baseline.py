"""Chance level for the reported-flood matches: would places nobody reported match just as often?

validate.py counts a reported flood as matched when new open water OR a "possible water under cover"
patch lies within max(precision_m, 500 m) of the reported place. Those patches are scattered over the
flat ground, and the tolerance can be 1.5 km, so some matches are expected by luck alone. This module
measures how many.

The same rule is applied to two reference sets of places that were not picked because of a report:

  flat ground   every 40 m pixel with radar data on both dates, outside permanent water, with slope
                <= FLOOD_MAX_SLOPE_DEG: the ground on which the method can map water at all
  settlements   every city, town, suburb and village in the box that has radar data (OpenStreetMap,
                data/reference/places_osm.csv): the kind of place a flood is reported from

For each observable reported flood, its chance is the share of the reference set that has a detection
within that report's own tolerance. The expected number of chance matches is the sum of those shares,
and the probability of at least the observed number follows exactly (Poisson-binomial). Nothing is
drawn at random, so there is no seed and the result is the same on every run.

Reads the published map layers in data/derived/geotiff, so it runs after render, and also on a
machine that has the published output but not the pipeline's intermediate layers.

  python -m pipeline.flood_baseline
Writes data/derived/flood_baseline.json.
"""
from __future__ import annotations

import csv
import json

import numpy as np
import rasterio

from . import ancillary
from . import common as K
from . import config as C
from . import validate

LAYERS = {"new_water": "new_water", "possible_water": "possible_water_under_cover"}
CURVE_M = list(range(0, 3001, 100))


def chance_of_match(dist_at_places, tolerance_m) -> float:
    """Share of the reference places that have a detection within tolerance_m."""
    d = np.asarray(dist_at_places, float)
    return float(np.mean(d <= tolerance_m)) if d.size else float("nan")


def prob_at_least(ps, k) -> float:
    """P(at least k successes) for independent trials with probabilities ps (Poisson-binomial, exact)."""
    dist = np.zeros(len(ps) + 1)
    dist[0] = 1.0
    for p in ps:
        new = dist * (1 - p)
        new[1:] += dist[:-1] * p
        dist = new
    return float(dist[max(int(k), 0):].sum())


def observable_floods(events, valid, before, after):
    """Reported floods that validate.py scores, with the same tests in the same order."""
    out = []
    for f in events:
        p = f["properties"]
        if p.get("type", "").strip().lower() not in validate.FLOOD_TYPES:
            continue
        lon, lat = f["geometry"]["coordinates"][:2]
        r, c, shape = K.lonlat_to_rowcol(lon, lat)
        prec = float(p.get("precision_m") or 500)
        date = p.get("date", "")
        if not (0 <= r < shape[0] and 0 <= c < shape[1]) or not valid[r, c]:
            continue
        if (date and not (before < date <= after)) or prec > 2000:
            continue
        out.append({"id": p.get("id"), "place": p.get("place", ""), "row": r, "col": c,
                    "tolerance_m": int(max(prec, validate.RADIUS["flood"]))})
    return out


def _mask(name):
    p = C.DERIVED / "geotiff" / f"{name}.tif"
    if not p.exists():
        return None
    with rasterio.open(p) as d:
        return d.read(1) == 1


def _settlement_cells(valid):
    p = C.REFERENCE / "places_osm.csv"
    if not p.exists():
        return [], []
    rows, cols = [], []
    with open(p, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r, c, shape = K.lonlat_to_rowcol(float(row["lon"]), float(row["lat"]))
            if 0 <= r < shape[0] and 0 <= c < shape[1] and valid[r, c]:
                rows.append(r)
                cols.append(c)
    return rows, cols


def _validation_csv_count():
    """What the last full validation run recorded, to show when this file and that run are out of step."""
    p = C.DERIVED / "validation.csv"
    if not p.exists():
        return None
    rows = [r for r in csv.DictReader(open(p, encoding="utf-8"))
            if r["type"] in validate.FLOOD_TYPES and r["observable"] == "yes"]
    return {"hits": sum(r["result"] == "hit" for r in rows), "of": len(rows)}


def run(write=True):
    masks = {k: _mask(v) for k, v in LAYERS.items()}
    if any(m is None for m in masks.values()):
        (C.DERIVED / "flood_baseline.json").unlink(missing_ok=True)   # never leave a stale check behind
        print("      published water layers not found; skipping the flood chance level")
        return None
    before = C.parse_granule_id(C.PRIMARY["before"])["date"]
    after = C.parse_granule_id(C.PRIMARY["after"])["date"]
    pair = K.load_pair()
    valid = np.isfinite(pair["hh_before"]) & np.isfinite(pair["hh_after"])
    aux = ancillary.load()
    slope, occ = np.nan_to_num(aux["slope"]), np.nan_to_num(aux["jrc_occurrence"])
    flat = valid & (occ < C.PERMANENT_WATER_OCCURRENCE) & (slope <= C.FLOOD_MAX_SLOPE_DEG)

    d_any = validate._dist_m(masks["new_water"] | masks["possible_water"])
    d_each = {k: validate._dist_m(m) for k, m in masks.items()}
    s_rows, s_cols = _settlement_cells(valid)
    ref = {"flat_ground": d_any[flat], "settlements": d_any[s_rows, s_cols]}

    events = []
    for e in observable_floods(validate.load_events(), valid, before, after):
        r, c = e.pop("row"), e.pop("col")
        d = d_any[r, c]
        e.update(distance_m=int(round(d)) if np.isfinite(d) else None, matched=bool(d <= e["tolerance_m"]),
                 nearest_layer=min(d_each, key=lambda k: d_each[k][r, c]),
                 nearest_new_water_m=int(round(d_each["new_water"][r, c])),
                 nearest_possible_water_m=int(round(d_each["possible_water"][r, c])),
                 chance={k: round(chance_of_match(v, e["tolerance_m"]), 3) for k, v in ref.items()})
        events.append(e)
    observed = sum(e["matched"] for e in events)

    what = {"flat_ground": f"every {C.GRID_RES:.0f} m pixel with radar data on both dates, outside permanent water, "
                           f"slope <= {C.FLOOD_MAX_SLOPE_DEG:.0f} deg",
            "settlements": "every city, town, suburb and village in the box with radar data "
                           "(OpenStreetMap, data/reference/places_osm.csv)"}
    reference = {}
    for k, v in ref.items():
        ps = [chance_of_match(v, e["tolerance_m"]) for e in events]
        reference[k] = {"what": what[k], "places": int(v.size),
                        "expected_matches": round(float(np.sum(ps)), 2),
                        "prob_at_least_observed": round(prob_at_least(ps, observed), 3),
                        "curve": [[m, round(chance_of_match(v, m), 3)] for m in CURVE_M]}
    reference["flat_ground"]["km2"] = round(float(flat.sum() * K.PIXEL_KM2), 1)

    out = {"generated": K.now_iso(),
           "rule": f"a reported flood is matched when new water or a possible-water patch lies within "
                   f"max(precision_m, {validate.RADIUS['flood']} m) of the reported place",
           "layers": {k: {"file": f"geotiff/{LAYERS[k]}.tif", "km2": round(float(m.sum() * K.PIXEL_KM2), 3)}
                      for k, m in masks.items()},
           "observed": {"matched": observed, "of": len(events),
                        "matched_to_new_water": sum(e["matched"] and e["nearest_layer"] == "new_water" for e in events)},
           "validation_csv": _validation_csv_count(),
           "events": events, "reference": reference}
    if write:
        K.write_json(C.DERIVED / "flood_baseline.json", out)
    return out


if __name__ == "__main__":
    s = run()
    if s:
        print(json.dumps({k: v for k, v in s.items() if k != "events"} |
                         {"reference": {k: {a: b for a, b in v.items() if a != "curve"}
                                        for k, v in s["reference"].items()}}, indent=2))
        for e in s["events"]:
            print(e)
