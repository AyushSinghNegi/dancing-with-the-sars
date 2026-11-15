"""What is near each likely slide zone: roads, railway lines and settlements.

A zone is a lead to check, not a confirmed landslide. This step only says what lies close to it, so
the people who look after a road, a railway line or a village know which zones concern them.

Sources (© OpenStreetMap contributors, ODbL):
  roads, railways   every way tagged highway = motorway, trunk, primary, secondary or tertiary, or
                    railway = rail, inside the study box, fetched once through the Overpass API on
                    15 Nov 2026 (OSM data as of 2026-11-15T00:45:00Z) and kept unedited, gzipped, as
                    data/reference/osm_roads_raw.json.gz. Query:

    [out:json][timeout:180];(way["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"](18.15,73.3,18.9,74.1);
    way["railway"="rail"](18.15,73.3,18.9,74.1););out tags geom;

  settlements       data/reference/places_osm.csv (pipeline/gazetteer.py)

Distances are straight lines on the map from the edge of the zone, not paths downhill. Smaller roads,
tracks and hamlets that OpenStreetMap does not have, or tags differently, are not counted.

  python -m pipeline.nearby
Writes data/derived/nearby.json and nearby.csv.
"""
from __future__ import annotations

import csv
import gzip
import json

from pyproj import Transformer
from shapely.geometry import LineString, Point, shape as shp
from shapely.ops import transform as shp_transform

from . import common as K
from . import config as C

RAW = C.REFERENCE / "osm_roads_raw.json.gz"
PLACES = C.REFERENCE / "places_osm.csv"
ROAD_M = 1000        # a road or railway counts as "near" within this distance
PLACE_M = 2000       # a settlement counts as "near" within this distance (as for reported events)
MAX_LISTED = 3
ROAD_CLASSES = ("motorway", "trunk", "primary", "secondary", "tertiary")


def _to_grid():
    return Transformer.from_crs(4326, C.GRID_EPSG, always_xy=True).transform


def load_ways(raw=None):
    """[(kind, class, name, ref, LineString in grid metres)] for every road and railway way."""
    d = raw if raw is not None else json.loads(gzip.open(RAW, "rt", encoding="utf-8").read())
    to_xy = _to_grid()
    out = []
    for e in d.get("elements", []):
        g, t = e.get("geometry") or [], e.get("tags", {})
        if e.get("type") != "way" or len(g) < 2:
            continue
        kind = "rail" if t.get("railway") == "rail" else "road" if t.get("highway") in ROAD_CLASSES else None
        if not kind:
            continue
        xs, ys = to_xy([p["lon"] for p in g], [p["lat"] for p in g])
        out.append((kind, t.get("highway") or "rail", (t.get("name:en") or t.get("name") or "").strip(),
                    (t.get("ref") or "").strip(), LineString(list(zip(xs, ys)))))
    return out


