"""Village, town and suburb names in the study box, for the app's "Check a place" search.

Source: OpenStreetMap (© OpenStreetMap contributors, ODbL), every node tagged place=city, town,
village or suburb inside the study box, fetched once through the Overpass API on 14 Nov 2026 and kept
unedited as data/reference/osm_places_raw.json. Query:

  [out:json][timeout:60];(node["place"~"^(city|town|village|suburb)$"](18.15,73.3,18.9,74.1););out body;

  python -m pipeline.gazetteer
Writes data/reference/places_osm.csv (name, Marathi name where OSM has one, type, lat, lon, OSM id).
"""
from __future__ import annotations

import csv
import json

from . import config as C

RAW = C.REFERENCE / "osm_places_raw.json"
OUT = C.REFERENCE / "places_osm.csv"
RANK = {"city": 0, "town": 1, "suburb": 2, "village": 3}


def run():
    d = json.loads(RAW.read_text(encoding="utf-8"))
    rows, seen = [], set()
    for e in d.get("elements", []):
        t = e.get("tags", {})
        name = (t.get("name:en") or t.get("name") or "").strip()
        if not name or e.get("type") != "node":
            continue
        lat, lon = float(e["lat"]), float(e["lon"])
        if not (C.AOI["south"] <= lat <= C.AOI["north"] and C.AOI["west"] <= lon <= C.AOI["east"]):
            continue
        key = (name.lower(), round(lat, 3), round(lon, 3))
        if key in seen:
            continue
        seen.add(key)
        rows.append({"name": name, "name_mr": (t.get("name:mr") or "").strip(), "place": t.get("place", ""),
                     "lat": round(lat, 5), "lon": round(lon, 5), "osm_id": e.get("id")})
    rows.sort(key=lambda r: (RANK.get(r["place"], 9), r["name"]))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "name_mr", "place", "lat", "lon", "osm_id"])
        w.writeheader()
        w.writerows(rows)
    return {"places": len(rows), "with_marathi": sum(bool(r["name_mr"]) for r in rows)}


if __name__ == "__main__":
    print(run())
