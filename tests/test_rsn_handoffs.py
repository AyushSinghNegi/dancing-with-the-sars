"""Regression tests for R3-R9 hand-offs and real/demo isolation."""
import json
import tempfile
from pathlib import Path

import h5py
import numpy as np
import pytest
from rasterio.transform import from_origin

from pipeline import config as C, common as K, nisar_io as io, water, timeline, zones, validate


def test_clean_never_adds_failed_or_nodata_pixels():
    candidate = np.ones((9, 9), bool)
    candidate[4, 4] = False
    cleaned = K.clean(candidate)
    assert not cleaned[4, 4]
    assert not (cleaned & ~candidate).any()


def test_incompatible_pair_rejected_before_files_are_read():
    incompatible = C.PRIMARY['after'].replace('_4005_DHDH_', '_2000_QPDH_')
    with pytest.raises(ValueError, match='must share'):
        K.load_pair(C.PRIMARY['before'], incompatible)


def test_missing_calibration_is_not_a_made_up_number():
    with pytest.raises(ValueError, match='Not enough valid'):
        K.water_threshold(np.full((20, 20), -9.0), np.zeros((20, 20), bool))


@pytest.mark.parametrize('flip_x,flip_y', [(False, False), (True, False), (False, True), (True, True)])
def test_hdf5_coordinate_orientation_and_fill(monkeypatch, flip_x, flip_y):
    transform = from_origin(400000, 2100000, 40, 40)
    monkeypatch.setattr(io, 'analysis_grid', lambda: (transform, (8, 8)))
    x = 400020 + np.arange(8) * 40
    y = 2099980 - np.arange(8) * 40
    expected = np.arange(64, dtype='float32').reshape(8, 8) + 1
    values = expected.copy()
    values[2, 3] = -9999
    if flip_x:
        x, values = x[::-1], values[:, ::-1]
    if flip_y:
        y, values = y[::-1], values[::-1, :]
    folder = C.DEMO / 'test-fixtures'
    folder.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=folder) as temp:
        path = Path(temp) / 'grid.h5'
        with h5py.File(path, 'w') as f:
            g = f.create_group('grid')
            g['xCoordinates'], g['yCoordinates'], g['projection'] = x, y, C.GRID_EPSG
            ds = g.create_dataset('power', data=values)
            ds.attrs['_FillValue'] = -9999
        with h5py.File(path, 'r') as f:
            arrays, _ = io.read_to_grid(f, {'power': '/grid/power'}, '/grid')
        actual = arrays['power']
        assert np.isnan(actual[2, 3])
        expected[2, 3] = np.nan
        np.testing.assert_allclose(actual, expected, equal_nan=True)


def test_coherence_zero_is_valid(monkeypatch):
    # Zero is complete decorrelation, not automatically nodata.
    class DummyFile:
        attrs = {}
        def __enter__(self): return self
        def __exit__(self, *args): pass
    monkeypatch.setattr(io, 'open_h5', lambda _: DummyFile())
    monkeypatch.setattr(io, 'find_coherence', lambda _: ('/coh', '/grid', 40))
    def reader(f, layers, group, invalid):
        values = np.array([[0.0, 0.5, 1.0, -1.0, 2.0]])
        np.testing.assert_array_equal(invalid({'coherence': values}), [[False, False, False, True, True]])
        return {'coherence': values}, {}
    monkeypatch.setattr(io, 'read_to_grid', reader)
    io.read_coherence('test')


def test_synthetic_hdf5_refused_in_real_mode(monkeypatch):
    class DummyFile:
        attrs = {'SYNTHETIC': 'not NISAR data'}
        def __enter__(self): return self
        def __exit__(self, *args): pass
    monkeypatch.setattr(C, 'IS_DEMO', False)
    monkeypatch.setattr(io, 'open_h5', lambda _: DummyFile())
    for reader in (io.read_gcov, io.read_coherence):
        with pytest.raises(ValueError, match='Synthetic input'):
            reader('test')


