"""R3: inspect a local or streamed NISAR file and save a reproducible report.

python -m pipeline.inspect_h5 FILE_OR_URL --json data/crops/inspection.json
Lists dataset paths/types/shapes, fill values, grid geometry and mask samples
inside the project box. Does not read full raster layers or expose credentials.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import h5py
import numpy as np
from pyproj import Transformer
from . import nisar_io as io, config as C
from .common import write_json


def scalar(value):
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    if isinstance(value, np.ndarray):
        return [scalar(item) for item in value.ravel()]
    if isinstance(value, np.generic):
        return scalar(value.item())
    if isinstance(value, complex):
        return {"real": value.real, "imaginary": value.imag}
    return value


def inspect(src):
    report = {"source": Path(str(src).split("?")[0]).name, "datasets": [], "grids": [], "identification": {}}
    with io.open_h5(src, block_size=256 * 1024) as f:
        report["synthetic"] = "SYNTHETIC" in f.attrs
        paths = []
        def visit(name, obj):
            if not isinstance(obj, h5py.Dataset):
                return
            report["datasets"].append({"path": "/" + name, "shape": list(obj.shape), "dtype": str(obj.dtype),
                         "fill_values": {key: scalar(obj.attrs[key]) for key in ("_FillValue", "missing_value") if key in obj.attrs},
                         "chunks": list(obj.chunks) if obj.chunks else None, "compression": obj.compression,
                         "attributes": {key: scalar(obj.attrs[key]) for key in
                                        ("units", "description", "long_name", "flag_values", "flag_meanings") if key in obj.attrs}})
            if name.endswith("/xCoordinates"):
                paths.append("/" + name.rsplit("/", 1)[0])
        f.visititems(visit)
        for group in sorted(paths):
            if not all(f"{group}/{key}" in f for key in ("yCoordinates", "projection")):
                continue
            x, y = f[f"{group}/xCoordinates"][:], f[f"{group}/yCoordinates"][:]
            epsg = io._epsg(f[f"{group}/projection"])
            grid = {"path": group, "epsg": epsg, "shape": [len(y), len(x)],
                    "x_spacing": float(x[1]-x[0]), "y_spacing": float(y[1]-y[0]),
                    "x_extent": [float(x.min()), float(x.max())], "y_extent": [float(y.min()), float(y.max())]}
            project = Transformer.from_crs(4326, epsg, always_xy=True)
            bounds = project.transform_bounds(C.AOI["west"], C.AOI["south"], C.AOI["east"], C.AOI["north"], densify_pts=21)
            grid["box_fully_within_grid"] = bool(x.min() <= bounds[0] and x.max() >= bounds[2] and
                                                y.min() <= bounds[1] and y.max() >= bounds[3])
            try:
                r0,r1,c0,c1 = io._window(x,y,bounds,0)
                grid["box_intersects_grid"] = True
                grid["box_window"] = [int(v) for v in (r0,r1,c0,c1)]
                if f"{group}/mask" in f:
                    # Small contiguous patches avoid fetching every HDF5 chunk
                    # intersected by a sparse, scene-wide stride.
                    patches = []
                    for row in np.unique(np.linspace(r0, max(r0, r1 - 32), 3).astype(int)):
                        for col in np.unique(np.linspace(c0, max(c0, c1 - 32), 3).astype(int)):
                            patches.append(f[f"{group}/mask"][row:min(row + 32, r1), col:min(col + 32, c1)].ravel())
                    sample = np.concatenate(patches)
                    grid["mask_sampling"] = "up to nine 32x32 patches within box; not exhaustive"
                    values,counts=np.unique(sample,return_counts=True)
                    grid["box_mask_sample_counts"]={str(v):int(n) for v,n in zip(values,counts)}
            except ValueError:
                grid["box_intersects_grid"] = False
            report["grids"].append(grid)
        group = "/science/LSAR/identification"
        for key in ("trackNumber", "frameNumber", "orbitPassDirection", "zeroDopplerStartTime", "lookDirection"):
            if f"{group}/{key}" in f:
                report["identification"][key] = scalar(f[f"{group}/{key}"][()])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--json", type=Path, dest="output")
    args = parser.parse_args(argv)
    report = inspect(args.source)
    if report["synthetic"]:
        print("SYNTHETIC INPUT — not NISAR observations")
    for row in report["datasets"]:
        print(f"{row['path']} {row['shape']} {row['dtype']} fill={row['fill_values']}")
    for grid in report["grids"]:
        print(f"Grid: {grid}")
    print(f"Identification: {report['identification']}")
    if args.output:
        if report["synthetic"] and C.DEMO.resolve() not in args.output.resolve().parents:
            raise ValueError("Synthetic inspection reports must stay inside data/demo/")
        write_json(args.output, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
