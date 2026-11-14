"""Check R1-R4 readiness without network calls or revealing credentials.

  python -m pipeline.preflight
  python -m pipeline.preflight --require-crops
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from . import config as C
from . import nisar_io as io


def report():
    needed = []
    for role, gid in C.PRIMARY.items():
        suffixes = ("COH",) if role == "pair" else ("HH", "HV")
        for suffix in suffixes:
            needed.append(C.CROPS / f"{io.crop_name(gid)}_{suffix}.tif")
    needed += [C.AUX / f"aux_{name}.tif" for name in ("jrc_occurrence", "nasadem_elevation", "nasadem_slope")]
    missing = [str(path.relative_to(C.ROOT)) for path in needed if not path.exists()]
    manifest_path = C.CROPS / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    quality_pending = [] if C.IS_DEMO else [gid for gid in C.PRIMARY.values()
        if not any(m.get("quality_rule") and m["granule_id"] == gid for m in manifest)]
    # Report only presence. Do not read or print credential contents.
    configured = bool(os.environ.get("EARTHDATA_TOKEN") or
                      (os.environ.get("EARTHDATA_USERNAME") and os.environ.get("EARTHDATA_PASSWORD")) or
                      Path(os.environ.get("NETRC", str(Path.home() / ".netrc"))).exists())
    return {"demo": C.IS_DEMO, "credentials_configured_not_verified": configured,
            "missing_crops": missing, "quality_pending": quality_pending,
            "ready_to_process": not missing and not quality_pending,
            "local_raw_files": [role for role, gid in C.PRIMARY.items() if (C.RAW / f"{gid}.h5").exists()],
            "reference_files": {name: (C.REFERENCE / name).exists()
                                for name in ("events.geojson", "rainfall.csv", "zones.geojson")}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-crops", action="store_true")
    args = parser.parse_args(argv)
    result = report()
    print(json.dumps(result, indent=2))
    return int(args.require_crops and not result["ready_to_process"])


if __name__ == "__main__":
    raise SystemExit(main())
