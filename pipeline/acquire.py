"""Inspect and crop catalog-selected real scenes, resuming completed hand-offs.

python -m pipeline.acquire --primary
python -m pipeline.acquire --timeline
Raw remote files are read in windows. This does not download full HDF5 files.
"""
from __future__ import annotations
import argparse
import json
import time
from . import config as C, crop, nisar_io as io
from .common import write_json
from .inspect_h5 import inspect


def acquire(gids, quality_only=False, inspect_only=False, refresh=False):
    if C.IS_DEMO:
        raise ValueError("Acquisition is for real inputs; unset MONSOONLENS_DEMO")
    failed = []
    for gid in dict.fromkeys(gids):
        granule = C.find(gid)
        name = io.crop_name(gid)
        destination = C.CROPS / f"inspection_{name}.json"
        source = crop.source_for(granule)
        suffixes = ("COH",) if granule.product == "GUNW" else ("HH", "HV")
        try:
            if quality_only:
                from .quality import apply
                apply(gid, source)
                continue
            if destination.exists() and not refresh:
                report = json.loads(destination.read_text())
            else:
                print(f"[inspect] {name}", flush=True)
                report = inspect(source)
                write_json(destination, report)
            if report["synthetic"]:
                raise ValueError("Refusing synthetic inspection in real acquisition")
            data_grids = [grid for grid in report["grids"] if "/grids/" in grid["path"]]
            print(f"[inspect] {name}: {len(report['datasets'])} datasets; data grids {data_grids}", flush=True)
            if not any(grid.get("box_intersects_grid") for grid in report["grids"]):
                raise ValueError("No inspected grid intersects the study box")
            if inspect_only:
                continue
            manifest = C.CROPS / "manifest.json"
            entries = json.loads(manifest.read_text()) if manifest.exists() else []
            if any(m["granule_id"] == gid for m in entries) and all((C.CROPS / f"{name}_{s}.tif").exists() for s in suffixes):
                if not any(m.get("quality_rule") for m in entries if m["granule_id"] == gid):
                    from .quality import apply
                    apply(gid, source)
                print(f"[crop] {name}: existing complete crop retained", flush=True)
                continue
            start = time.monotonic()
            print(f"[crop] {name}: reading project window", flush=True)
            _, valid = (io.crop_gcov if granule.product == "GCOV" else io.crop_gunw)(gid, source)
            print(f"[crop] {name}: valid fraction {valid:.4f}; {time.monotonic()-start:.0f}s", flush=True)
            from .quality import apply
            apply(gid, source)
        except Exception as exc:
            print(f"[failed] {name}: {type(exc).__name__}: {exc}", flush=True)
            failed.append({"granule_id": gid, "error_type": type(exc).__name__})
    write_json(C.CROPS / "acquisition_status.json", {"requested": list(dict.fromkeys(gids)), "failed": failed})
    return int(bool(failed))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", action="store_true")
    parser.add_argument("--granule", action="append", default=[])
    parser.add_argument("--inspect-only", action="store_true")
    parser.add_argument("--refresh-inspection", action="store_true")
    parser.add_argument("--timeline", action="store_true")
    parser.add_argument("--quality-only", action="store_true", help="apply native validity masks to already-cropped GCOV/GUNW files")
    parser.add_argument("--stage-extra-timeline", action="store_true",
                        help="acquire only extra timeline dates into data/staging/timeline, without changing the main manifest")
    args = parser.parse_args(argv)
    if args.stage_extra_timeline:
        if args.primary or not args.timeline:
            parser.error("--stage-extra-timeline requires --timeline and excludes --primary")
        C.CROPS = C.DATA / "staging" / "timeline"
    gids = (list(C.PRIMARY.values()) if args.primary else []) + args.granule
    if args.timeline:
        primary = C.find(C.PRIMARY["before"])
        gids += [g.granule_id for g in C.load_candidates() if g.product == "GCOV"
                 and C.same_mode(g, primary) and g.date in C.TIMELINE_DATES]
    if args.stage_extra_timeline:
        gids = [gid for gid in gids if gid not in C.PRIMARY.values()]
    if not gids:
        parser.error("select --primary or --timeline")
    return acquire(gids, quality_only=args.quality_only, inspect_only=args.inspect_only,
                   refresh=args.refresh_inspection)


if __name__ == "__main__":
    raise SystemExit(main())
