"""Reading NISAR GCOV and GUNW HDF5 files: local or streamed, cropped to the Pune box.

The key idea: never download a 5 GB frame to use an 80 km box. We read the
coordinate vectors (a few hundred kB), work out which rows and columns cover
the box, and read only those, in strips, multilooking to the 40 m analysis grid.
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.transform import from_origin
from rasterio.warp import Resampling, reproject

from . import config as C

GCOV_GRID = "/science/LSAR/GCOV/grids/frequencyA"


# ---------------------------------------------------------------- analysis grid
def analysis_grid(res: float = C.GRID_RES):
    """Transform and shape of the common UTM grid covering the project box."""
    t = Transformer.from_crs(4326, C.GRID_EPSG, always_xy=True)
    lons = [C.AOI["west"], C.AOI["east"], C.AOI["east"], C.AOI["west"]]
    lats = [C.AOI["south"], C.AOI["south"], C.AOI["north"], C.AOI["north"]]
    xs, ys = t.transform(lons, lats)
    x0 = math.floor(min(xs) / res) * res
    y1 = math.ceil(max(ys) / res) * res
    x1 = math.ceil(max(xs) / res) * res
    y0 = math.floor(min(ys) / res) * res
    width, height = int(round((x1 - x0) / res)), int(round((y1 - y0) / res))
    return from_origin(x0, y1, res, res), (height, width)


# ---------------------------------------------------------------- opening files
def open_h5(src: str, block_size=8 * 1024 * 1024):
    """Open a local path or an Earthdata HTTPS URL as an h5py.File.

    For URLs, authentication is the user's own: EARTHDATA_TOKEN in their
    environment, or earthaccess (reads ~/.netrc or asks for username and
    password in their terminal). Nothing is stored by this code.
    """
    if not str(src).startswith("http"):
        return h5py.File(src, "r")
    import fsspec
    token = os.environ.get("EARTHDATA_TOKEN")
    if token:
        fs = fsspec.filesystem("https", client_kwargs={"headers": {"Authorization": f"Bearer {token}"}})
    else:
        import earthaccess
        auth = earthaccess.login()  # tries env vars, then ~/.netrc, then asks in the terminal
        if not getattr(auth, "authenticated", True):
            raise PermissionError("Earthdata login failed: check your username/password at urs.earthdata.nasa.gov")
        fs = earthaccess.get_fsspec_https_session()
    fobj = fs.open(src, mode="rb", block_size=block_size, cache_type="blockcache")
    return h5py.File(fobj, "r")


def _epsg(ds) -> int:
    val = ds[()]
    if np.ndim(val):
        val = np.ravel(val)[0]
    epsg = int(val)
    if epsg <= 0 and "epsg_code" in ds.attrs:
        epsg = int(np.ravel(ds.attrs["epsg_code"])[0])
    return epsg


def find_coherence(f: h5py.File):
    """Locate the finest GUNW coherenceMagnitude layer and its coordinate vectors."""
    found = []

    def visit(name, obj):
        if isinstance(obj, h5py.Dataset) and name.endswith("coherenceMagnitude") and "frequencyA" in name:
            parts = name.split("/")
            for up in (1, 2, 3):
                g = "/".join(parts[:-up])
                if f"{g}/xCoordinates" in f and f"{g}/projection" in f:
                    x = f[f"{g}/xCoordinates"]
                    found.append(("/" + name, "/" + g, abs(float(x[1]) - float(x[0]))))
                    break
    f.visititems(visit)
    if not found:
        raise KeyError("No frequencyA coherenceMagnitude with coordinates found; run pipeline.inspect_h5")
    return sorted(found, key=lambda t: t[2])[0]


# ---------------------------------------------------------------- windowed read
def _window(x, y, bounds, pad):
    minx, miny, maxx, maxy = bounds
    cols = np.where((x >= minx - pad) & (x <= maxx + pad))[0]
    rows = np.where((y >= miny - pad) & (y <= maxy + pad))[0]
    if cols.size == 0 or rows.size == 0:
        raise ValueError("The project box is outside this file's footprint")
    return rows.min(), rows.max() + 1, cols.min(), cols.max() + 1


def _block_mean(a, k):
    h, w = (a.shape[0] // k) * k, (a.shape[1] // k) * k
    a = a[:h, :w].reshape(h // k, k, w // k, k)
    with np.errstate(invalid="ignore"):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            return np.nanmean(a, axis=(1, 3))


def _block_any(a, k):
    h, w = (a.shape[0] // k) * k, (a.shape[1] // k) * k
    return a[:h, :w].reshape(h // k, k, w // k, k).any(axis=(1, 3))


def read_to_grid(f: h5py.File, layers: dict, coord_group: str, invalid=None, strip=1024,
                 resampling=Resampling.average, value_transform=None):
    """Read named 2-D layers inside the box, multilook, and reproject to the analysis grid.

    layers: {"name": "/hdf5/path"}; values are linear (power or coherence).
    invalid: optional function(array_dict) -> bool mask of bad source pixels.
    """
    dst_transform, shape = analysis_grid()
    epsg = _epsg(f[f"{coord_group}/projection"])
    x = f[f"{coord_group}/xCoordinates"][:]
    y = f[f"{coord_group}/yCoordinates"][:]
    if len(x) < 2 or len(y) < 2:
        raise ValueError("Coordinate arrays must contain at least two cell centres")
    for axis in (x, y):
        delta = np.diff(axis)
        if not (np.all(delta > 0) or np.all(delta < 0)) or not np.allclose(delta, delta[0]):
            raise ValueError("NISAR grid coordinates must be regularly spaced and monotonic")
    dx, dy = abs(float(x[1] - x[0])), abs(float(y[1] - y[0]))
    # Box corners in the file's own projection.
    t = Transformer.from_crs(C.GRID_EPSG, epsg, always_xy=True)
    gx0, gy1 = dst_transform.c, dst_transform.f
    gx1, gy0 = gx0 + shape[1] * C.GRID_RES, gy1 - shape[0] * C.GRID_RES
    cx, cy = t.transform([gx0, gx1, gx1, gx0], [gy0, gy0, gy1, gy1])
    r0, r1, c0, c1 = _window(x, y, (min(cx), min(cy), max(cx), max(cy)), pad=4 * C.GRID_RES)
    k = max(1, int(round(C.GRID_RES / max(dx, dy))))
    r1 = r0 + ((r1 - r0) // k) * k
    c1 = c0 + ((c1 - c0) // k) * k
    out, bad_parts = {n: [] for n in layers}, []
    step = max(k, (strip // k) * k)
    for s in range(r0, r1, step):
        e = min(s + step, r1)
        block = {n: np.asarray(f[p][s:e, c0:c1], dtype=None if value_transform else np.float32) for n, p in layers.items()}
        if value_transform is not None:
            block = value_transform(block)
        bad = np.zeros_like(next(iter(block.values())), dtype=bool)
        for n, a in block.items():
            bad |= ~np.isfinite(a)
            ds = f[layers[n]]
            for key in ("_FillValue", "missing_value"):
                if key in ds.attrs:
                    for fill in np.asarray(ds.attrs[key]).ravel():
                        bad |= a == fill
        if invalid is not None:
            bad |= invalid(block, s, e, c0, c1)
        for n, a in block.items():
            a = a.copy()
            a[bad] = np.nan
            out[n].append(_block_mean(a, k))
        bad_parts.append(_block_any(bad, k))
        if f.driver == "fileobj":
            print(f"[read] native rows {e - r0}/{r1 - r0} loaded", flush=True)
    src_transform = from_origin(float(min(x[c0], x[c1 - 1])) - dx / 2,
                                float(max(y[r0], y[r1 - 1])) + dy / 2, dx * k, dy * k)
    result = {}
    for n, parts in out.items():
        src = np.vstack(parts)
        if x[1] < x[0]:
            src = src[:, ::-1]
        if y[1] > y[0]:
            src = src[::-1, :]
        dst = np.full(shape, np.nan, dtype=np.float32)
        reproject(src, dst, src_transform=src_transform, src_crs=f"EPSG:{epsg}", src_nodata=np.nan,
                  dst_transform=dst_transform, dst_crs=f"EPSG:{C.GRID_EPSG}", dst_nodata=np.nan,
                  resampling=resampling)
        result[n] = dst
    meta = {"source_epsg": epsg, "source_spacing_m": [dx, dy], "multilook": k,
            "window_rows": [int(r0), int(r1)], "window_cols": [int(c0), int(c1)]}
    return result, meta


def read_gcov(src: str):
    """HH and HV gamma0 (linear power) on the analysis grid, plus read metadata."""
    with open_h5(src) as f:
        if "SYNTHETIC" in f.attrs and not C.IS_DEMO:
            raise ValueError("Synthetic input requires MONSOONLENS_DEMO=1")
        g = GCOV_GRID
        layers = {n: f"{g}/{n}" for n in ("HHHH", "HVHV") if f"{g}/{n}" in f}
        if "HHHH" not in layers:
            raise KeyError(f"{g}/HHHH not found; run pipeline.inspect_h5 on this file")
        has_mask = f"{g}/mask" in f

        def invalid(block, s, e, c0, c1):
            bad = block["HHHH"] <= 0
            if has_mask:
                m = f[f"{g}/mask"][s:e, c0:c1]
                bad |= (m == 0) | (m == 255)  # source metadata: invalid/partially focused, or outside swath
            return bad

        arrays, meta = read_to_grid(f, layers, g, invalid=invalid)
        meta["layers"] = list(layers)
    return arrays, meta


def read_coherence(src: str):
    with open_h5(src) as f:
        if "SYNTHETIC" in f.attrs and not C.IS_DEMO:
            raise ValueError("Synthetic input requires MONSOONLENS_DEMO=1")
        path, group, spacing = find_coherence(f)
        arrays, meta = read_to_grid(f, {"coherence": path}, group,
                                    invalid=lambda b, *a: (b["coherence"] < 0) | (b["coherence"] > 1))
        meta["coherence_path"] = path
    return arrays["coherence"], meta


# ---------------------------------------------------------------- crop files
def db(power):
    with np.errstate(divide="ignore", invalid="ignore"):
        return 10.0 * np.log10(power)


def _profile(dtype, nodata):
    transform, (h, w) = analysis_grid()
    return {"driver": "GTiff", "height": h, "width": w, "count": 1, "dtype": dtype, "nodata": nodata,
            "crs": f"EPSG:{C.GRID_EPSG}", "transform": transform, "compress": "deflate",
            "predictor": 2, "tiled": True, "blockxsize": 256, "blockysize": 256}


def save_db_int16(path: Path, arr_db, tags: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    a = np.where(np.isfinite(arr_db), np.clip(np.round(arr_db * 100), -32767, 32767), -32768).astype("int16")
    with rasterio.open(path, "w", **_profile("int16", -32768)) as d:
        d.write(a, 1)
        d.update_tags(scale="0.01 dB", **{k: str(v) for k, v in tags.items()})


def save_unit_uint8(path: Path, arr, tags: dict):
    """Values 0..1 stored as 0..250; 255 = no data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    a = np.where(np.isfinite(arr), np.clip(np.round(arr * 250), 0, 250), 255).astype("uint8")
    with rasterio.open(path, "w", **_profile("uint8", 255)) as d:
        d.write(a, 1)
        d.update_tags(scale="1/250", **{k: str(v) for k, v in tags.items()})


