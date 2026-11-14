"""Check radar detections against reported events (R9).

Input: data/reference/events.geojson (Urvashi, U3). One Point per reported
event with properties:
  id, type (flood | waterlogging | river_overflow | landslide | road_closure),
  date (YYYY-MM-DD), place, precision_m (how exact the location is: 100,
  500, 2000), source_name, source_url, note.

For each event we decide:
  * observable? (inside the radar box with data, and happened between the two
    radar dates, 28 Jun and 10 Jul)
  * hit / miss: is there a matching detection within max(precision_m, 500 m)
    (floods) or max(precision_m, 750 m) (slides)?
  * for misses, the most likely reason radar could not see it.

  python -m pipeline.validate
Writes data/derived/validation.csv and validation_summary.json.
"""
from __future__ import annotations

import csv
import json

import numpy as np
from scipy import ndimage as ndi

from . import ancillary
from . import common as K
from . import config as C

FLOOD_TYPES = {"flood", "waterlogging", "river_overflow"}
SLIDE_TYPES = {"landslide"}
RADIUS = {"flood": 500, "slide": 750}


def events_path():
    demo = C.DEMO / "reference" / "events.geojson"
    return demo if C.IS_DEMO else C.REFERENCE / "events.geojson"


def load_events():
    p = events_path()
    if not p.exists():
        return []
    return json.loads(p.read_text()).get("features", [])


def _dist_m(mask):
    if not mask.any():
        return np.full(mask.shape, np.inf)
    return ndi.distance_transform_edt(~mask) * C.GRID_RES


def run(write=True):
    before = C.parse_granule_id(C.PRIMARY["before"])["date"]
    after = C.parse_granule_id(C.PRIMARY["after"])["date"]
    lay = {k: K.load_layer(k) for k in ("new_water", "brighter", "slide_zones", "valid", "hh_before")}
    slope = np.nan_to_num(ancillary.load()["slope"])
    d_flood = _dist_m(lay["new_water"] | lay["brighter"])
    d_slide = _dist_m(lay["slide_zones"])
    rows = []
    for f in load_events():
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        typ = p.get("type", "").strip().lower()
        group = "flood" if typ in FLOOD_TYPES else "slide" if typ in SLIDE_TYPES else "other"
        r, c, shape = K.lonlat_to_rowcol(lon, lat)
        prec = float(p.get("precision_m") or 500)
        row = {"id": p.get("id"), "type": typ, "date": p.get("date", ""), "place": p.get("place", ""),
               "lon": lon, "lat": lat, "precision_m": int(prec), "observable": "no", "result": "",
               "distance_m": "", "reason": "", "source_name": p.get("source_name", ""),
               "source_url": p.get("source_url", "")}
        inside = 0 <= r < shape[0] and 0 <= c < shape[1]
        if not inside:
            row.update(result="not observable", reason="outside the radar box")
        elif not lay["valid"][r, c]:
            row.update(result="not observable", reason="no radar data at this spot (edge of swath)")
        elif row["date"] and not (before < row["date"] <= after):
            row.update(result="not observable",
                       reason=f"happened {'before' if row['date'] <= before else 'after'} the radar pair "
                              f"({before} to {after})")
        elif group == "other":
            row.update(result="not scored", reason="event type has no radar layer (e.g. road closure)")
        else:
            row["observable"] = "yes"
            dist = (d_flood if group == "flood" else d_slide)[r, c]
            radius = max(prec, RADIUS[group])
            row["distance_m"] = "" if not np.isfinite(dist) else int(round(dist))
            if dist <= radius:
                row.update(result="hit", reason="")
            else:
                row.update(result="miss", reason=_why(group, row, r, c, lay, slope, after))
        rows.append(row)

    summary = _summary(rows, lay)
    if write:
        C.DERIVED.mkdir(parents=True, exist_ok=True)
        cols = ["id", "type", "date", "place", "lon", "lat", "precision_m", "observable", "result",
                "distance_m", "reason", "source_name", "source_url"]
        with open(C.DERIVED / "validation.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        K.write_json(C.DERIVED / "validation_summary.json", summary)
    return summary, rows


def _why(group, row, r, c, lay, slope, after):
    win = (slice(max(0, r - 6), r + 7), slice(max(0, c - 6), c + 7))
    if group == "flood":
        if np.nanmedian(lay["hh_before"][win]) > -6:
            return "dense buildings: radar bounces off walls, which hides street flooding"
        if row["date"] and row["date"] < after:
            return "water may have drained before the 10 Jul pass"
        return "flooding smaller than our 40 m pixels or under thick canopy"
    if np.median(slope[win]) < C.SLIDE_MIN_SLOPE_DEG:
        return "ground near the report is gentler than our 15 deg slide search"
    return "slide smaller than a few 40 m pixels, or coherence lost everywhere nearby"


def _summary(rows, lay):
    out = {"events": len(rows)}
    for group, types in (("flood", FLOOD_TYPES), ("slide", SLIDE_TYPES)):
        obs = [r for r in rows if r["type"] in types and r["observable"] == "yes"]
        hits = [r for r in obs if r["result"] == "hit"]
        out[group] = {"reported": sum(r["type"] in types for r in rows), "observable": len(obs),
                      "hits": len(hits), "hit_rate": round(len(hits) / len(obs), 3) if obs else None}
    # Detections with no report nearby: changes nobody reported (worth a look).
    evs = [(r["lon"], r["lat"]) for r in rows]
    for name, layer, km in (("unreported_slide_zones", "slide_zones", 2.0),):
        lab, n = ndi.label(lay[layer], structure=np.ones((3, 3)))
        if n == 0 or not evs:
            out[name] = n
            continue
        ev_mask = np.zeros(lab.shape, bool)
        for lon, lat in evs:
            r, c, shape = K.lonlat_to_rowcol(lon, lat)
            if 0 <= r < shape[0] and 0 <= c < shape[1]:
                ev_mask[r, c] = True
        near = _dist_m(ev_mask) <= km * 1000
        out[name] = int(n - len(set(np.unique(lab[near & (lab > 0)]))))
    return out


if __name__ == "__main__":
    s, rows = run()
    print(json.dumps(s, indent=2))
