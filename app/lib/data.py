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


def ver() -> str:
    """Changes whenever the pipeline output changes (a new deploy checks out new files), so cached
    reads below are refreshed instead of serving numbers from an older run."""
    d = _dir()
    files = [d / "metrics.json"] if d else []
    files += [REFERENCE / n for n in ("rainfall.csv", "events.geojson", "candidate_scenes.csv", "cloud_check.json")]
    return "|".join(f"{f.stat().st_mtime_ns}-{f.stat().st_size}" if f.exists() else "-" for f in files)


def metrics() -> dict:
    return _metrics(ver())


@st.cache_data(show_spinner=False)
def _metrics(v: str) -> dict:
    d = _dir()
    return json.loads((d / "metrics.json").read_text()) if d else {}


def bounds() -> dict:
    return _bounds(ver())


@st.cache_data(show_spinner=False)
def _bounds(v: str) -> dict:
    d = _dir()
    return json.loads((d / "bounds.json").read_text()) if d else {}


def geojson(name: str) -> dict | None:
    return _geojson(name, ver())


@st.cache_data(show_spinner=False)
def _geojson(name: str, v: str) -> dict | None:
    d = _dir()
    p = d / name if d else None
    return json.loads(p.read_text()) if p and p.exists() else None


def table(name: str) -> pd.DataFrame | None:
    return _table(name, ver())


@st.cache_data(show_spinner=False)
def _table(name: str, v: str) -> pd.DataFrame | None:
    d = _dir()
    p = d / name if d else None
    return pd.read_csv(p) if p and p.exists() else None


def rainfall() -> pd.DataFrame | None:
    return _rainfall(ver())


@st.cache_data(show_spinner=False)
def _rainfall(v: str) -> pd.DataFrame | None:
    p = REFERENCE / "rainfall.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["date"])
    return df if {"date", "precip_mm"} <= set(df.columns) and len(df) else None


def events() -> dict | None:
    return _events(ver())


@st.cache_data(show_spinner=False)
def _events(v: str) -> dict | None:
    """Reported events. Demo mode uses synthetic events so real reports are never scored against fake radar."""
    p = (ROOT / "data" / "demo" / "reference" / "events.geojson") if source()["demo"] else REFERENCE / "events.geojson"
    return json.loads(p.read_text()) if p.exists() else None


def publish_overlays() -> str | None:
    return _publish_overlays(ver())


@st.cache_resource(show_spinner=False)
def _publish_overlays(v: str) -> str | None:
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


def downloads() -> list[tuple[str, str, int]]:
    """(file name, static URL, bytes) for every download, served as plain files.

    st.download_button sends the whole file to the browser when the page loads (5.9 MB for the
    change GeoTIFF alone), so downloads are static links instead: nothing moves until clicked."""
    return _downloads(ver())


@st.cache_resource(show_spinner=False)
def _downloads(v: str) -> list[tuple[str, str, int]]:
    s = source()
    if not s["dir"]:
        return []
    d = Path(s["dir"])
    files = [d / rel for rel in metrics().get("downloads", {}).values()]
    files += [d / n for n in ("slide_zones.geojson", "new_water.geojson", "validation.csv", "water_stats.csv",
                              "crosstrack.json", "dem_check.json", "metrics.json")]
    dst = STATIC / s["key"] / "downloads"
    dst.mkdir(parents=True, exist_ok=True)
    out = []
    for f in files:
        if not f.exists():
            continue
        t = dst / f.name
        if not t.exists() or t.stat().st_size != f.stat().st_size or t.stat().st_mtime < f.stat().st_mtime:
            shutil.copy2(f, t)
        out.append((f.name, f"/app/static/layers/{s['key']}/downloads/{f.name}", f.stat().st_size))
    return out


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


def passes() -> pd.DataFrame | None:
    return _passes(ver())


