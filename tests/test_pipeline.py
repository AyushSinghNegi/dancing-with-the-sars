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


def test_dem_check_reasons_follow_the_slope_band():
    from pipeline import dem_check as D
    m = np.zeros((4, 4), bool)
    m[1:3, 1:3] = True
    flat_ok = np.zeros((4, 4), bool)
    assert D._why(m, np.full((4, 4), 50.0), flat_ok) == D.REASONS[0]
    assert D._why(m, np.full((4, 4), 10.0), flat_ok) == D.REASONS[1]
    bad = flat_ok.copy()
    bad[1, 1] = True
    assert D._why(m, np.full((4, 4), 30.0), bad) == D.REASONS[2]
    assert D._why(m, np.full((4, 4), 30.0), flat_ok) == D.REASONS[3]


def test_dem_check_output_adds_up():
    import json
    p = C.DERIVED / "dem_check.json"
    if not p.exists():
        pytest.skip("no elevation-map check in this output")
    d = json.loads(p.read_text())
    assert d["found"] + d["not_found"] == d["zones_main"]
    assert sum(d["not_found_reasons"].values()) == d["not_found"]
    assert sum(v["zones"] for v in d["by_confidence"].values()) == d["zones_main"]
    assert d["reported_slide_hits"]["nasadem"] <= d["reported_slide_hits"]["scored"]


def test_evidence_checks_and_reasons():
    from pipeline import evidence as E
    p = {"slope_deg": 32.4, "coherence": 0.2, "coherence_vs_local": 0.45, "hv_change_db": -3.1, "hh_change_db": 0.4,
         "track106": "not covered", "nasadem": "found", "nearest_event_km": 1.2}
    ck = E.checks(p)
    assert ck == {"second_orbit": None, "nasadem": True, "report_nearby": True}
    why = " ".join(E.why_slide(p))
    assert "32°" in why and "HV fell 3.1 dB" in why and "HH rose" not in why
    assert E.checks({**p, "track106": "confirmed", "nearest_event_km": 5})["second_orbit"] is True


def test_field_list_matches_zones():
    import csv
    import json
    z, f = C.DERIVED / "slide_zones.geojson", C.DERIVED / "field_list.csv"
    if not (z.exists() and f.exists()):
        pytest.skip("no field list in this output")
    zones = json.loads(z.read_text())["features"]
    rows = list(csv.DictReader(open(f, encoding="utf-8")))
    assert len(rows) == len(zones)
    assert [float(r["score"]) for r in rows] == sorted((float(r["score"]) for r in rows), reverse=True)
    assert all(r["map_link"].startswith("https://www.google.com/maps/") for r in rows)


def test_flood_chance_maths():
    from pipeline import flood_baseline as F
    assert F.chance_of_match([100, 600, 900, 2000], 800) == 0.5
    assert F.prob_at_least([0.5, 0.5], 0) == 1.0
    assert F.prob_at_least([0.5, 0.5], 1) == pytest.approx(0.75)
    assert F.prob_at_least([0.5, 0.5], 2) == pytest.approx(0.25)
    assert F.prob_at_least([0.2, 0.9], 2) == pytest.approx(0.18)
    assert F.prob_at_least([1.0, 1.0, 0.0], 3) == 0.0


def test_flood_chance_output_adds_up():
    import json
    p = C.DERIVED / "flood_baseline.json"
    if not p.exists():
        pytest.skip("no flood chance level in this output")
    d = json.loads(p.read_text())
    ev = d["events"]
    assert d["observed"] == {"matched": sum(e["matched"] for e in ev), "of": len(ev),
                             "matched_to_new_water": sum(e["matched"] and e["nearest_layer"] == "new_water" for e in ev)}
    assert all(e["matched"] == (e["distance_m"] <= e["tolerance_m"]) for e in ev)
    assert all(e["distance_m"] == min(e["nearest_new_water_m"], e["nearest_possible_water_m"]) for e in ev)
    for k, ref in d["reference"].items():
        assert ref["expected_matches"] == pytest.approx(sum(e["chance"][k] for e in ev), abs=0.02)
        shares = [s for _, s in ref["curve"]]
        assert shares == sorted(shares) and 0 <= shares[0] and shares[-1] <= 1
        assert 0 <= ref["prob_at_least_observed"] <= 1


def test_nearby_lists_what_is_in_range():
    from shapely.geometry import LineString, Point
    from pipeline import nearby as N
    zone = Point(0, 0).buffer(40)
    ways = [("road", "trunk", "Big Road", "NH1", LineString([(-500, 340), (500, 340)])),      # 300 m from the edge
            ("road", "trunk", "Big Road", "NH1", LineString([(-500, 2000), (500, 2000)])),    # same road, further
            ("road", "tertiary", "", "", LineString([(-500, -3040), (500, -3040)])),          # 3 km: out of range
            ("rail", "rail", "Main Line", "", LineString([(1540, -500), (1540, 500)]))]       # 1.5 km: out of range
    places = [{"name": "Near", "name_mr": "", "type": "village", "pt": Point(0, 1040)},
              {"name": "Far", "name_mr": "", "type": "town", "pt": Point(5040, 0)}]
    d = N.describe(zone, ways, places)
    assert [(r["ref"], r["distance_m"]) for r in d["roads"]] == [("NH1", 300)]
    assert d["railways"] == [] and d["nearest_railway"]["distance_m"] == 1500
    assert [p["name"] for p in d["places"]] == ["Near"] and d["nearest_place"]["distance_m"] == 1000
    assert N.line_label(d["nearest_road"]) == "NH1 Big Road"
    assert N.line_label({"ref": "", "name": "", "class": "tertiary"}) == "unnamed tertiary road"


def test_nearby_output_matches_zones():
    import json
    z, n = C.DERIVED / "slide_zones.geojson", C.DERIVED / "nearby.json"
    if not (z.exists() and n.exists()):
        pytest.skip("no nearby list in this output")
    zones = {f["properties"]["id"]: f["properties"] for f in json.loads(z.read_text())["features"]}
    d = json.loads(n.read_text())
    assert set(d["zones"]) == set(zones)
    assert all((v["lat"], v["lon"]) == (zones[k]["lat"], zones[k]["lon"]) for k, v in d["zones"].items())
    s = d["summary"]
    assert s["zones"] == len(zones)
    assert s["road_within"] == sum(bool(v["roads"]) for v in d["zones"].values())
    assert all(r["distance_m"] <= d["road_m"] for v in d["zones"].values() for r in v["roads"] + v["railways"])
    assert all(p["distance_m"] <= d["place_m"] for v in d["zones"].values() for p in v["places"])


def test_gazetteer_inside_box():
    import csv
    p = C.REFERENCE / "places_osm.csv"
    if not p.exists():
        pytest.skip("no gazetteer")
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    assert len(rows) > 100
    assert all(C.AOI["south"] <= float(r["lat"]) <= C.AOI["north"] and C.AOI["west"] <= float(r["lon"]) <= C.AOI["east"]
               for r in rows)
    assert any(r["name"] == "Pune" for r in rows)