def load_db(path: Path):
    with rasterio.open(path) as d:
        a = d.read(1).astype(np.float32)
    a[a == -32768] = np.nan
    return a / 100.0


def load_unit(path: Path):
    with rasterio.open(path) as d:
        a = d.read(1).astype(np.float32)
    a[a == 255] = np.nan
    return a / 250.0


def crop_name(gid: str) -> str:
    p = C.parse_granule_id(gid)
    if p["product"] == "GCOV":
        return f"{p['date']}_T{p['track']}_{p['mode']}_{p['pol']}"
    return f"{p['date']}_{p['date2']}_T{p['track']}_{p['mode']}"


def update_manifest(entry: dict):
    path = C.CROPS / "manifest.json"
    items = json.loads(path.read_text()) if path.exists() else []
    items = [i for i in items if i["name"] != entry["name"]] + [entry]
    path.write_text(json.dumps(sorted(items, key=lambda i: i["name"]), indent=2))


def crop_gcov(gid: str, src: str):
    arrays, meta = read_gcov(src)
    name = crop_name(gid)
    tags = {"granule_id": gid, **meta}
    save_db_int16(C.CROPS / f"{name}_HH.tif", db(arrays["HHHH"]), tags)
    if "HVHV" in arrays:
        save_db_int16(C.CROPS / f"{name}_HV.tif", db(arrays["HVHV"]), tags)
    valid = float(np.isfinite(arrays["HHHH"]).mean())
    update_manifest({"name": name, "granule_id": gid, "kind": "GCOV", "valid_fraction": round(valid, 4),
                     "created": datetime.now(timezone.utc).isoformat(timespec="seconds"), **meta})
    return name, valid


def crop_gunw(gid: str, src: str):
    coh, meta = read_coherence(src)
    name = crop_name(gid)
    save_unit_uint8(C.CROPS / f"{name}_COH.tif", coh, {"granule_id": gid, **meta})
    valid = float(np.isfinite(coh).mean())
    update_manifest({"name": name, "granule_id": gid, "kind": "GUNW", "valid_fraction": round(valid, 4),
                     "created": datetime.now(timezone.utc).isoformat(timespec="seconds"), **meta})
    return name, valid
