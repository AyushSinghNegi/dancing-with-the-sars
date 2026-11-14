"""Cut NISAR files down to the Pune box (R2 + R4).

Streams only the needed part of each file from ASF (about 1/10 of the
frame), or uses a full file if you already downloaded it into data/raw/.

  python -m pipeline.crop --primary      # GCOV 28 Jun, GCOV 10 Jul, GUNW pair  (CP1/CP2)
  python -m pipeline.crop --timeline     # extra GCOV dates for the timeline     (R7)
  python -m pipeline.crop --granule NISAR_L2_PR_GCOV_...
  python -m pipeline.crop --file data/raw/NISAR_L2_PR_GCOV_....h5

Login: set EARTHDATA_TOKEN in your own terminal (create one at
urs.earthdata.nasa.gov > Generate Token), or have a ~/.netrc / _netrc for
urs.earthdata.nasa.gov; otherwise earthaccess asks for your username and
password in the terminal. Never commit tokens or .netrc files.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from . import config as C
from . import nisar_io as io


def source_for(g: C.Granule) -> str:
    local = C.RAW / f"{g.granule_id}.h5"
    return str(local) if local.exists() else g.url


def run(gids: list[str], files: dict[str, str] | None = None) -> int:
    files = files or {}
    failures = 0
    for gid in gids:
        g = C.find(gid) if gid not in files else None
        src = files.get(gid) or source_for(g)
        kind = C.parse_granule_id(gid)["product"]
        t0 = time.time()
        print(f"[crop] {kind} {gid}\n       from {'local file' if not src.startswith('http') else 'ASF (streaming)'}", flush=True)
        try:
            name, valid = (io.crop_gcov if kind == "GCOV" else io.crop_gunw)(gid, src)
            note = "" if valid > 0.5 else "  <-- under half the box has data: check the footprint"
            print(f"       -> data/crops/{name}_*.tif  ({valid:.0%} of box valid, {time.time() - t0:.0f}s){note}")
        except Exception as e:  # keep going so one bad file does not block the rest
            failures += 1
            print(f"       FAILED: {type(e).__name__}: {e}", file=sys.stderr)
    return failures


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--primary", action="store_true")
    ap.add_argument("--timeline", action="store_true")
    ap.add_argument("--granule", action="append", default=[])
    ap.add_argument("--file", action="append", default=[])
    a = ap.parse_args(argv)
    gids, files = list(a.granule), {}
    if a.primary:
        gids += [C.PRIMARY["before"], C.PRIMARY["after"], C.PRIMARY["pair"]]
    if a.timeline:
        primary = C.find(C.PRIMARY["before"])
        for g in C.load_candidates():
            if g.product == "GCOV" and C.same_mode(g, primary) and g.date in C.TIMELINE_DATES \
                    and g.granule_id not in gids:
                gids.append(g.granule_id)
    for p in a.file:
        gid = Path(p).stem
        files[gid] = p
        gids.append(gid)
    if not gids:
        ap.print_help()
        return 2
    return 1 if run(gids, files) else 0


if __name__ == "__main__":
    raise SystemExit(main())
