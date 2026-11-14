"""Turn analysis layers into what the app shows (map PNGs, GeoTIFFs, bounds.json).

Map overlays are reprojected to Web Mercator (EPSG:3857) so they sit exactly
on the base map. Colours are fixed by role (validated for colour-blind
readers): new water = blue, slide zones = orange, possible water under trees
or between buildings = aqua (hatched), permanent water = pale blue.

  python -m pipeline.render
"""
from __future__ import annotations

import numpy as np
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.warp import Resampling, calculate_default_transform, reproject

from . import common as K
from . import config as C
from . import nisar_io as io

COLORS = {
    "new_water": "#2a78d6",
    "flood": "#1c5cab",
    "rise": "#6da7ec",
    "slide_zones": "#eb6834",
    "brighter": "#1baf7a",
    "permanent": "#b7d3f6",
    "receded": "#86b6ef",
}
DIVERGING = {"neg": (42, 120, 214), "mid": (240, 239, 236), "pos": (227, 73, 72)}  # blue <-> gray <-> red

OVERLAYS = {
    # name: (layer, style, legend)
    "hh_before": ("hh_before", "gray", "Radar HH, 28 Jun (dark = smooth/water, bright = rough/buildings)"),
    "hh_after": ("hh_after", "gray", "Radar HH, 10 Jul"),
    "rgb_before": (None, "rgb_before", "Radar colour, 28 Jun (red HH, green HV, blue HH/HV)"),
    "rgb_after": (None, "rgb_after", "Radar colour, 10 Jul"),
    "change": ("ratio", "diverging", "Change in HH, 28 Jun to 10 Jul (blue darker, red brighter)"),
    "new_water": ("new_water", "new_water", "New open water on 10 Jul"),
    "flood": ("flood", "flood", "Flooding: new water where JRC never recorded water"),
    "rise": ("rise", "rise", "Reservoirs and rivers rising"),
    "brighter": ("brighter", "brighter", "Possible water under trees or between buildings"),
    "permanent": ("permanent", "permanent", "Permanent water (JRC, rivers and reservoirs)"),
    "coherence": ("coherence", "coherence", "Radar coherence, 28 Jun to 10 Jul (dark = surface changed)"),
    "slide_raster": ("slide_zones", "slide_zones", "Likely slide zones"),
}


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mercator_target():
    src_t, (h, w) = io.analysis_grid()
    left, top = src_t.c, src_t.f
    right, bottom = left + w * C.GRID_RES, top - h * C.GRID_RES
    dst_t, dw, dh = calculate_default_transform(f"EPSG:{C.GRID_EPSG}", "EPSG:3857", w, h,
                                                left, bottom, right, top)
    return src_t, dst_t, (dh, dw)


def to_mercator(arr, categorical=False):
    src_t, dst_t, shape = _mercator_target()
    out = np.full(shape, np.nan, np.float32)
    reproject(arr.astype(np.float32), out, src_transform=src_t, src_crs=f"EPSG:{C.GRID_EPSG}",
              dst_transform=dst_t, dst_crs="EPSG:3857", src_nodata=np.nan, dst_nodata=np.nan,
              resampling=Resampling.nearest if categorical else Resampling.bilinear)
    return out


def latlon_bounds():
    _, dst_t, (h, w) = _mercator_target()
    t = Transformer.from_crs(3857, 4326, always_xy=True)
    west, north = t.transform(dst_t.c, dst_t.f)
    east, south = t.transform(dst_t.c + w * dst_t.a, dst_t.f + h * dst_t.e)
    return [[south, west], [north, east]]


def _stretch(a, lo, hi):
    return np.clip((a - lo) / (hi - lo), 0, 1)


def _hatch(shape, every=6):
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    return ((xx + yy) % every) < 2


