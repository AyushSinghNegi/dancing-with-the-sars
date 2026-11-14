"""SYNTHETIC NISAR-format files for development and tests. NOT REAL DATA.

Writes GCOV (two dates) and GUNW files with the same HDF5 layout as real
NISAR L2 products, over the Pune box, so the whole pipeline and app can be
built and tested before the real crops arrive. Terrain, slope and permanent
water come from the real ancillary layers; every radar value is simulated.

  MONSOONLENS_DEMO=1 python -m pipeline.synthetic      # writes data/demo/raw/*.h5

Every file carries the attribute SYNTHETIC="not NISAR data".
"""
from __future__ import annotations

import numpy as np
import h5py
from scipy import ndimage as ndi

from . import ancillary
from . import config as C
from .nisar_io import analysis_grid

SPACING = 20.0          # simulated native posting (m)
LOOKS = 4               # simulated looks at native posting
DEMO_RAW = C.DEMO / "raw"


def _upsample(a, f=2):
    return np.repeat(np.repeat(a, f, axis=0), f, axis=1)


def _blobs(rng, candidates, n, rmin, rmax, shape, elongate=1.0):
    out = np.zeros(shape, bool)
    ys, xs = np.nonzero(candidates)
    if ys.size == 0:
        return out
    pick = rng.choice(ys.size, size=min(n, ys.size), replace=False)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    for i in pick:
        cy, cx = ys[i], xs[i]
        r = rng.uniform(rmin, rmax)
        ang = rng.uniform(0, np.pi)
        y0, y1 = max(0, cy - int(r * elongate) - 2), min(shape[0], cy + int(r * elongate) + 3)
        x0, x1 = max(0, cx - int(r * elongate) - 2), min(shape[1], cx + int(r * elongate) + 3)
        dy, dx = yy[y0:y1, x0:x1] - cy, xx[y0:y1, x0:x1] - cx
        u = dx * np.cos(ang) + dy * np.sin(ang)
        v = -dx * np.sin(ang) + dy * np.cos(ang)
        out[y0:y1, x0:x1] |= (u / (r * elongate)) ** 2 + (v / r) ** 2 <= 1
    return out


def scene(seed=7):
    """Return simulated 40 m-grid truth layers built on real terrain and water."""
    rng = np.random.default_rng(seed)
    aux = ancillary.load()
    occ, slope, elev = aux["jrc_occurrence"], aux["slope"], aux["elevation"]
    shape = occ.shape
    perm = np.nan_to_num(occ) >= C.PERMANENT_WATER_OCCURRENCE
    seasonal = (np.nan_to_num(occ) > 5) & ~perm
    near_water = ndi.distance_transform_edt(~(np.nan_to_num(occ) > 5)) * C.GRID_RES < 2500
    flat = np.nan_to_num(slope, nan=90) < 2.5
    low = np.nan_to_num(elev, nan=9999) < np.nanpercentile(elev, 30)
    flood = _blobs(rng, flat & near_water & low & ~perm, 40, 3, 14, shape) & flat & ~perm
    flood |= seasonal & flat & (rng.random(shape) < 0.6)
    flooded_veg = _blobs(rng, flat & near_water & ~perm & ~flood, 15, 2, 6, shape) & ~flood
    steep = np.nan_to_num(slope) >= 25
    slides = _blobs(rng, steep, 45, 1.2, 2.5, shape, elongate=3.0) & (np.nan_to_num(slope) >= 18)
    # Pune city core (bright urban), approx. 73.86E 18.52N
    transform, _ = analysis_grid()
    from pyproj import Transformer
    ux, uy = Transformer.from_crs(4326, C.GRID_EPSG, always_xy=True).transform(73.86, 18.52)
    col, row = ~transform * (ux, uy)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    urban = ((yy - row) ** 2 + (xx - col) ** 2) * C.GRID_RES ** 2 < 7000 ** 2
    urban &= rng.random(shape) < 0.85
    texture = ndi.gaussian_filter(rng.normal(0, 1, shape), 3) * 2.0
    veg = np.clip((np.nan_to_num(elev) - 500) / 600, 0, 1)
    return dict(perm=perm, flood=flood, flooded_veg=flooded_veg, slides=slides, urban=urban,
                texture=texture, veg=veg, slope=np.nan_to_num(slope))


def _backscatter(t, after, rng):
    hh = -9.0 + t["texture"] - 1.5 * t["veg"]
    hv = -16.0 + 0.6 * t["texture"] + 2.0 * t["veg"]
    hh = np.where(t["urban"], -3.0 + 0.5 * t["texture"], hh)
    hv = np.where(t["urban"], -12.0, hv)
    water = t["perm"] | (t["flood"] if after else False)
    hh = np.where(water, -22.5 + 0.5 * t["texture"], hh)
    hv = np.where(water, -28.5, hv)
    if after:
        hh = np.where(t["flooded_veg"], hh + 5.0, hh)
        hv = np.where(t["slides"], hv - 5.0, hv)
        hh = np.where(t["slides"], hh + 2.5, hh)
        hh = hh + 0.4  # wetter soil after heavy rain: slightly brighter land
    out = []
    for layer_db in (hh, hv):
        p = _upsample(10 ** (layer_db / 10))
        out.append((p * rng.gamma(LOOKS, 1.0 / LOOKS, p.shape)).astype(np.float32))
    return out


