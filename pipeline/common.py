"""Shared helpers: loading crops, speckle filtering, thresholds, patches and polygons."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import rasterio
from pyproj import Transformer
from rasterio import features
from scipy import ndimage as ndi
from shapely.geometry import shape as shp, mapping
from shapely.ops import transform as shp_transform

from . import config as C
from . import nisar_io as io

PIXEL_KM2 = (C.GRID_RES / 1000.0) ** 2
PIXEL_HA = C.GRID_RES ** 2 / 10_000


# ------------------------------------------------------------------ inputs
def manifest():
    p = C.CROPS / "manifest.json"
    return json.loads(p.read_text()) if p.exists() else []


def gcov_crops():
    """Available GCOV crops, oldest first: [{name, date, granule_id, mode, pol, track}]."""
    out = []
    for m in manifest():
        if m["kind"] != "GCOV" or not (C.CROPS / f"{m['name']}_HH.tif").exists():
            continue
        p = C.parse_granule_id(m["granule_id"])
        out.append({**m, **p})
    return sorted(out, key=lambda m: m["date"])


def load_pair(before_gid=None, after_gid=None, pair_gid=None):
    before_gid = before_gid or C.PRIMARY["before"]
    after_gid = after_gid or C.PRIMARY["after"]
    pair_gid = pair_gid or C.PRIMARY["pair"]
    out = {}
    for key, gid in (("before", before_gid), ("after", after_gid)):
        name = io.crop_name(gid)
        out[f"hh_{key}"] = io.load_db(C.CROPS / f"{name}_HH.tif")
        hv = C.CROPS / f"{name}_HV.tif"
        out[f"hv_{key}"] = io.load_db(hv) if hv.exists() else np.full_like(out[f"hh_{key}"], np.nan)
    coh = C.CROPS / f"{io.crop_name(pair_gid)}_COH.tif"
    out["coherence"] = io.load_unit(coh) if coh.exists() else None
    return out


# ------------------------------------------------------------------ filters
def lee_db(arr_db, size=3, looks=8.0):
    """Lee speckle filter applied in linear power, returned in dB. NaN-safe."""
    p = np.where(np.isfinite(arr_db), 10 ** (arr_db / 10), np.nan)
    valid = np.isfinite(p)
    p0 = np.where(valid, p, 0)
    w = ndi.uniform_filter(valid.astype(float), size)
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = ndi.uniform_filter(p0, size) / w
        sq = ndi.uniform_filter(p0 ** 2, size) / w
        var = np.maximum(sq - mean ** 2, 0)
        noise = (mean ** 2) / looks
        k = np.clip((var - noise) / np.maximum(var, 1e-12), 0, 1)
        out = mean + k * (p - mean)
    out[~valid] = np.nan
    return io.db(out)


def otsu(values, bins=256):
    v = values[np.isfinite(values)]
    if v.size < 100:
        return np.nan
    hist, edges = np.histogram(v, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    w0 = np.cumsum(hist)
    w1 = w0[-1] - w0
    m0 = np.cumsum(hist * centers) / np.maximum(w0, 1)
    m1 = (np.sum(hist * centers) - np.cumsum(hist * centers)) / np.maximum(w1, 1)
    between = w0 * w1 * (m0 - m1) ** 2
    # When the two populations are well separated the score is flat across the empty gap;
    # take the middle of that plateau instead of its first bin.
    best = between >= between.max() * (1 - 1e-6)
    return float(centers[best].mean())


def kittler_illingworth(values, bins=256):
    """Minimum-error threshold (Kittler & Illingworth, 1986): suited to a narrow water class next to a
    broad land class, the usual case in radar flood mapping."""
    v = values[np.isfinite(values)]
    if v.size < 100:
        return np.nan
    hist, edges = np.histogram(v, bins=bins)
    c = (edges[:-1] + edges[1:]) / 2
    p = hist / hist.sum()
    P1, M1, S1 = np.cumsum(p), np.cumsum(p * c), np.cumsum(p * c * c)
    P2, M2, S2 = 1 - P1, M1[-1] - M1, S1[-1] - S1
    with np.errstate(divide="ignore", invalid="ignore"):
        mu1, mu2 = M1 / P1, M2 / P2
        v1, v2 = S1 / P1 - mu1 ** 2, S2 / P2 - mu2 ** 2
        J = 1 + P1 * np.log(v1) + P2 * np.log(v2) - 2 * (P1 * np.log(P1) + P2 * np.log(P2))
    ok = (P1 > 1e-4) & (P2 > 1e-4) & (v1 > 0) & (v2 > 0) & np.isfinite(J)
    if not ok.any():
        return np.nan
    return float(c[np.where(ok)[0][np.argmin(J[ok])]])


def water_threshold(hh_db, occurrence, rng_seed=0):
    """Per-date water threshold, trained on the radar itself.

    Training sample: reservoir and river cores that JRC says are water at least 90% of the time, plus an
    equal number of never-water land pixels. The minimum-error (Kittler-Illingworth) threshold of that
    sample is kept inside WATER_DB_BOUNDS. Cores (not every >=50% pixel) because reservoir edges are
    exposed bed before the monsoon refills them.
    """
    rng = np.random.default_rng(rng_seed)
    occ = np.nan_to_num(occurrence)
    finite = np.isfinite(hh_db)
    w = hh_db[(occ >= C.WATER_TRAIN_OCCURRENCE) & finite]
    land_idx = np.flatnonzero((occ < 1) & finite)
    lo, hi = C.WATER_DB_BOUNDS
    if w.size < 200 or land_idx.size < 200:
        return float((lo + hi) / 2), "fallback-midpoint"
    land = hh_db.ravel()[rng.choice(land_idx, size=min(land_idx.size, w.size), replace=False)]
    t = kittler_illingworth(np.concatenate([w, land]))
    if not np.isfinite(t):
        return float((lo + hi) / 2), "fallback-midpoint"
    how = "ki-jrc-cores" if lo <= t <= hi else "ki-clipped"
    return float(np.clip(t, lo, hi)), how


def clean(mask, min_px=C.MIN_PATCH_PIXELS):
    mask = ndi.binary_closing(mask, structure=np.ones((2, 2)))
    lab, n = ndi.label(mask, structure=np.ones((3, 3)))
    if n == 0:
        return mask
    sizes = ndi.sum(mask, lab, index=np.arange(1, n + 1))
    keep = np.zeros(n + 1, bool)
    keep[1:] = sizes >= min_px
    return keep[lab]


def local_median(a, size_px=25, factor=5):
    """Fast approximate local median (downsample, median, upsample)."""
    h, w = a.shape
    hp, wp = -(-h // factor) * factor, -(-w // factor) * factor
    pad = np.pad(a, ((0, hp - h), (0, wp - w)), constant_values=np.nan)
    small = np.nanmedian(pad.reshape(hp // factor, factor, wp // factor, factor), axis=(1, 3))
    small = np.where(np.isfinite(small), small, np.nanmedian(small))
    med = ndi.median_filter(small, size=max(3, size_px // factor))
    return np.repeat(np.repeat(med, factor, 0), factor, 1)[:h, :w]


# ------------------------------------------------------------------ radar viewing geometry
def aspect_degrees(elev, res=C.GRID_RES):
    """Downhill direction of each slope, degrees clockwise from north."""
    gy, gx = np.gradient(np.nan_to_num(elev), res, res)   # rows run north to south
    return (np.degrees(np.arctan2(-gx, gy)) + 360) % 360


def radar_facing_azimuth(hh_db, slope, aspect):
    """Which way slopes face when they look brightest: they face the radar.

    Measured from the data (moderate slopes, 30-degree bins), so no assumption about the
    satellite's heading or look side is needed. Returns degrees clockwise from north.
    """
    m = (slope >= 20) & (slope < 40) & np.isfinite(hh_db)
    bins = np.arange(0, 360, 30)
    means = [np.nanmean(hh_db[m & (aspect >= b) & (aspect < b + 30)]) for b in bins]
    return float(bins[int(np.nanargmax(means))] + 15)


def layover_shadow(slope, aspect, facing_az, incidence_deg=C.INCIDENCE_DEG, margin_deg=10.0):
    """True where steep terrain is foreshortened into layover or hidden in radar shadow."""
    look = np.radians((facing_az + 180) % 360)          # direction the radar beam travels over the ground
    th, s, a = np.radians(incidence_deg), np.radians(slope), np.radians(aspect)
    cos_local = np.cos(th) * np.cos(s) - np.sin(th) * np.sin(s) * np.cos(a - look)
    local = np.degrees(np.arccos(np.clip(cos_local, -1, 1)))
    return (local < margin_deg) | (local > 90 - margin_deg)


# ------------------------------------------------------------------ geometry
def grid_to_lonlat():
    return Transformer.from_crs(C.GRID_EPSG, 4326, always_xy=True).transform


def patches_to_features(mask, props_fn, simplify_m=C.GRID_RES / 2):
    """Polygonise a mask; props_fn(region_bool) -> dict of properties for each patch."""
    transform, _ = io.analysis_grid()
    lab, n = ndi.label(mask, structure=np.ones((3, 3)))
    to_ll = grid_to_lonlat()
    feats = []
    if n == 0:
        return feats
    slices = ndi.find_objects(lab)
    for i, sl in enumerate(slices, start=1):
        sub = lab[sl] == i
        r0, c0 = sl[0].start, sl[1].start
        sub_t = transform * rasterio.Affine.translation(c0, r0)
        geoms = [shp(g) for g, v in features.shapes(sub.astype(np.uint8), mask=sub, transform=sub_t) if v == 1]
        if not geoms:
            continue
        from shapely.ops import unary_union
        g = unary_union(geoms).simplify(simplify_m)
        region = np.zeros_like(mask)
        region[sl] = sub
        props = props_fn(region)
        c = g.centroid
        lon, lat = to_ll(c.x, c.y)
        props.update({"lon": round(lon, 5), "lat": round(lat, 5)})
        feats.append({"type": "Feature", "properties": props,
                      "geometry": mapping(shp_transform(lambda x, y, z=None: to_ll(x, y), g))})
    return feats


def lonlat_to_rowcol(lon, lat):
    transform, shape = io.analysis_grid()
    x, y = Transformer.from_crs(4326, C.GRID_EPSG, always_xy=True).transform(lon, lat)
    col, row = ~transform * (x, y)
    return int(np.floor(row)), int(np.floor(col)), shape


# ------------------------------------------------------------------ outputs
def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_layer(name, arr, kind="mask"):
    """Save an analysis-grid layer as an internal .npy for later steps (not committed)."""
    d = C.DERIVED / "_layers"
    d.mkdir(parents=True, exist_ok=True)
    np.save(d / f"{name}.npy", arr)


def load_layer(name):
    p = C.DERIVED / "_layers" / f"{name}.npy"
    return np.load(p) if p.exists() else None