def test_water_sensitivity_and_unknown_aux_exclusion(monkeypatch, tmp_path):
    size = (30, 30)
    before = np.full(size, -10.0)
    after = np.full(size, -17.5)
    occurrence, slope = np.zeros(size), np.zeros(size)
    occurrence[0:5, 0:5] = 100
    occurrence[10:15, 10:15] = np.nan
    pair = {'hh_before': before, 'hh_after': after, 'hv_before': before, 'hv_after': before}
    monkeypatch.setattr(K, 'load_pair', lambda: pair)
    monkeypatch.setattr(K, 'lee_db', lambda a: a)
    monkeypatch.setattr(K, 'water_threshold', lambda *a: (-18.0, 'test'))
    monkeypatch.setattr(water.ancillary, 'load', lambda: {'jrc_occurrence': occurrence, 'slope': slope})
    stats, layers = water.run(write=False)
    assert stats['new_water_sensitivity_min_km2'] == stats['new_water_km2'] == 0
    assert stats['new_water_sensitivity_max_km2'] == pytest.approx(850 * K.PIXEL_KM2)
    assert not layers['valid'][10:15, 10:15].any()


def test_timeline_excludes_mode_change_and_computes_both_pols(monkeypatch):
    primary = C.parse_granule_id(C.PRIMARY['before'])
    good = dict(primary, name='good', granule_id=C.PRIMARY['before'], quality_rule='test')
    bad = dict(good, mode='2000', name='bad', granule_id='incompatible')
    mask = np.ones((20, 20), bool)
    monkeypatch.setattr(zones, 'masks', lambda: iter([({'id': 'zone', 'name': 'Test'}, mask)]))
    monkeypatch.setattr(K, 'gcov_crops', lambda: [good, bad])
    monkeypatch.setattr(timeline.ancillary, 'load', lambda: {'jrc_occurrence': mask.astype(float), 'slope': mask.astype(float)})
    monkeypatch.setattr(K, 'water_threshold', lambda *a: (-18., 'test'))
    monkeypatch.setattr(K, 'lee_db', lambda a: a)
    monkeypatch.setattr(io, 'load_db', lambda p: np.full(mask.shape, -12. if str(p).endswith('_HH.tif') else -19.))
    monkeypatch.setattr(Path, 'exists', lambda _: True)
    captured = {}
    monkeypatch.setattr(timeline, 'write_csv', lambda p, columns, rows: captured.update({p.name: rows}))
    monkeypatch.setattr(K, 'write_json', lambda p, obj: captured.update({p.name: obj}))
    rows = timeline.run()
    assert len(rows) == 1
    assert [r['median_db'] for r in captured['timeline.csv']] == [-12., -19.]
    assert captured['water_timeline.csv'] == rows
    assert captured['timeline_status.json']['excluded'][0]['granule_id'] == 'incompatible'


def test_json_missing_numbers_are_null(tmp_path):
    path = tmp_path / 'metrics.json'
    K.write_json(path, {'value': np.float32(np.nan), 'nested': [np.inf, np.int64(2)]})
    assert json.loads(path.read_text()) == {'value': None, 'nested': [None, 2]}
    assert 'NaN' not in path.read_text()


def test_validation_possible_water_is_not_a_confirmed_hit(monkeypatch):
    shape = (8, 8)
    zero = np.zeros(shape, bool)
    layers = {'new_water': zero, 'brighter': ~zero, 'slide_zones': zero,
              'valid': ~zero, 'hh_before': np.full(shape, -10.), 'coherence': np.full(shape, 0.5)}
    monkeypatch.setattr(K, 'load_layer', lambda k: layers[k])
    monkeypatch.setattr(K, 'lonlat_to_rowcol', lambda *a: (4, 4, shape))
    monkeypatch.setattr(validate.ancillary, 'load', lambda: {'slope': np.zeros(shape)})
    event = {'geometry': {'coordinates': [73.8, 18.5]},
             'properties': {'id': 'e', 'type': 'flood', 'date': '2026-07-06', 'precision_m': 100}}
    monkeypatch.setattr(validate, 'load_events', lambda: [event])
    summary, rows = validate.run(write=False, water_usable=True)
    assert rows[0]['result'] == 'miss'
    assert summary['flood']['hits'] == 0
    assert 'hit_rate' not in summary['flood']


def test_missing_coherence_refuses_slide_detection(monkeypatch):
    from pipeline import slide_zones
    monkeypatch.setattr(K, 'load_pair', lambda: {'coherence': None})
    with pytest.raises(ValueError, match='coherence is required'):
        slide_zones.run(layers={}, write=False)