@st.cache_data(show_spinner=False)
def _passes(v: str) -> pd.DataFrame | None:
    """Every NISAR GCOV pass over the study box (all tracks), from the CMR scene list."""
    p = REFERENCE / "candidate_scenes.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, dtype=str)
    df = df[(df["aoi"] == "pune") & (df["product"] == "GCOV")].copy()
    df["date"] = pd.to_datetime(df["date_reference"])
    df["orbit"] = "track " + df["track"].str.lstrip("0") + " " + df["direction"]
    return df[["date", "orbit", "track"]].drop_duplicates()


XT_LIFT_MIN = 2.0   # below this the second track agrees about as often as chance: say so
XT_SMALL_SAMPLE = 20  # fewer zones than this inside the second track's view: call it a small sample


def crosstrack() -> dict | None:
    """Second-track check summary (track 106), or None if that pair was not processed."""
    xt = value("crosstrack")
    if not xt or not xt.get("status_counts"):
        return None
    c = xt["status_counts"]
    scored = c.get("confirmed", 0) + c.get("partial", 0) + c.get("not seen", 0)
    if not scored:
        return None
    lift = xt.get("lift_confirmed")
    cov = xt.get("valid_fraction")
    return {**xt, "confirmed": c.get("confirmed", 0), "scored": scored, "lift": lift,
            "good": lift is not None and lift >= XT_LIFT_MIN, "small": scored < XT_SMALL_SAMPLE,
            "coverage": f"{cov:.0%}" if cov is not None else "part"}


def cloud_check() -> dict | None:
    return _cloud_check(ver())


@st.cache_data(show_spinner=False)
def _cloud_check(v: str) -> dict | None:
    """Urvashi's check of NASA's daily true-colour images for the storm week (content/cloud_check.md)."""
    p = REFERENCE / "cloud_check.json"
    if not p.exists():
        return None
    c = json.loads(p.read_text())
    img = ROOT / c.get("image", "")
    c["image_path"] = str(img) if img.exists() else None
    return c


def rain_peak(min_mm: float = 100.0) -> tuple[str, str] | None:
    """First and last day of the run of days with at least min_mm of rain around the wettest day."""
    r = rainfall()
    if r is None or not len(r):
        return None
    r = r.sort_values("date").reset_index(drop=True)
    k = int(r["precip_mm"].idxmax())
    if r.loc[k, "precip_mm"] < min_mm:
        return r.loc[k, "date"].strftime("%Y-%m-%d"), r.loc[k, "date"].strftime("%Y-%m-%d")
    a = b = k
    while a > 0 and r.loc[a - 1, "precip_mm"] >= min_mm:
        a -= 1
    while b < len(r) - 1 and r.loc[b + 1, "precip_mm"] >= min_mm:
        b += 1
    return r.loc[a, "date"].strftime("%Y-%m-%d"), r.loc[b, "date"].strftime("%Y-%m-%d")


def limits() -> dict:
    """Numbers for the "what radar could not see" panel, all from pipeline output or reference files."""
    val = table("validation.csv")
    out = {"flood_miss": 0, "flood_miss_built": 0, "slide_miss_gentle": 0}
    if val is not None and len(val):
        floods = val[val["type"].isin(["flood", "waterlogging", "river_overflow"]) & (val["result"] == "miss")]
        out["flood_miss"] = int(len(floods))
        out["flood_miss_built"] = int(floods["reason"].fillna("").str.startswith("dense buildings").sum())
        slides = val[(val["type"] == "landslide") & (val["result"] == "miss")]
        out["slide_miss_gentle"] = int(slides["reason"].fillna("").str.contains("gentler").sum())
    m = metrics()
    out.update(res_m=(m.get("grid") or {}).get("res_m"),
               slope_min=(m.get("thresholds") or {}).get("slide_min_slope_deg"),
               slope_max=(m.get("thresholds") or {}).get("slide_max_slope_deg"),
               hidden_share=(m.get("slides") or {}).get("layover_shadow_share_of_steep"),
               unreported=(m.get("validation") or {}).get("unreported_slide_zones"),
               zones=(m.get("slides") or {}).get("zones"), peak=rain_peak())
    return out