def _coords(shape, pad_px=40):
    transform, _ = analysis_grid()
    x0, y1 = transform.c - pad_px * SPACING, transform.f + pad_px * SPACING
    ny, nx = shape[0] * 2 + 2 * pad_px, shape[1] * 2 + 2 * pad_px
    x = x0 + SPACING / 2 + SPACING * np.arange(nx)
    y = y1 - SPACING / 2 - SPACING * np.arange(ny)
    return x, y, pad_px


def _pad(a, pad, value):
    return np.pad(a, pad, constant_values=value)


def _proj(g, epsg=C.GRID_EPSG):
    d = g.create_dataset("projection", data=np.uint32(epsg))
    d.attrs["epsg_code"] = np.int32(epsg)


def write_gcov(path, hh, hv, x, y, pad, date, track="034"):
    with h5py.File(path, "w") as f:
        f.attrs["SYNTHETIC"] = "not NISAR data"
        g = f.create_group("/science/LSAR/GCOV/grids/frequencyA")
        for name, arr in (("HHHH", hh), ("HVHV", hv)):
            g.create_dataset(name, data=_pad(arr, pad, np.nan), chunks=(512, 512), compression="gzip",
                             compression_opts=1)
        mask = np.ones((len(y), len(x)), np.uint8)
        mask[:, :pad] = 255
        g.create_dataset("mask", data=mask, chunks=(512, 512), compression="gzip")
        g.create_dataset("xCoordinates", data=x)
        g.create_dataset("yCoordinates", data=y)
        g.create_dataset("xCoordinateSpacing", data=SPACING)
        g.create_dataset("yCoordinateSpacing", data=-SPACING)
        _proj(g)
        i = f.create_group("/science/LSAR/identification")
        i.create_dataset("trackNumber", data=int(track))
        i.create_dataset("zeroDopplerStartTime", data=f"{date}T13:42:39".encode())
        i.create_dataset("orbitPassDirection", data=b"Descending")


def write_gunw(path, t, x, y, pad, rng):
    coh = 0.30 + 0.15 * (1 - t["veg"]) + 0.03 * t["texture"]
    coh = np.where(t["urban"], 0.75, coh)
    coh = np.where(t["perm"] | t["flood"], 0.05, coh)
    coh = np.where(t["slides"], 0.07, coh)
    coh = np.clip(coh + rng.normal(0, 0.05, coh.shape), 0.01, 0.99).astype(np.float32)
    coh = _upsample(coh)
    with h5py.File(path, "w") as f:
        f.attrs["SYNTHETIC"] = "not NISAR data"
        base = "/science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram"
        g = f.create_group(base)
        g.create_dataset("xCoordinates", data=x)
        g.create_dataset("yCoordinates", data=y)
        _proj(g)
        h = g.create_group("HH")
        h.create_dataset("coherenceMagnitude", data=_pad(coh, pad, np.nan), chunks=(512, 512),
                         compression="gzip", compression_opts=1)
        h.create_dataset("unwrappedPhase", data=np.zeros((8, 8), np.float32))


def write_demo_events(t, rng, n_each=6):
    """SYNTHETIC test events at simulated floods/slides plus a few deliberate misses (demo only)."""
    import json
    from pyproj import Transformer
    from scipy import ndimage as ndi
    transform, _ = analysis_grid()
    to_ll = Transformer.from_crs(C.GRID_EPSG, 4326, always_xy=True).transform
    feats = []

    def add(r, c, typ, date, place):
        x, y = transform * (c + 0.5, r + 0.5)
        lon, lat = to_ll(x, y)
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [round(lon, 5), round(lat, 5)]},
                      "properties": {"id": f"D{len(feats) + 1:03d}", "type": typ, "date": date, "place": place,
                                     "precision_m": 500, "source_name": "SYNTHETIC test event",
                                     "source_url": "", "note": "Demo only; not a real report"}})
    for key, typ in (("slides", "landslide"), ("flood", "flood")):
        lab, n = ndi.label(t[key])
        centers = ndi.center_of_mass(t[key], lab, range(1, n + 1))
        for i in rng.choice(len(centers), size=min(n_each, len(centers)), replace=False):
            r, c = centers[i]
            add(int(r), int(c), typ, "2026-07-06", f"Synthetic {typ} {len(feats) + 1}")
    h, w = t["perm"].shape
    for typ, date in (("flood", "2026-07-07"), ("landslide", "2026-07-05"), ("flood", "2026-07-20")):
        add(int(rng.integers(50, h - 50)), int(rng.integers(50, w - 50)), typ, date, f"Synthetic miss ({typ})")
    out = C.DEMO / "reference" / "events.geojson"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, indent=1))


def build(seed=7):
    if not C.IS_DEMO:
        raise ValueError("Run with MONSOONLENS_DEMO=1 so synthetic files stay in data/demo/")
    rng = np.random.default_rng(seed)
    t = scene(seed)
    x, y, pad = _coords(t["perm"].shape)
    DEMO_RAW.mkdir(parents=True, exist_ok=True)
    for key, after in (("before", False), ("after", True)):
        hh, hv = _backscatter(t, after, rng)
        p = C.parse_granule_id(C.PRIMARY[key])
        write_gcov(DEMO_RAW / f"{C.PRIMARY[key]}.h5", hh, hv, x, y, pad, p["date"])
    write_gunw(DEMO_RAW / f"{C.PRIMARY['pair']}.h5", t, x, y, pad, rng)
    np.savez_compressed(C.DEMO / "truth.npz", **{k: t[k] for k in ("flood", "flooded_veg", "slides", "perm")})
    write_demo_events(t, rng)
    print(f"[synthetic] wrote 3 files to {DEMO_RAW} (SYNTHETIC, not NISAR data)")


if __name__ == "__main__":
    build()
