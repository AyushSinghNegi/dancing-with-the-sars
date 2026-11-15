"""One radar colour image per NISAR pass, for the pass-by-pass view in the app's "Check a place".

Every GCOV crop on the primary track taken in the same radar mode and polarisation as the main pair
(config.same_mode: brightness is only comparable between such passes) becomes one map image, drawn
exactly like render.py's "Radar colour" layers: Lee-filtered HH and HV in dB, red = HH, green = HV,
blue = HH/HV, with the same fixed stretch on every date so the dates can be compared by eye.

  python -m pipeline.pass_images
Writes data/derived/overlays/radar_d<date>.webp and data/derived/pass_images.json.
"""
from __future__ import annotations

import json

import numpy as np
from PIL import Image

from . import common as K
from . import config as C
from . import nisar_io as io
from . import render


def same_mode_passes():
    """Primary-track crops with HH and HV, in the main pair's mode and polarisation, oldest first."""
    primary = C.parse_granule_id(C.PRIMARY["before"])
    return [m for m in K.gcov_crops()
            if m["track"] == primary["track"] and m["mode"] == primary["mode"] and m["pol"] == primary["pol"]
            and (C.CROPS / f"{m['name']}_HV.tif").exists()]


def run(write=True):
    out_dir = C.DERIVED / "overlays"
    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        for old in out_dir.glob("radar_d*.webp"):     # no dates from an older run
            old.unlink()
    passes = []
    for m in same_mode_passes():
        layers = {f"{p}_before": render.to_mercator(K.lee_db(io.load_db(C.CROPS / f"{m['name']}_{p.upper()}.tif")))
                  for p in ("hh", "hv")}
        img = render.rgba_for("rgb_before", None, layers)
        name = f"radar_d{m['date']}"
        if write:
            Image.fromarray(img, "RGBA").save(out_dir / f"{name}.webp", "WEBP", quality=80, method=6)
        passes.append({"date": m["date"], "file": f"overlays/{name}.webp", "granule_id": m["granule_id"],
                       "valid_fraction": round(float((img[..., 3] > 0).mean()), 3)})
    out = {"generated": K.now_iso(), "track": C.parse_granule_id(C.PRIMARY["before"])["track"],
           "legend": "Radar colour: red HH, green HV, blue HH/HV; same stretch on every date",
           "passes": passes}
    if write:
        K.write_json(C.DERIVED / "pass_images.json", out)
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
