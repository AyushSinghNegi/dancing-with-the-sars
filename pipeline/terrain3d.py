"""Files for the app's 3D view: the study box as a relief model with the findings painted on it.

Writes, in data/derived/overlays/:
  terrain_dem.png      elevation, Terrarium-encoded (height = R*256 + G + B/256 - 32768 m), 1025 x 1025, EPSG:4326
  terrain_relief.webp  shaded relief in monsoon greens + rivers, reservoirs, flooding and slide zones
  terrain_radar.webp   NISAR HH radar of the "after" date + the same findings
and adds a "terrain" entry (bounds, elevation range) to bounds.json.

Elevation is Copernicus GLO-30 on the analysis grid (data/crops/aux_elevation.tif). Every file is on the AOI box in
plain longitude/latitude, which is how deck.gl's TerrainLayer lays a single image over its bounds.

  python -m pipeline.terrain3d
"""
from __future__ import annotations

import json

import numpy as np
import rasterio
from PIL import Image
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject
from scipy import ndimage

from . import common as K
from . import config as C
from . import nisar_io as io

DEM_SIZE = 1024          # a power of two: the browser adds the extra edge row it needs for the fast "martini" mesh
TEX_SIZE = 2048
COL = {"permanent": "#b7d3f6", "rise": "#3d8ef0", "new_water": "#3d8ef0", "flood": "#2f6fd0", "slide": "#f0743a"}


