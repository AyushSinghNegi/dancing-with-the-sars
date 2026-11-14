"""Fast checks for the pipeline's core rules. Run: python -m pytest -q"""
import numpy as np
import pytest

from pipeline import common as K
from pipeline import config as C


def test_parse_gcov_and_gunw_names():
    g = C.parse_granule_id(C.PRIMARY["before"])
    assert (g["product"], g["track"], g["mode"], g["pol"], g["date"]) == ("GCOV", "034", "4005", "DHDH", "2026-06-28")
    u = C.parse_granule_id(C.PRIMARY["pair"])
    assert (u["product"], u["date"], u["date2"]) == ("GUNW", "2026-06-28", "2026-07-10")


def test_primary_pair_is_same_mode():
    assert C.same_mode(C.find(C.PRIMARY["before"]), C.find(C.PRIMARY["after"]))


def test_quad_pol_dates_are_not_same_mode():
    cands = [g for g in C.load_candidates() if g.product == "GCOV" and g.track == "034"]
    qp = [g for g in cands if g.pol == "QPDH"]
    assert qp, "expected quad-pol dates after the late-August mode change"
    assert not C.same_mode(C.find(C.PRIMARY["before"]), qp[0])


def test_otsu_splits_two_populations():
    rng = np.random.default_rng(0)
    v = np.concatenate([rng.normal(-22, 1, 5000), rng.normal(-9, 1.5, 5000)])
    assert -18 < K.otsu(v) < -13


def test_water_threshold_is_clipped_and_reported():
    rng = np.random.default_rng(1)
    hh = rng.normal(-9, 1, (200, 200))
    perm = np.zeros_like(hh, bool)
    perm[:40, :40] = True
    hh[perm] = rng.normal(-22, 1, perm.sum())
    t, how = K.water_threshold(hh, perm)
    lo, hi = C.WATER_DB_BOUNDS
    assert lo <= t <= hi and how.startswith("otsu")


def test_clean_drops_small_patches():
    m = np.zeros((50, 50), bool)
    m[5:7, 5:7] = True      # 4 px: kept
    m[30, 30] = True        # 1 px: dropped
    out = K.clean(m)
    assert out[5:7, 5:7].all() and not out[30, 30]


def test_lee_filter_keeps_nan_and_reduces_noise():
    rng = np.random.default_rng(2)
    p = rng.gamma(4, 0.25, (100, 100)) * 0.1
    d = 10 * np.log10(p)
    d[0, 0] = np.nan
    f = K.lee_db(d)
    assert np.isnan(f[0, 0]) and np.nanstd(f) < np.nanstd(d)


def test_demo_and_real_paths_never_overlap():
    assert C.DEMO not in C.DATA.joinpath("derived").parents
    assert str(C.DEMO) != str(C.DATA / "derived")


def test_events_file_schema():
    import json
    p = C.REFERENCE / "events.geojson"
    if not p.exists():
        pytest.skip("events.geojson not added yet")
    fc = json.loads(p.read_text())
    for f in fc["features"]:
        pr = f["properties"]
        assert {"id", "type", "date", "place", "precision_m", "source_url"} <= set(pr)
        assert pr["type"] in {"flood", "waterlogging", "river_overflow", "landslide", "road_closure"}
        lon, lat = f["geometry"]["coordinates"][:2]
        assert 72 < lon < 75 and 17 < lat < 20
