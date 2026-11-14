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
    hh = rng.normal(-6, 3, (200, 200))
    occ = np.zeros_like(hh)
    occ[:40, :40] = 100
    hh[occ == 100] = rng.normal(-16, 1, (occ == 100).sum())
    t, how = K.water_threshold(hh, occ)
    lo, hi = C.WATER_DB_BOUNDS
    assert lo <= t <= hi and how.startswith("ki")


def test_kittler_illingworth_beats_otsu_on_radar_like_classes():
    # Narrow water (-16 +/- 1 dB) next to broad land (-6 +/- 3 dB), as in the real Pune NISAR crops:
    # the valley is near -13 dB. KI finds it; Otsu splits the means and cuts into land.
    rng = np.random.default_rng(3)
    v = np.concatenate([rng.normal(-16, 1, 20000), rng.normal(-6, 3, 20000)])
    t_ki, t_otsu = K.kittler_illingworth(v), K.otsu(v)
    assert -14.5 < t_ki < -12, t_ki
    assert t_otsu > t_ki + 1


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


def _tiny_gcov(path, ascending=False, mask_value=1, spacing=80.0):
    """GCOV-layout file over the study box with a bright square in the NE corner."""
    import h5py
    from pipeline.nisar_io import analysis_grid
    t, (h, w) = analysis_grid()
    nx, ny = int(w * C.GRID_RES / spacing) + 4, int(h * C.GRID_RES / spacing) + 4
    x = t.c - spacing + spacing / 2 + spacing * np.arange(nx)
    y = t.f + spacing - spacing / 2 - spacing * np.arange(ny)
    hh = np.full((ny, nx), 0.05, np.float32)
    hh[2:40, -40:-2] = 1.0           # north-east corner (row 0 = north)
    mask = np.full((ny, nx), mask_value, np.uint8)
    if ascending:
        y, hh, mask = y[::-1], hh[::-1], mask[::-1]
    with h5py.File(path, "w") as f:
        g = f.create_group("/science/LSAR/GCOV/grids/frequencyA")
        g["HHHH"], g["HVHV"], g["mask"] = hh, hh * 0.1, mask
        g["xCoordinates"], g["yCoordinates"] = x, y
        g["projection"] = np.uint32(C.GRID_EPSG)


@pytest.mark.parametrize("ascending", [False, True])
def test_crop_geometry_keeps_north_up(tmp_path, ascending):
    from pipeline import nisar_io as io
    p = tmp_path / "g.h5"
    _tiny_gcov(p, ascending=ascending)
    arrays, meta = io.read_gcov(str(p))
    hh = arrays["HHHH"]
    h, w = hh.shape
    rows, cols = np.nonzero(np.nan_to_num(hh) > 0.5)
    assert rows.size > 0
    # Bright square must land in the north-east quarter: a flip would put it south or west.
    assert rows.mean() < h / 4 and cols.mean() > 3 * w / 4, (rows.mean(), cols.mean(), h, w)


def test_gcov_mask_zero_and_255_are_dropped(tmp_path):
    from pipeline import nisar_io as io
    for value in (0, 255):
        p = tmp_path / f"m{value}.h5"
        _tiny_gcov(p, mask_value=value)
        arrays, _ = io.read_gcov(str(p))
        assert np.isnan(arrays["HHHH"]).all()


def test_crosstrack_classify_statuses():
    from pipeline.crosstrack import STATUSES, classify
    ids = np.zeros((20, 20), np.int64)
    ids[2:4, 2:4] = 1        # second track has a zone here      -> confirmed
    ids[2:4, 10:12] = 2      # only one piece of evidence         -> partial
    ids[10:12, 2:4] = 3      # good data, nothing                 -> not seen
    ids[10:12, 10:12] = 4    # no second-track data               -> not covered
    z2 = np.zeros((20, 20), bool); z2[3, 3] = True
    ev = np.zeros((20, 20), bool); ev[2, 11] = True; ev[3, 3] = True
    cov = np.ones((20, 20), bool); cov[10:12, 10:12] = False
    st, size = classify(ids, 4, z2, ev, cov)
    assert [STATUSES[s] for s in st] == ["confirmed", "partial", "not seen", "not covered"]
    assert list(size) == [4, 4, 4, 4]


def test_crosstrack_chance_is_low_for_sparse_second_track():
    from pipeline.crosstrack import chance_rates
    rng = np.random.default_rng(0)
    ids = np.zeros((200, 200), np.int64)
    for i in range(1, 21):
        r, c = rng.integers(5, 195, 2)
        ids[r:r + 2, c:c + 2] = i
    z2 = ids > 0                     # second track agrees exactly at the real places...
    ev = z2.copy()
    cov = np.ones_like(z2)
    elig = np.ones_like(z2)
    counts = chance_rates(ids, 20, elig, z2, ev, cov, trials=40)
    # ...so moved 2+ km away the zones should almost never land on a second-track zone.
    assert counts[0] / counts[:3].sum() < 0.1