def rgba_for(style, a, layers=None):
    h, w = a.shape if a is not None else layers["hh_before"].shape
    img = np.zeros((h, w, 4), np.uint8)
    if style == "gray":
        g = _stretch(a, -25, 0)
        v = np.isfinite(a)
        img[..., :3] = (np.nan_to_num(g) * 255).astype(np.uint8)[..., None]
        img[..., 3] = np.where(v, 255, 0)
    elif style in ("rgb_before", "rgb_after"):
        key = style.split("_")[1]
        hh, hv = layers[f"hh_{key}"], layers[f"hv_{key}"]
        r, g, b = _stretch(hh, -22, -2), _stretch(hv, -30, -10), _stretch(hh - hv, 0, 14)
        v = np.isfinite(hh) & np.isfinite(hv)
        img[..., 0], img[..., 1], img[..., 2] = [(np.nan_to_num(c) * 255).astype(np.uint8) for c in (r, g, b)]
        img[..., 3] = np.where(v, 255, 0)
    elif style == "diverging":
        t = np.clip(np.nan_to_num(a) / 8.0, -1, 1)
        mid, neg, pos = (np.array(DIVERGING[k], float) for k in ("mid", "neg", "pos"))
        col = np.where(t[..., None] < 0, mid + (neg - mid) * (-t)[..., None], mid + (pos - mid) * t[..., None])
        img[..., :3] = col.astype(np.uint8)
        alpha = np.clip((np.abs(np.nan_to_num(a)) - 1.5) / 3.0, 0, 1) * 220
        img[..., 3] = np.where(np.isfinite(a), alpha, 0).astype(np.uint8)
    elif style == "coherence":
        g = _stretch(a, 0, 1)
        img[..., :3] = (np.nan_to_num(g) * 255).astype(np.uint8)[..., None]
        img[..., 3] = np.where(np.isfinite(a), 255, 0)
    else:  # solid masks
        m = np.nan_to_num(a) > 0.5
        img[..., :3] = _hex(COLORS[style])
        alpha = {"permanent": 150, "brighter": 230}.get(style, 235)
        if style == "brighter":  # hatched, so "possible" never reads as the same thing as new water
            img[..., 3] = np.where(m, np.where(_hatch(m.shape), 255, 110), 0)
        else:
            img[..., 3] = np.where(m, alpha, 0)
    return img


def run(demo_flag=False):
    out_dir = C.DERIVED / "overlays"
    out_dir.mkdir(parents=True, exist_ok=True)
    names = ("hh_before", "hh_after", "hv_before", "hv_after", "ratio", "new_water", "flood", "rise", "brighter",
             "permanent", "coherence", "slide_zones")
    grid = {k: K.load_layer(k) for k in names}
    merc = {}
    for k, v in grid.items():
        if v is None:
            continue
        categorical = v.dtype == bool
        merc[k] = to_mercator(v.astype(np.float32), categorical=categorical)
    written = {}
    for name, (layer, style, legend) in OVERLAYS.items():
        if layer is not None and layer not in merc:
            continue
        if style.startswith("rgb") and not all(f"{p}_{style.split('_')[1]}" in merc for p in ("hh", "hv")):
            continue
        img = rgba_for(style, merc.get(layer) if layer else None, merc)
        continuous = style in ("gray", "coherence", "diverging") or style.startswith("rgb")
        fname = f"{name}.webp" if continuous else f"{name}.png"
        for old in out_dir.glob(f"{name}.*"):
            old.unlink()
        im = Image.fromarray(img, "RGBA")
        if continuous:  # lossy WebP with alpha: ~10x smaller than PNG for radar texture
            im.save(out_dir / fname, "WEBP", quality=80, method=6)
        else:
            im.save(out_dir / fname, optimize=True)
        written[name] = {"file": f"overlays/{fname}", "legend": legend,
                         "color": COLORS.get(style if style in COLORS else "", None)}
    # GeoTIFF downloads on the analysis grid (UTM 43N, 40 m).
    gt = C.DERIVED / "geotiff"
    gt.mkdir(exist_ok=True)
    downloads = {}
    for name, arr, kind in (("new_water", grid["new_water"], "mask"),
                            ("flooding", grid["flood"], "mask"),
                            ("possible_water_under_cover", grid["brighter"], "mask"),
                            ("slide_zones", grid["slide_zones"], "mask"),
                            ("hh_change_db", grid["ratio"], "db")):
        if arr is None:
            continue
        p = gt / f"{name}.tif"
        if kind == "mask":
            prof = io._profile("uint8", 255)
            with rasterio.open(p, "w", **prof) as d:
                d.write(arr.astype(np.uint8), 1)
        else:
            io.save_db_int16(p, arr, {"layer": name})
        downloads[name] = f"geotiff/{name}.tif"
    return {"bounds_latlon": latlon_bounds(), "overlays": written, "downloads": downloads}
