"""JRC permanent water and NASADEM elevation/slope on the common analysis grid.

python -m pipeline.ancillary --nasadem-only
python -m pipeline.ancillary   # rebuild both JRC and NASADEM, Earthdata required
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from zipfile import ZipFile
import urllib.request

import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject

from . import config as C
from .nisar_io import _profile, analysis_grid

JRC_URL = ("https://storage.googleapis.com/global-surface-water/downloads2021/occurrence/"
           "occurrence_{lon}E_{lat}Nv1_4_2021.tif")

SOURCES = {
    "jrc": "Pekel et al. (2016) Nature 540:418-422; JRC Global Surface Water v1.4 (1984-2021), occurrence layer",
    "dem": "NASADEM_HGT.001, NASA/USGS; doi:10.5067/MEASURES/NASADEM/NASADEM_HGT.001",
}


def _download(url: str, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    print(f"[ancillary] downloading {url.rsplit('/', 1)[-1]}", flush=True)
    tmp = dest.with_suffix(".part")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(dest)
    return dest


def _to_grid(paths, resampling, dtype=np.float32, nodata=None):
    transform, shape = analysis_grid()
    out = np.full(shape, np.nan, dtype=np.float32)
    for p in paths:
        with rasterio.open(p) as src:
            tmp = np.full(shape, np.nan, dtype=np.float32)
            reproject(rasterio.band(src, 1), tmp, src_nodata=nodata if nodata is not None else src.nodata,
                      dst_transform=transform, dst_crs=f"EPSG:{C.GRID_EPSG}", dst_nodata=np.nan,
                      resampling=resampling)
            fill = np.isnan(out) & np.isfinite(tmp)
            out[fill] = tmp[fill]
    return out


def tiles():
    lats = range(math.floor(C.AOI["south"]), math.floor(C.AOI["north"] - 1e-9) + 1)
    lons = range(math.floor(C.AOI["west"]), math.floor(C.AOI["east"] - 1e-9) + 1)
    return [(la, lo) for la in lats for lo in lons]


def slope_degrees(elev, res=C.GRID_RES):
    gy, gx = np.gradient(elev, res, res)
    return np.degrees(np.arctan(np.hypot(gx, gy)))


def build_nasadem():
    import earthaccess
    root = C.ANCILLARY / "nasadem"
    root.mkdir(parents=True, exist_ok=True)
    paths = sorted(root.glob("*.hgt"))
    if len(paths) < len(tiles()):
        auth = earthaccess.login(strategy="netrc", persist=False)
        if not auth.authenticated:
            raise RuntimeError("Earthdata authentication required for NASADEM")
        results = earthaccess.search_data(short_name="NASADEM_HGT", bounding_box=(
            C.AOI["west"], C.AOI["south"], C.AOI["east"], C.AOI["north"]))
        archives = earthaccess.download(results, root, threads=2, show_progress=False)
        for archive in archives:
            with ZipFile(archive) as zipped:
                for name in zipped.namelist():
                    if name.lower().endswith(".hgt"):
                        if Path(name).name != name:
                            raise ValueError("Unexpected NASADEM archive path")
                        zipped.extract(name, root)
        paths = sorted(root.glob("*.hgt"))
    elev = _to_grid(paths, Resampling.bilinear, nodata=-32768)
    if not np.isfinite(elev).any():
        raise ValueError("NASADEM tiles have no coverage of the analysis grid")
    C.AUX.mkdir(parents=True, exist_ok=True)
    for name, arr, units in (("elevation", elev, "m"), ("slope", slope_degrees(elev), "degrees")):
        with rasterio.open(C.AUX / f"aux_nasadem_{name}.tif", "w", **_profile("float32", np.nan)) as dst:
            dst.write(arr.astype("float32"), 1)
            dst.update_tags(source=SOURCES["dem"], units=units,
                            method="bilinear elevation to 40m UTM grid; central-difference gradient")
    (C.AUX / "nasadem_provenance.json").write_text(json.dumps({
        "source": SOURCES["dem"], "tiles": [p.name for p in paths],
        "grid_epsg": C.GRID_EPSG, "grid_res_m": C.GRID_RES,
        "finite_fraction": float(np.isfinite(elev).mean()),
        "slope_method": "degrees(arctan(hypot(dz/dx,dz/dy))); 40m central differences"
    }, indent=2) + "\n")
    return elev


def build():
    jrc_paths = []
    for la, lo in tiles():
        url = JRC_URL.format(lon=(lo // 10) * 10, lat=(la // 10 + 1) * 10)
        jrc_paths.append(_download(url, C.ANCILLARY / url.rsplit("/", 1)[-1]))
    occ = _to_grid(sorted(set(jrc_paths)), Resampling.average, nodata=255)
    occ[occ > 100] = np.nan
    C.AUX.mkdir(parents=True, exist_ok=True)
    with rasterio.open(C.AUX / "aux_jrc_occurrence.tif", "w", **_profile("uint8", 255)) as dst:
        dst.write(np.where(np.isfinite(occ), np.round(occ), 255).astype("uint8"), 1)
        dst.update_tags(source=SOURCES["jrc"])
    build_nasadem()


def load():
    out = {}
    for name in ("jrc_occurrence", "slope", "elevation"):
        source = f"nasadem_{name}" if name in ("slope", "elevation") else name
        with rasterio.open(C.AUX / f"aux_{source}.tif") as d:
            a = d.read(1).astype(np.float32)
            a[a == d.nodata] = np.nan
        out[name] = a
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nasadem-only", action="store_true")
    args = parser.parse_args()
    build_nasadem() if args.nasadem_only else build()