# ------------------------------------------------------------------ evidence, places, season
def publish_chips() -> str | None:
    return _publish_chips(ver())


@st.cache_resource(show_spinner=False)
def _publish_chips(v: str) -> str | None:
    """Copy the evidence chips (pipeline/evidence.py) into app/static so pages load them by URL."""
    s = source()
    if not s["dir"]:
        return None
    src = Path(s["dir"]) / "chips"
    if not src.exists():
        return None
    dst = STATIC / s["key"] / "chips"
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.webp"):
        t = dst / f.name
        if not t.exists() or t.stat().st_size != f.stat().st_size or t.stat().st_mtime < f.stat().st_mtime:
            shutil.copy2(f, t)
    return f"/app/static/layers/{s['key']}/chips"


def chip_url(fid: str, kind: str) -> str | None:
    base = publish_chips()
    d = _dir()
    if not base or not d or not (d / "chips" / f"{fid}_{kind}.webp").exists():
        return None
    return f"{base}/{fid}_{kind}.webp"


def zones() -> list[dict]:
    gj = geojson("slide_zones.geojson")
    return [f["properties"] for f in gj["features"]] if gj else []


def flood_patches() -> list[dict]:
    gj = geojson("new_water.geojson")
    return [f["properties"] for f in gj["features"] if f["properties"].get("kind") == "flood"] if gj else []


def water_patches() -> list[dict]:
    gj = geojson("new_water.geojson")
    return [f["properties"] for f in gj["features"]] if gj else []


def places() -> pd.DataFrame | None:
    return _places(ver())


@st.cache_data(show_spinner=False)
def _places(v: str) -> pd.DataFrame | None:
    """Villages, towns and suburbs in the box (OpenStreetMap, pipeline/gazetteer.py)."""
    p = REFERENCE / "places_osm.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, dtype={"name_mr": str}).fillna({"name_mr": ""})
    return df


def season_dates() -> list[str]:
    """Dates with an open-water overlay for the season slider, oldest first."""
    ov = bounds().get("overlays", {})
    return sorted(o["date"] for k, o in ov.items() if k.startswith("water_d") and o.get("date"))


def field_files() -> dict[str, tuple[str, int]]:
    """Field check list downloads: name -> (static url, bytes)."""
    return _field_files(ver())


@st.cache_resource(show_spinner=False)
def _field_files(v: str) -> dict[str, tuple[str, int]]:
    s = source()
    if not s["dir"]:
        return {}
    dst = STATIC / s["key"] / "downloads"
    dst.mkdir(parents=True, exist_ok=True)
    out = {}
    for ext in ("html", "kml", "csv", "geojson"):
        f = Path(s["dir"]) / f"field_list.{ext}"
        if not f.exists():
            continue
        t = dst / f.name
        if not t.exists() or t.stat().st_size != f.stat().st_size or t.stat().st_mtime < f.stat().st_mtime:
            shutil.copy2(f, t)
        out[ext] = (f"/app/static/layers/{s['key']}/downloads/{f.name}", f.stat().st_size)
    return out


def next_pass() -> tuple[str, str] | None:
    """(last pass on the main track, next expected pass from NISAR's 12-day repeat), ISO dates."""
    p = passes()
    if p is None or not len(p):
        return None
    track = metrics().get("sources", [{}])[0].get("granule_id", "").split("_")[5:6]
    if not track:
        return None
    mine = p[p["track"] == track[0]]
    if not len(mine):
        return None
    last = mine["date"].max()
    today = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize()
    nxt = last
    while nxt <= today:
        nxt = nxt + pd.Timedelta(days=12)
    return last.strftime("%Y-%m-%d"), nxt.strftime("%Y-%m-%d")


def km(lat1, lon1, lat2, lon2) -> float:
    import math
    dy = (lat2 - lat1) * 111.32
    dx = (lon2 - lon1) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)