def test_complex_hdf5_fill_metadata_serializes(tmp_path):
    from pipeline.inspect_h5 import scalar
    path = tmp_path / "inspection.json"
    K.write_json(path, {"fill": scalar(np.complex64(complex(float("nan"), 0)))})
    assert json.loads(path.read_text()) == {"fill": {"real": None, "imaginary": 0.0}}


def test_real_gcov_mask_zero_and_fill_are_invalid():
    from pipeline.quality import valid_values
    result = valid_values({"mask": np.array([[0, 1, 2, 3, 255]], dtype=np.uint8)})
    np.testing.assert_array_equal(result["mask"], [[0, 1, 1, 1, 0]])


def test_gunw_subswaths_anomalies_and_water_flag():
    from pipeline.quality import gunw_valid_values
    values = np.array([[0, 1, 10, 11, 100, 101, 110, 111, 255,
                        11 | (1 << 8), 11 | (1 << 16), 11 | (1 << 24)]], dtype=np.uint32)
    np.testing.assert_array_equal(gunw_valid_values({'mask': values})['mask'],
                                  [[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]])


def test_slide_report_without_valid_coherence_is_not_a_miss(monkeypatch):
    size = (8, 8)
    layers = {'new_water': np.zeros(size, bool), 'brighter': np.zeros(size, bool),
              'slide_zones': np.zeros(size, bool), 'valid': np.ones(size, bool),
              'hh_before': np.full(size, -10.), 'coherence': np.full(size, np.nan)}
    monkeypatch.setattr(K, 'load_layer', lambda k: layers[k])
    monkeypatch.setattr(K, 'lonlat_to_rowcol', lambda *a: (4, 4, size))
    monkeypatch.setattr(validate.ancillary, 'load', lambda: {'slope': np.full(size, 25.)})
    event = {'geometry': {'coordinates': [73.8, 18.5]},
             'properties': {'id': 'e', 'type': 'landslide', 'date': '2026-07-06', 'precision_m': 100}}
    monkeypatch.setattr(validate, 'load_events', lambda: [event])
    summary, rows = validate.run(write=False, water_usable=True)
    assert rows[0]['result'] == 'not observable'
    assert summary['slide']['misses'] == 0


def test_rejected_water_classifier_does_not_score_flood_reports(monkeypatch):
    shape = (8, 8)
    yes = np.ones(shape, bool)
    layers = {'new_water': yes, 'brighter': yes, 'slide_zones': ~yes,
              'valid': yes, 'hh_before': np.full(shape, -10.), 'coherence': np.full(shape, 0.5)}
    monkeypatch.setattr(K, 'load_layer', lambda k: layers[k])
    monkeypatch.setattr(K, 'lonlat_to_rowcol', lambda *a: (4, 4, shape))
    monkeypatch.setattr(validate.ancillary, 'load', lambda: {'slope': np.zeros(shape)})
    monkeypatch.setattr(validate, 'load_events', lambda: [
        {'geometry': {'coordinates': [73.8, 18.5]},
         'properties': {'id': 'e', 'type': 'flood', 'date': '2026-07-06', 'precision_m': 500}}])
    summary, rows = validate.run(write=False, water_usable=False)
    assert rows[0]['result'] == 'not scored'
    assert summary['flood']['hits'] == summary['flood']['misses'] == 0


def test_fixed_200m_match_does_not_expand_primary_hit_to_report_precision(monkeypatch):
    shape = (20, 20)
    candidate = np.zeros(shape, bool)
    candidate[10, 2] = True  # 320m from event; inside 500m report precision
    layers = {'new_water': candidate, 'brighter': ~candidate, 'slide_zones': candidate,
              'valid': np.ones(shape, bool), 'hh_before': np.full(shape, -10.), 'coherence': np.full(shape, .5)}
    monkeypatch.setattr(K, 'load_layer', lambda k: layers[k])
    monkeypatch.setattr(K, 'lonlat_to_rowcol', lambda *a: (10, 10, shape))
    monkeypatch.setattr(validate.ancillary, 'load', lambda: {'slope': np.zeros(shape)})
    monkeypatch.setattr(validate, 'load_events', lambda: [
        {'geometry': {'coordinates': [73.8, 18.5]},
         'properties': {'id': 'e', 'type': 'flood', 'date': '2026-07-06', 'precision_m': 500}}])
    _, rows = validate.run(write=False, water_usable=True)
    assert rows[0]['result'] == 'miss'
    assert rows[0]['precision_aware_result'] == 'hit'
    assert rows[0]['distance_m'] == 320