def load_places():
    to_xy = _to_grid()
    out = []
    if not PLACES.exists():
        return out
    with open(PLACES, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            x, y = to_xy(float(r["lon"]), float(r["lat"]))
            out.append({"name": r["name"], "name_mr": r.get("name_mr", ""), "type": r["place"], "pt": Point(x, y)})
    return out


def nearest_lines(geom, ways, kind):
    """Distinct roads (or railway lines) by distance from geom, nearest first. One entry per ref or name;
    ways with neither are grouped by class."""
    best = {}
    for k, cls, name, ref, line in ways:
        if k != kind:
            continue
        d = geom.distance(line)
        key = ref or name or f"unnamed {cls}"
        if key not in best or d < best[key]["distance_m"]:
            best[key] = {"name": name, "ref": ref, "class": cls, "distance_m": d}
    out = sorted(best.values(), key=lambda r: r["distance_m"])
    for r in out:
        r["distance_m"] = int(round(r["distance_m"]))
    return out


def nearest_places(geom, places):
    out = [{"name": p["name"], "name_mr": p["name_mr"], "type": p["type"],
            "distance_m": int(round(geom.distance(p["pt"])))} for p in places]
    return sorted(out, key=lambda r: r["distance_m"])


def describe(geom, ways, places):
    """Everything listed for one zone: what is within range, and the nearest of each kind whatever the range."""
    roads, rails, pl = nearest_lines(geom, ways, "road"), nearest_lines(geom, ways, "rail"), nearest_places(geom, places)
    return {"roads": [r for r in roads if r["distance_m"] <= ROAD_M][:MAX_LISTED],
            "railways": [r for r in rails if r["distance_m"] <= ROAD_M][:MAX_LISTED],
            "places": [p for p in pl if p["distance_m"] <= PLACE_M][:MAX_LISTED],
            "nearest_road": roads[0] if roads else None, "nearest_railway": rails[0] if rails else None,
            "nearest_place": pl[0] if pl else None}


def line_label(r) -> str:
    return " ".join(x for x in (r["ref"], r["name"]) if x) or f"unnamed {r['class']} road"


def run(write=True):
    zp = C.DERIVED / "slide_zones.geojson"
    if not (zp.exists() and RAW.exists()):
        for n in ("nearby.json", "nearby.csv"):
            (C.DERIVED / n).unlink(missing_ok=True)       # never leave a stale list behind
        print("      slide zones or the OpenStreetMap road file not found; skipping")
        return None
    ways, places, to_xy = load_ways(), load_places(), _to_grid()
    zones = {}
    for f in json.loads(zp.read_text())["features"]:
        p = f["properties"]
        geom = shp_transform(lambda x, y, z=None: to_xy(x, y), shp(f["geometry"]))
        zones[p["id"]] = {"lat": p["lat"], "lon": p["lon"], "confidence": p.get("confidence"), "score": p.get("score"),
                          **describe(geom, ways, places)}
    n = len(zones)
    summary = {"zones": n,
               "road_within": sum(bool(z["roads"]) for z in zones.values()),
               "railway_within": sum(bool(z["railways"]) for z in zones.values()),
               "place_within": sum(bool(z["places"]) for z in zones.values()),
               "nothing_within": sum(not (z["roads"] or z["railways"] or z["places"]) for z in zones.values())}
    out = {"generated": K.now_iso(), "road_m": ROAD_M, "place_m": PLACE_M,
           "source": "OpenStreetMap contributors (ODbL): roads and railways via Overpass, data as of "
                     "2026-11-15T00:45:00Z; settlements from data/reference/places_osm.csv",
           "road_classes": list(ROAD_CLASSES), "ways": len(ways), "places": len(places),
           "summary": summary, "zones": zones}
    if write:
        K.write_json(C.DERIVED / "nearby.json", out)
        order = sorted(zones, key=lambda i: (-(zones[i]["score"] or 0), i))
        with open(C.DERIVED / "nearby.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["zone", "confidence", "lat", "lon", "nearest_road", "road_class", "road_distance_m",
                        "nearest_railway", "railway_distance_m", "nearest_settlement", "settlement_type",
                        "settlement_distance_m", f"roads_within_{ROAD_M}m", f"railways_within_{ROAD_M}m",
                        f"settlements_within_{PLACE_M}m"])
            for i in order:
                z = zones[i]
                r, rl, pl = z["nearest_road"], z["nearest_railway"], z["nearest_place"]
                w.writerow([i, z["confidence"], z["lat"], z["lon"],
                            line_label(r) if r else "", r["class"] if r else "", r["distance_m"] if r else "",
                            (rl["name"] or "railway line") if rl else "", rl["distance_m"] if rl else "",
                            pl["name"] if pl else "", pl["type"] if pl else "", pl["distance_m"] if pl else "",
                            "; ".join(f"{line_label(x)} ({x['distance_m']} m)" for x in z["roads"]),
                            "; ".join(f"{x['name'] or 'railway line'} ({x['distance_m']} m)" for x in z["railways"]),
                            "; ".join(f"{x['name']} ({x['distance_m']} m)" for x in z["places"])])
    return out


if __name__ == "__main__":
    s = run()
    if s:
        print(json.dumps({k: v for k, v in s.items() if k != "zones"}, indent=2))
