"""How much do the water numbers depend on the water threshold?

The threshold is set per date from the radar itself (Kittler-Illingworth on JRC reservoir cores). Here
both dates' thresholds are moved together by -1 dB and +1 dB, everything else unchanged, and the
water results are recomputed. If the story changed with a 1 dB nudge, the numbers would be fragile.

  python -m pipeline.sensitivity
Writes data/derived/sensitivity.json.
"""
from __future__ import annotations

from . import ancillary
from . import common as K
from . import config as C
from . import water

SHIFTS = (-1.0, 0.0, 1.0)
KEEP = ("threshold_before_db", "threshold_after_db", "new_water_km2", "rise_km2", "flood_km2", "flood_patches",
        "permanent_water_seen_dark")


def run(write=True):
    aux = ancillary.load()
    d = K.load_pair()
    rows = []
    for s in SHIFTS:
        stats, _, _ = water.compute(d, aux, shift_db=s)
        v = {m: val for m, val, *_ in stats}
        rows.append({"shift_db": s, **{k: round(v[k], 3) if isinstance(v[k], float) else v[k] for k in KEEP}})
    base = next(r for r in rows if r["shift_db"] == 0)
    out = {"shifts_db": list(SHIFTS), "rows": rows,
           "range": {k: [min(r[k] for r in rows), max(r[k] for r in rows)] for k in ("new_water_km2", "rise_km2",
                                                                                    "flood_km2")},
           "base": {k: base[k] for k in ("new_water_km2", "rise_km2", "flood_km2")}}
    if write:
        K.write_json(C.DERIVED / "sensitivity.json", out)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=1))
