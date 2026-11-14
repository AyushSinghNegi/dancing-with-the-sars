"""The app must never silently substitute synthetic results for real data."""
import importlib.util
import json
from pathlib import Path
import pytest


@pytest.fixture
def app_data(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('monsoonlens_app_data_test', Path(__file__).parents[1] / 'app/lib/data.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.source.clear()
    for key, demo in (('REAL', False), ('DEMO', True)):
        directory = tmp_path / key
        directory.mkdir()
        (directory / 'metrics.json').write_text(json.dumps({'demo': demo}))
        (directory / 'bounds.json').write_text('{}')
        monkeypatch.setattr(module, key, directory)
    yield module
    module.source.clear()


def test_no_demo_fallback(app_data, monkeypatch):
    monkeypatch.delenv('MONSOONLENS_DEMO', raising=False)
    (app_data.REAL / 'metrics.json').unlink()
    assert app_data.source() == {'dir': None, 'demo': False, 'key': None}


def test_explicit_demo_selects_only_demo(app_data, monkeypatch):
    monkeypatch.setenv('MONSOONLENS_DEMO', '1')
    assert app_data.source()['dir'] == str(app_data.DEMO)
    assert app_data.source()['demo'] is True


def test_synthetic_provenance_rejected_in_real_directory(app_data, monkeypatch):
    monkeypatch.delenv('MONSOONLENS_DEMO', raising=False)
    (app_data.REAL / 'metrics.json').write_text('{"demo": true}')
    with pytest.raises(ValueError, match='provenance'):
        app_data.source()


def test_failed_classifier_cannot_publish_a_zero_flood_claim(app_data, monkeypatch):
    monkeypatch.setattr(app_data, 'metrics', lambda: {
        'water': {'classification_usable': 0, 'new_water_km2': 0.0},
        'slides': {'zones': 0}})
    assert app_data.value('water.new_water_km2') is None
    assert app_data.overlay_url('new_water') is None
    assert app_data.value('slides.zones') == 0
