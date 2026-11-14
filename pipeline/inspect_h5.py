"""Print what is inside a NISAR HDF5 file (R3).

  python -m pipeline.inspect_h5 data/raw/NISAR_L2_PR_GCOV_....h5
  python -m pipeline.inspect_h5 https://nisar.asf.earthdatacloud.nasa.gov/...h5   (streams)

Lists every dataset with shape and type, the projection, pixel spacing and
the mask values inside the Pune box, so CONTEXT.md can record the real paths.
"""
from __future__ import annotations

import sys

import h5py
import numpy as np

from . import nisar_io as io


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    with io.open_h5(argv[0]) as f:
        rows = []
        f.visititems(lambda n, o: rows.append((n, o.shape, o.dtype)) if isinstance(o, h5py.Dataset) else None)
        big = [r for r in rows if len(r[1]) == 2 and r[1][0] > 100]
        print(f"{len(rows)} datasets; 2-D layers:")
        for n, s, d in big:
            print(f"  /{n}  {s}  {d}")
        for grp in sorted({"/" + n.rsplit("/", 1)[0] for n, s, d in rows if n.endswith("xCoordinates")}):
            x, y = f[f"{grp}/xCoordinates"], f[f"{grp}/yCoordinates"]
            epsg = io._epsg(f[f"{grp}/projection"]) if f"{grp}/projection" in f else "?"
            print(f"\ngrid {grp}: EPSG {epsg}, {len(y)} x {len(x)} px, spacing "
                  f"{abs(float(x[1]) - float(x[0])):.1f} m x {abs(float(y[1]) - float(y[0])):.1f} m")
        if f"{io.GCOV_GRID}/mask" in f:
            m = f[f"{io.GCOV_GRID}/mask"]
            sub = m[:: max(1, m.shape[0] // 400), :: max(1, m.shape[1] // 400)]
            vals, counts = np.unique(sub, return_counts=True)
            print("\nmask values (sampled):", dict(zip(vals.tolist(), counts.tolist())))
        ident = "/science/LSAR/identification"
        if ident in f:
            for k in ("trackNumber", "frameNumber", "orbitPassDirection", "zeroDopplerStartTime", "lookDirection"):
                if k in f[ident]:
                    v = f[ident][k][()]
                    print(f"{k}: {v.decode() if isinstance(v, bytes) else v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
