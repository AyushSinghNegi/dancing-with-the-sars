"""Project-wide settings for MonsoonLens.

Every path, box and scene choice lives here so the pipeline, the app and the
docs agree. Change values here, not inside other modules.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import os

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REFERENCE = DATA / "reference"
AUX = DATA / "crops"            # JRC water, slope, elevation on the analysis grid (committed, real)
ANCILLARY = DATA / "ancillary"  # JRC water and DEM source tiles (never committed)
DEMO = DATA / "demo"            # synthetic NISAR-format inputs and outputs, for development only

# MONSOONLENS_DEMO=1 sends every NISAR read and write to data/demo/ so synthetic
# test data can never mix with real results.
IS_DEMO = os.environ.get("MONSOONLENS_DEMO") == "1"
RAW = (DEMO / "raw") if IS_DEMO else (DATA / "raw")            # full .h5 files, if downloaded (never committed)
CROPS = (DEMO / "crops") if IS_DEMO else (DATA / "crops")      # NISAR crops (int16 GeoTIFF)
DERIVED = (DEMO / "derived") if IS_DEMO else (DATA / "derived")  # everything the app reads

# Project box (WGS84): Pune city, Mulshi, Maval, Lonavala and the Ghats edge.
AOI = {"west": 73.30, "south": 18.15, "east": 74.10, "north": 18.90}

# Analysis grid: UTM zone 43N, 40 m pixels (multilooked from NISAR's native posting).
GRID_EPSG = 32643
GRID_RES = 40.0

# Primary case study: track 034, descending, frame 079 (same mode on both dates).
PRIMARY = {
    "before": "NISAR_L2_PR_GCOV_024_034_D_079_4005_DHDH_A_20260628T134239_20260628T134314_P05023_N_F_J_001",
    "after": "NISAR_L2_PR_GCOV_025_034_D_079_4005_DHDH_A_20260710T134239_20260710T134313_P05023_N_F_J_001",
    "pair": "NISAR_L2_PR_GUNW_024_034_D_079_025_4000_SH_20260628T134239_20260628T134314_20260710T134239_20260710T134313_P05023_N_F_J_001",
}

# Extra same-track dates for the timeline (R7/R8). Mode is checked from the file name.
TIMELINE_DATES = ["2026-06-28", "2026-07-10", "2026-07-22", "2026-08-15", "2026-10-14"]

# Thresholds (documented on the Method page; tune only with a written reason).
WATER_DB_BOUNDS = (-20.0, -11.0)   # guard rails for the per-date HH water threshold (dB)
WATER_TRAIN_OCCURRENCE = 90        # JRC occurrence % of the reservoir/river cores used to train it
CHANGE_DB = 3.0                    # |after - before| in dB that counts as real change
PERMANENT_WATER_OCCURRENCE = 50    # JRC occurrence % treated as permanent water
FLOOD_MAX_SLOPE_DEG = 5.0          # floods are mapped only on near-flat ground
SLIDE_MIN_SLOPE_DEG = 15.0         # slide zones only on steep ground...
SLIDE_MAX_SLOPE_DEG = 45.0         # ...but not on cliffs (bare rock, radar layover)
SLIDE_HH_RISE_DB = 3.0             # fresh debris: HH rises (about the scene's top 1% on steep ground)
SLIDE_HV_DROP_DB = 2.0             # stripped vegetation: HV drops (about the scene's bottom 1%)
INCIDENCE_DEG = 40.0               # approximate NISAR incidence over Pune, for the layover/shadow mask
COHERENCE_LOW = 0.35               # coherence below this is "lost"
MIN_PATCH_PIXELS = 4               # new-water patches: 4 px at 40 m = 0.64 ha
RISE_BUFFER_M = 120                # new water within this distance of water JRC has ever seen = reservoir/river rise
MIN_SLIDE_PIXELS = 2               # slide zones: 2 px = 0.32 ha (a slide that buries a house can be this small)
HIDDEN_WATER_RATIO_DB = 2.0        # possible water under cover: HH must rise this much more than HV (double bounce)
HIDDEN_WATER_NEAR_M = 2000         # ...and lie within this distance of a river, reservoir or new water


@dataclass(frozen=True)
class Granule:
    granule_id: str
    product: str
    track: str
    direction: str
    frame: str
    mode: str
    pol: str
    date: str
    date2: str | None
    url: str
    size_mb: float


def parse_granule_id(gid: str) -> dict:
    """Pull track, frame, mode, polarisation and dates out of a NISAR file name."""
    f = gid.split("_")
    product = f[3]
    if product == "GCOV":
        return {"product": product, "track": f[5], "direction": f[6], "frame": f[7],
                "mode": f[8], "pol": f[9], "date": f"{f[11][:4]}-{f[11][4:6]}-{f[11][6:8]}", "date2": None}
    if product == "GUNW":
        return {"product": product, "track": f[5], "direction": f[6], "frame": f[7],
                "mode": f[9], "pol": f[10], "date": f"{f[11][:4]}-{f[11][4:6]}-{f[11][6:8]}",
                "date2": f"{f[13][:4]}-{f[13][4:6]}-{f[13][6:8]}"}
    raise ValueError(f"Unsupported product in {gid}")


def load_candidates(aoi: str = "pune") -> list[Granule]:
    rows = []
    with open(REFERENCE / "candidate_scenes.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["aoi"] != aoi:
                continue
            p = parse_granule_id(r["granule_id"])
            rows.append(Granule(r["granule_id"], p["product"], p["track"], p["direction"], p["frame"],
                                p["mode"], p["pol"], p["date"], p["date2"], r["download_url"],
                                float(r["size_mb"] or 0)))
    return rows


def find(gid: str) -> Granule:
    for g in load_candidates():
        if g.granule_id == gid:
            return g
    raise KeyError(gid)


def same_mode(a: Granule, b: Granule) -> bool:
    """Backscatter is only compared between files taken in the same radar mode and polarisation."""
    return a.mode == b.mode and a.pol == b.pol and a.track == b.track
