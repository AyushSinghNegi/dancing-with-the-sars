"""The committed app data has everything the pages need (guards against a pipeline step overwriting another's)."""
import json
from pathlib import Path

DERIVED = Path(__file__).resolve().parents[1] / "data" / "derived"


def test_bounds_has_terrain_and_its_files():
    b = json.loads((DERIVED / "bounds.json").read_text())
    t = b.get("terrain")
    assert t, "bounds.json lost its 'terrain' entry: the 3D view would disappear"
    for k in ("dem", "relief", "radar"):
        if t.get(k):
            assert (DERIVED / t[k]).exists(), t[k]
    w, s, e, n = t["bounds"]
    assert w < e and s < n


def test_metrics_and_validation_agree():
    m = json.loads((DERIVED / "metrics.json").read_text())
    v = json.loads((DERIVED / "validation_summary.json").read_text())
    assert m["validation"]["flood"]["hits"] == v["flood"]["hits"]
