"""Everything the app reads, in one place. The app never computes science itself."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
REAL = ROOT / "data" / "derived"
DEMO = ROOT / "data" / "demo" / "derived"
REFERENCE = ROOT / "data" / "reference"
STATIC = ROOT / "app" / "static" / "layers"


def _has_results(d: Path) -> bool:
    return (d / "metrics.json").exists() and (d / "bounds.json").exists()


@st.cache_data(show_spinner=False)
def source() -> dict:
    """Pick real results if they exist, otherwise the synthetic demo (with a banner)."""
    if _has_results(REAL):
        return {"dir": str(REAL), "demo": False, "key": "real"}
    if _has_results(DEMO):
        return {"dir": str(DEMO), "demo": True, "key": "demo"}
    return {"dir": None, "demo": False, "key": None}


def _dir() -> Path | None:
    s = source()
    return Path(s["dir"]) if s["dir"] else None


@st.cache_data(show_spinner=False)
def metrics() -> dict:
    d = _dir()
    return json.loads((d / "metrics.json").read_text()) if d else {}


@st.cache_data(show_spinner=False)
def bounds() -> dict:
    d = _dir()
    return json.loads((d / "bounds.json").read_text()) if d else {}


@st.cache_data(show_spinner=False)
def geojson(name: str) -> dict | None:
    d = _dir()
    p = d / name if d else None
    return json.loads(p.read_text()) if p and p.exists() else None


@st.cache_data(show_spinner=False)
def table(name: str) -> pd.DataFrame | None:
    d = _dir()
    p = d / name if d else None
    return pd.read_csv(p) if p and p.exists() else None


@st.cache_data(show_spinner=False)
def rainfall() -> pd.DataFrame | None:
    p = REFERENCE / "rainfall.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["date"])
    return df if {"date", "precip_mm"} <= set(df.columns) and len(df) else None


@st.cache_data(show_spinner=False)
def events() -> dict | None:
    """Reported events. Demo mode uses synthetic events so real reports are never scored against fake radar."""
    p = (ROOT / "data" / "demo" / "reference" / "events.geojson") if source()["demo"] else REFERENCE / "events.geojson"
    return json.loads(p.read_text()) if p.exists() else None


@st.cache_resource(show_spinner=False)
def publish_overlays() -> str | None:
    """Copy map images into app/static so the browser loads them by URL (fast, cached)."""
    s = source()
    if not s["dir"]:
        return None
    src, dst = Path(s["dir"]) / "overlays", STATIC / s["key"]
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.*"):
        t = dst / f.name
        if not t.exists() or t.stat().st_mtime < f.stat().st_mtime or t.stat().st_size != f.stat().st_size:
            shutil.copy2(f, t)
    return f"/app/static/layers/{s['key']}"


def overlay_url(name: str) -> str | None:
    base = publish_overlays()
    o = bounds().get("overlays", {}).get(name)
    if not base or not o:
        return None
    return f"{base}/{Path(o['file']).name}"


def overlay_path(name: str) -> Path | None:
    d = _dir()
    o = bounds().get("overlays", {}).get(name)
    return (d / o["file"]) if d and o else None


def download_path(name: str) -> Path | None:
    d = _dir()
    rel = metrics().get("downloads", {}).get(name)
    return (d / rel) if d and rel else None


def value(path: str, default=None):
    """metrics() lookup by dotted path, e.g. value('water.new_water_km2')."""
    cur = metrics()
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def dates() -> tuple[str, str]:
    src = {s["role"]: s for s in metrics().get("sources", [])}
    def d(role, fallback):
        gid = src.get(role, {}).get("granule_id", "")
        parts = gid.split("_")
        return f"{parts[11][:4]}-{parts[11][4:6]}-{parts[11][6:8]}" if len(parts) > 11 else fallback
    return d("before", "2026-06-28"), d("after", "2026-07-10")


def nice_date(iso: str, year=True) -> str:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    d = f"{int(iso[8:10])} {months[int(iso[5:7]) - 1]}"
    return f"{d} {iso[:4]}" if year else d
