"""Daily rainfall over the study box (U2 interim source, no login needed).

NASA POWER daily API, parameter PRECTOTCORR (MERRA-2 corrected precipitation,
mm/day). We average a 3 x 3 grid of points across the box. GPM IMERG via
Giovanni is finer and observation-based, and data/reference/rainfall.csv now holds
IMERG Late Run (see data/reference/SOURCES.md). This script therefore writes
data/reference/rainfall_power.csv for comparison and never touches rainfall.csv.

  python -m pipeline.rainfall
"""
from __future__ import annotations

import csv
import json
import urllib.request

import numpy as np

from . import config as C

API = ("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG"
       "&longitude={lon:.3f}&latitude={lat:.3f}&start={start}&end={end}&format=JSON")
SOURCE = "NASA POWER daily PRECTOTCORR (MERRA-2), mean of 9 points over the study box"


def fetch(start="20260601", end="20261031"):
    lons = np.linspace(C.AOI["west"] + 0.1, C.AOI["east"] - 0.1, 3)
    lats = np.linspace(C.AOI["south"] + 0.1, C.AOI["north"] - 0.1, 3)
    series = []
    for lat in lats:
        for lon in lons:
            with urllib.request.urlopen(API.format(lon=lon, lat=lat, start=start, end=end), timeout=60) as r:
                d = json.load(r)["properties"]["parameter"]["PRECTOTCORR"]
            series.append(d)
    dates = sorted(series[0])
    rows = []
    for k in dates:
        vals = [s[k] for s in series if s.get(k, -999) > -900]
        if vals:
            rows.append({"date": f"{k[:4]}-{k[4:6]}-{k[6:]}", "precip_mm": round(float(np.mean(vals)), 2),
                         "max_point_mm": round(float(np.max(vals)), 2), "source": SOURCE})
    return rows


def main():
    rows = fetch()
    C.REFERENCE.mkdir(parents=True, exist_ok=True)
    with open(C.REFERENCE / "rainfall_power.csv", "w", newline="") as fh:   # never overwrite the IMERG file
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    jul = [r for r in rows if "2026-07-01" <= r["date"] <= "2026-07-10"]
    top = sorted(jul, key=lambda r: -r["precip_mm"])[:3]
    print(f"[rainfall] {len(rows)} days; 1-10 Jul total {sum(r['precip_mm'] for r in jul):.0f} mm (box mean); "
          f"wettest days: {[(r['date'], r['precip_mm']) for r in top]}")


if __name__ == "__main__":
    main()