def _hex(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def _box():
    return C.AOI["west"], C.AOI["south"], C.AOI["east"], C.AOI["north"]


def _to_lonlat(arr, size, categorical=False):
    src_t, _ = io.analysis_grid()
    w, s, e, n = _box()
    out = np.full((size, size), np.nan, np.float32)
    reproject(arr.astype(np.float32), out, src_transform=src_t, src_crs=f"EPSG:{C.GRID_EPSG}",
              dst_transform=from_bounds(w, s, e, n, size, size), dst_crs="EPSG:4326", src_nodata=np.nan,
              dst_nodata=np.nan, resampling=Resampling.nearest if categorical else Resampling.bilinear)
    return out


def _fill(a):
    """Fill gaps with the nearest valid value, so the model has no holes or cliffs."""
    bad = ~np.isfinite(a)
    if bad.any():
        idx = ndimage.distance_transform_edt(bad, return_distances=False, return_indices=True)
        a = a[tuple(idx)]
    return a


def _hillshade(dem, res, az=315.0, alt=40.0, z=1.6):
    dy, dx = np.gradient(dem * z, res)
    slope = np.arctan(np.hypot(dx, dy))
    aspect = np.arctan2(-dx, dy)
    a, l = np.radians(360 - az + 90), np.radians(alt)
    hs = np.sin(l) * np.cos(slope) + np.cos(l) * np.sin(slope) * np.cos(a - aspect)
    return np.clip(hs, 0, 1)


def _paint(base, mask, color, alpha=1.0, grow=0):
    if mask is None:
        return base
    m = np.nan_to_num(mask) > 0.5
    if grow:
        m = ndimage.binary_dilation(m, iterations=grow)
    base[m] = base[m] * (1 - alpha) + _hex(color) * alpha
    return base


def run():
    out = C.DERIVED / "overlays"
    out.mkdir(parents=True, exist_ok=True)
    with rasterio.open(C.AUX / "aux_elevation.tif") as r:
        dem_utm = r.read(1).astype(np.float32)
        if r.nodata is not None:
            dem_utm[dem_utm == r.nodata] = np.nan
    h, w = io.analysis_grid()[1]
    if dem_utm.shape != (h, w):          # the elevation crop is on the analysis grid; refuse anything else
        raise ValueError(f"aux_elevation.tif is {dem_utm.shape}, analysis grid is {(h, w)}")

    # ---- elevation, Terrarium-encoded
    dem = _fill(_to_lonlat(dem_utm, DEM_SIZE))
    v = dem + 32768.0
    rgb = np.stack([np.floor(v / 256), np.floor(v % 256), np.floor((v - np.floor(v)) * 256)], -1)
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8), "RGB").save(out / "terrain_dem.png", optimize=True)

    # ---- shared pieces of both textures
    hs = _fill(_to_lonlat(_hillshade(np.nan_to_num(dem_utm, nan=float(np.nanmedian(dem_utm))), C.GRID_RES), TEX_SIZE))
    elev = _fill(_to_lonlat(dem_utm, TEX_SIZE))
    lay = {k: K.load_layer(k) for k in ("permanent", "rise", "new_water", "flood", "slide_zones", "hh_after")}
    m = {k: (_to_lonlat(v_, TEX_SIZE, categorical=True) if v_ is not None and k != "hh_after" else None)
         for k, v_ in lay.items()}

    def findings(img, with_permanent=True):
        if with_permanent:
            img = _paint(img, m["permanent"], COL["permanent"], 0.92)
        img = _paint(img, m["new_water"], COL["new_water"], 1.0, grow=1)
        img = _paint(img, m["rise"], COL["rise"], 1.0, grow=1)
        img = _paint(img, m["flood"], "#ffffff", 1.0, grow=2)               # white halo: flooding on dry land
        img = _paint(img, m["flood"], COL["flood"], 1.0, grow=1)
        img = _paint(img, m["slide_zones"], "#ffffff", 1.0, grow=2)       # white halo so small zones read
        img = _paint(img, m["slide_zones"], COL["slide"], 1.0, grow=1)
        return img

    # relief: monsoon greens by height, shaded from the north-west
    stops = np.array([300, 600, 800, 1000, 1400], np.float32)
    cols = np.array([_hex(c) for c in ("#b8c98f", "#a4bd7f", "#82a566", "#668d55", "#55784a")])
    t = np.clip(elev, stops[0], stops[-1])
    tint = np.stack([np.interp(t, stops, cols[:, i]) for i in range(3)], -1)
    shade = (0.45 + 0.75 * hs)[..., None]
    relief = findings(np.clip(tint * shade, 0, 255))
    Image.fromarray(relief.astype(np.uint8), "RGB").save(out / "terrain_relief.webp", quality=86, method=6)

    # radar: NISAR HH after, cool-tinted, with the findings on top (water is already dark in radar)
    hh = _to_lonlat(lay["hh_after"], TEX_SIZE) if lay["hh_after"] is not None else None
    if hh is not None:
        lo, hi = np.nanpercentile(hh, (2, 99.5))
        g = np.clip((_fill(hh) - lo) / (hi - lo), 0, 1) ** 0.9
        radar = g[..., None] * np.array([215, 228, 242], np.float32) + np.array([10, 14, 24], np.float32)
        radar = findings(radar, with_permanent=False)
        Image.fromarray(np.clip(radar, 0, 255).astype(np.uint8), "RGB").save(out / "terrain_radar.webp",
                                                                              quality=86, method=6)

    w_, s_, e_, n_ = _box()
    meta = {"dem": "overlays/terrain_dem.png", "relief": "overlays/terrain_relief.webp",
            "radar": "overlays/terrain_radar.webp" if hh is not None else None,
            "bounds": [w_, s_, e_, n_], "size": DEM_SIZE,
            "min_m": float(np.nanmin(dem)), "max_m": float(np.nanmax(dem)),
            "source": "Copernicus GLO-30 DEM (ESA), on the analysis grid"}
    bp = C.DERIVED / "bounds.json"
    b = json.loads(bp.read_text()) if bp.exists() else {}
    b["terrain"] = meta
    bp.write_text(json.dumps(b, indent=1))
    print(f"terrain3d: elevation {meta['min_m']:.0f} to {meta['max_m']:.0f} m, textures {TEX_SIZE}px")
    return meta


if __name__ == "__main__":
    run()
