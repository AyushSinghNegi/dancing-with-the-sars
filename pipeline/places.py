"""Name the nearest village or suburb for each slide zone and the largest new-water patches.

Uses OpenStreetMap Nominatim reverse geocoding (1 request per second, cached in
data/reference/places_cache.json so reruns are instant and polite). Optional:
if offline, the pipeline carries on without names.

  python -m pipeline.places
Data (c) OpenStreetMap contributors, ODbL.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

from . import config as C

CACHE = C.REFERENCE / "places_cache.json"
URL = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=14&addressdetails=1&lat={lat}&lon={lon}"
UA = "MonsoonLens/0.3 (NASA Space Apps 2026, team iGenfinity; github.com/AyushSinghNegi/dancing-with-the-sars)"


def _key(lat, lon):
    return f"{lat:.3f},{lon:.3f}"


def _label(addr: dict) -> str:
    for k in ("village", "hamlet", "suburb", "neighbourhood", "town", "city_district", "city", "county"):
        if addr.get(k):
            place = addr[k]
            sub = addr.get("state_district") or addr.get("county") or ""
            taluka = addr.get("subdistrict") or ""
            extra = taluka or sub
            return f"{place}, {extra}" if extra and extra != place else place
    return ""


def name(lat, lon, cache, delay=1.1):
    k = _key(lat, lon)
    if k in cache:
        return cache[k]
    req = urllib.request.Request(URL.format(lat=lat, lon=lon), headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        label = _label(d.get("address", {}))
    except Exception:
        return ""
    cache[k] = label
    time.sleep(delay)
    return label


def run(max_slides=60, max_water=25):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    done = 0
    for fname, top in (("slide_zones.geojson", max_slides), ("new_water.geojson", max_water)):
        p = C.DERIVED / fname
        if not p.exists():
            continue
        gj = json.loads(p.read_text())
        feats = gj["features"]
        order = sorted(range(len(feats)), key=lambda i: -(feats[i]["properties"].get("score")
                                                           or feats[i]["properties"].get("area_ha", 0)))
        for i in order[:top]:
            pr = feats[i]["properties"]
            pr["near"] = name(pr["lat"], pr["lon"], cache)
            done += 1
        p.write_text(json.dumps(gj, indent=2))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False, sort_keys=True))
    return done


if __name__ == "__main__":
    print(f"[places] named {run()} features")
