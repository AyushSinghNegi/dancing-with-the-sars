"""Public context layers on the analysis grid (no login needed).

* JRC Global Surface Water occurrence (1984-2021, % of time water was seen):
  separates rivers, lakes and reservoirs that are always wet from new flooding.
* Copernicus GLO-30 DEM (30 m): elevation and slope. Floods are mapped on
  flat ground only; slide zones on steep ground only.

  python -m pipeline.ancillary

Writes data/crops/aux_jrc_occurrence.tif, aux_elevation.tif, aux_slope.tif.
"""
from __future__ import annotations

import math
import urllib.request

import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject

from . import config as C
from .nisar_io import _profile, analysis_grid

JRC_URL = ("https://storage.googleapis.com/global-surface-water/downloads2021/occurrence/"
           "occurrence_{lon}E_{lat}Nv1_4_2021.tif")
DEM_URL = ("https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N{lat:02d}_00_E{lon:03d}_00_DEM/"
           "Copernicus_DSM_COG_10_N{lat:02d}_00_E{lon:03d}_00_DEM.tif")

SOURCES = {
    "jrc": "Pekel et al. (2016) Nature 540:418-422; JRC Global Surface Water v1.4 (1984-2021), occurrence layer",
    "dem": "Copernicus GLO-30 DEM (ESA / Airbus), distributed via AWS Open Data",
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


def build():
    jrc_paths = []
    for la, lo in tiles():
        jlon, jlat = (lo // 10) * 10, (la // 10 + 1) * 10   # JRC tiles are named by top-left corner
        url = JRC_URL.format(lon=jlon, lat=jlat)
        jrc_paths.append(_download(url, C.ANCILLARY / url.rsplit("/", 1)[-1]))
    jrc_paths = sorted(set(jrc_paths))
    dem_paths = [_download(DEM_URL.format(lat=la, lon=lo), C.ANCILLARY / f"cop30_N{la}_E{lo:03d}.tif")
                 for la, lo in tiles()]

    occ = _to_grid(jrc_paths, Resampling.average, nodata=255)
    occ[occ > 100] = np.nan
    elev = _to_grid(dem_paths, Resampling.bilinear)
    slope = slope_degrees(elev)

    C.AUX.mkdir(parents=True, exist_ok=True)
    for name, arr, dtype, nod in (("aux_jrc_occurrence", occ, "uint8", 255),
                                  ("aux_slope", slope, "uint8", 255),
                                  ("aux_elevation", elev, "int16", -32768)):
        a = np.where(np.isfinite(arr), np.round(arr), nod).astype(dtype)
        with rasterio.open(C.AUX / f"{name}.tif", "w", **_profile(dtype, nod)) as d:
            d.write(a, 1)
            d.update_tags(source=SOURCES["jrc" if "jrc" in name else "dem"])
    perm = np.nanmean(occ >= C.PERMANENT_WATER_OCCURRENCE) * 100
    print(f"[ancillary] permanent water {perm:.2f}% of box; slope >= {C.SLIDE_MIN_SLOPE_DEG:.0f} deg on "
          f"{np.nanmean(slope >= C.SLIDE_MIN_SLOPE_DEG) * 100:.1f}%; elevation {np.nanmin(elev):.0f}-{np.nanmax(elev):.0f} m")


def load():
    out = {}
    for name in ("aux_jrc_occurrence", "aux_slope", "aux_elevation"):
        with rasterio.open(C.AUX / f"{name}.tif") as d:
            a = d.read(1).astype(np.float32)
            a[a == d.nodata] = np.nan
        out[name.replace("aux_", "")] = a
    return out


if __name__ == "__main__":
    build()
