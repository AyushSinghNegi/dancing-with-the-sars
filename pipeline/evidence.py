"""Evidence for every finding a person might act on, and the field check list built from it.

For each likely slide zone and each flood patch this writes small NISAR image chips of that exact
spot (radar colour before and after, and coherence for slide zones), and adds to its record the
nearest reported event and how many of the independent checks it passes. Then it writes the field
check list that district teams can take outside: CSV, KML (Google Earth, phone map apps), GeoJSON and
a printable HTML page with the chips.

Nothing here changes a result: it only packages what the earlier steps found.

  python -m pipeline.evidence
Writes data/derived/chips/*.webp, field_list.csv, field_list.kml, field_list.geojson, field_list.html,
and adds "nearest_event*", "checks_*" and patch ids to slide_zones.geojson and new_water.geojson.
"""
from __future__ import annotations

import base64
import csv
import html
import json
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

from . import common as K
from . import config as C
from . import validate

HALF = 24          # chip half-width in 40 m pixels: 48 px = 1.9 km across
SCALE = 4          # each pixel drawn 4 x 4, so a chip is 192 px
EVENT_NEAR_KM = 2.0
SLIDE_COLOR = (235, 104, 52)
FLOOD_COLOR = (42, 120, 214)


def _stretch(a, lo, hi):
    return np.clip((a - lo) / (hi - lo), 0, 1)


def _channels(hh, hv):
    """Radar colour channels as on the map: red HH, green HV, blue HH/HV, in dB."""
    return [hh, hv, hh - hv]


def _rgb_pair(before, after):
    """Both dates of one chip with ONE stretch per channel (2nd to 98th percentile over both windows),
    so a change between them is real and not a change of contrast."""
    out = []
    lims = []
    for cb, ca in zip(before, after):
        v = np.concatenate([cb[np.isfinite(cb)], ca[np.isfinite(ca)]])
        lo, hi = (np.percentile(v, 2), np.percentile(v, 98)) if v.size else (0, 1)
        lims.append((lo, hi if hi > lo else lo + 1))
    for chans in (before, after):
        img = np.stack([np.nan_to_num(_stretch(c, lo, hi)) for c, (lo, hi) in zip(chans, lims)], -1)
        img[~np.isfinite(chans[0]) | ~np.isfinite(chans[1])] = (13 / 255, 27 / 255, 38 / 255)
        out.append((img * 255).astype(np.uint8))
    return out


def _gray(a, lo, hi):
    g = (np.nan_to_num(_stretch(a, lo, hi)) * 255).astype(np.uint8)
    return np.stack([g, g, g], -1)


def _window(a, r, c, fill=np.nan):
    """A (2*HALF) x (2*HALF) window centred on (r, c), padded where it runs off the box."""
    out = np.full((2 * HALF, 2 * HALF) + a.shape[2:], fill, dtype=np.float32 if a.dtype != bool else bool)
    r0, c0 = r - HALF, c - HALF
    rs, cs = slice(max(0, r0), min(a.shape[0], r0 + 2 * HALF)), slice(max(0, c0), min(a.shape[1], c0 + 2 * HALF))
    out[rs.start - r0:rs.stop - r0, cs.start - c0:cs.stop - c0] = a[rs, cs]
    return out


def _chip(rgb, mask, color):
    """Upscale a window (each 40 m pixel drawn 4 x 4, no smoothing) and ring the finding, leaving the
    pixels inside the ring as the radar saw them."""
    h, w = rgb.shape[:2]
    im = Image.fromarray(rgb, "RGB").resize((w * SCALE, h * SCALE), Image.NEAREST)
    if mask is not None and mask.any():
        rr, cc = np.nonzero(mask)
        cy, cx = (rr.mean() + 0.5) * SCALE, (cc.mean() + 0.5) * SCALE
        rad = max(20, (max(np.ptp(rr), np.ptp(cc)) + 1) * SCALE / 2 + 12)
        d = ImageDraw.Draw(im)
        d.ellipse((cx - rad - 2, cy - rad - 2, cx + rad + 2, cy + rad + 2), outline=(255, 255, 255), width=2)
        d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=color, width=3)
    return im


def _save(im, path):
    im.save(path, "WEBP", quality=82, method=6)


def _events():
    out = []
    for f in validate.load_events():
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        out.append({"id": p.get("id"), "type": p.get("type", ""), "place": p.get("place", ""),
                    "date": p.get("date", ""), "lon": lon, "lat": lat, "url": p.get("source_url", "")})
    return out


def _km(lat1, lon1, lat2, lon2):
    dy = (lat2 - lat1) * 111.32
    dx = (lon2 - lon1) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)


def _nearest(lat, lon, events, kinds=None):
    best = None
    for e in events:
        if kinds and e["type"] not in kinds:
            continue
        k = _km(lat, lon, e["lat"], e["lon"])
        if best is None or k < best[0]:
            best = (k, e)
    return best


def why_slide(p) -> list[str]:
    """Plain-language reasons, from the zone's own measurements (English; the app translates)."""
    out = [f"Steep ground: {p['slope_deg']:.0f}° on average."]
    if p.get("coherence") is not None:
        out.append(f"The ground stopped matching itself between passes: coherence {p['coherence']:.2f}, "
                   f"{p['coherence_vs_local']:.1f}× its surrounding kilometre.")
    bits = []
    if p.get("hv_change_db") is not None and p["hv_change_db"] <= -C.SLIDE_HV_DROP_DB:
        bits.append(f"HV fell {abs(p['hv_change_db']):.1f} dB (vegetation stripped)")
    if p.get("hh_change_db") is not None and p["hh_change_db"] >= C.SLIDE_HH_RISE_DB:
        bits.append(f"HH rose {p['hh_change_db']:.1f} dB (rough debris)")
    if bits:
        out.append("Radar brightness changed: " + " and ".join(bits) + ".")
    else:
        out.append("Radar brightness changed more than the rest of the scene did.")
    return out


def checks(p) -> dict:
    """The independent checks a zone can pass. None = could not be checked there."""
    t = p.get("track106")
    orbit = True if t == "confirmed" else (None if t in (None, "not covered") else False)
    dem = None if "nasadem" not in p else p["nasadem"] == "found"
    rep = p.get("nearest_event_km") is not None and p["nearest_event_km"] <= EVENT_NEAR_KM
    return {"second_orbit": orbit, "nasadem": dem, "report_nearby": rep}


def run(write=True):
    lay = {k: K.load_layer(k) for k in ("hh_before", "hh_after", "hv_before", "hv_after", "coherence",
                                        "slide_zone_ids", "flood")}
    if lay["slide_zone_ids"] is None:
        print("      no slide zones yet; skipping")
        return None
    out_dir = C.DERIVED / "chips"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.webp"):
        old.unlink()
    cb = _channels(lay["hh_before"], lay["hv_before"])
    ca = _channels(lay["hh_after"], lay["hv_after"])
    coh = lay["coherence"]
    events = _events()
    ids = lay["slide_zone_ids"]

    # ---- slide zones
    gp = C.DERIVED / "slide_zones.geojson"
    gz = json.loads(gp.read_text())
    for f in gz["features"]:
        p = f["properties"]
        i = int(p["id"][2:])
        rr, cc = np.nonzero(ids == i)
        r, c = int(round(rr.mean())), int(round(cc.mean()))
        mask = _window(ids == i, r, c, fill=False)
        b, a = _rgb_pair([_window(x, r, c) for x in cb], [_window(x, r, c) for x in ca])
        _save(_chip(b, mask, SLIDE_COLOR), out_dir / f"{p['id']}_before.webp")
        _save(_chip(a, mask, SLIDE_COLOR), out_dir / f"{p['id']}_after.webp")
        if coh is not None:
            _save(_chip(_gray(_window(coh, r, c), 0, 1), mask, SLIDE_COLOR), out_dir / f"{p['id']}_coh.webp")
        near = _nearest(p["lat"], p["lon"], events)
        if near:
            p.update(nearest_event=near[1]["id"], nearest_event_type=near[1]["type"],
                     nearest_event_place=near[1]["place"], nearest_event_km=round(near[0], 2))
        ck = checks(p)
        p["checks_passed"] = sum(v is True for v in ck.values())
        p["checks_possible"] = sum(v is not None for v in ck.values())

    # ---- flood patches (ids by size, largest first)
    wp = C.DERIVED / "new_water.geojson"
    gw = json.loads(wp.read_text())
    floods = [f for f in gw["features"] if f["properties"].get("kind") == "flood"]
    floods.sort(key=lambda f: (-f["properties"]["area_ha"], f["properties"]["lat"]))
    lab = ndi.label(lay["flood"], structure=np.ones((3, 3)))[0] if lay["flood"] is not None else None
    for k, f in enumerate(floods, start=1):
        p = f["properties"]
        p["id"] = f"FP{k:02d}"
        rc = K.lonlat_to_rowcol(p["lon"], p["lat"])
        r, c = int(rc[0]), int(rc[1])
        mask = None
        if lab is not None:
            win = _window(lab.astype(np.float32), r, c, fill=0)
            labs = [v for v in np.unique(win[HALF - 2:HALF + 3, HALF - 2:HALF + 3]) if v]
            mask = np.isin(win, labs) if labs else None
        b, a = _rgb_pair([_window(x, r, c) for x in cb], [_window(x, r, c) for x in ca])
        _save(_chip(b, mask, FLOOD_COLOR), out_dir / f"{p['id']}_before.webp")
        _save(_chip(a, mask, FLOOD_COLOR), out_dir / f"{p['id']}_after.webp")
        near = _nearest(p["lat"], p["lon"], events, kinds=validate.FLOOD_TYPES)
        if near:
            p.update(nearest_event=near[1]["id"], nearest_event_place=near[1]["place"],
                     nearest_event_km=round(near[0], 2))

    if write:
        K.write_json(gp, gz)
        K.write_json(wp, gw)
        _field_list(gz["features"], out_dir)
    n_chips = len(list(out_dir.glob("*.webp")))
    return {"zones": len(gz["features"]), "flood_patches": len(floods), "chips": n_chips,
            "chip_km": round(2 * HALF * C.GRID_RES / 1000, 2)}


# ------------------------------------------------------------------ field check list
def _maps(lat, lon):
    return f"https://www.google.com/maps/search/?api=1&query={lat:.5f},{lon:.5f}"


def _status_words(p):
    ck = checks(p)
    word = {True: "yes", False: "no", None: "not checked here"}
    orbit = word[ck["second_orbit"]] if ck["second_orbit"] is not None else "outside its view"
    dem = "kept" if ck["nasadem"] else (f"not kept ({p.get('nasadem_reason', '')})" if ck["nasadem"] is False
                                         else "not run")
    rep = (f"{p['nearest_event_place']} ({p['nearest_event_type']}), {p['nearest_event_km']:.1f} km"
           if p.get("nearest_event_km") is not None else "none")
    return orbit, dem, rep


def _rows(feats):
    rows = []
    for rank, f in enumerate(feats, start=1):
        p = f["properties"]
        orbit, dem, rep = _status_words(p)
        rows.append({"rank": rank, "zone": p["id"], "nearest_place": p.get("near") or "", "confidence": p["confidence"],
                     "score": p["score"], "lat": round(p["lat"], 5), "lon": round(p["lon"], 5),
                     "area_ha": p["area_ha"], "slope_deg": p["slope_deg"], "why": " ".join(why_slide(p)),
                     "second_nisar_orbit": orbit, "nasadem_check": dem, "nearest_report": rep,
                     "checks_passed": p.get("checks_passed", 0), "map_link": _maps(p["lat"], p["lon"])})
    return rows


def _field_list(feats, chip_dir):
    feats = sorted(feats, key=lambda f: (-f["properties"]["score"], f["properties"]["id"]))
    rows = _rows(feats)
    with open(C.DERIVED / "field_list.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    K.write_json(C.DERIVED / "field_list.geojson", {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
         "properties": {k: v for k, v in r.items() if k not in ("lat", "lon")}} for r in rows]})
    _kml(rows)
    _html(rows, chip_dir)


def _kml(rows):
    style = {"high": "ff3468eb", "medium": "ff5a8fef", "low": "ff9cb9f4"}   # aabbggrr
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
           "<name>MonsoonLens: likely slide zones to check (NISAR, 28 Jun to 10 Jul 2026)</name>",
           "<description>Leads to check on the ground, not confirmed landslides. Ranked by score. "
           "Source: NISAR L2 GCOV and GUNW (NASA/JPL-Caltech and ISRO, via ASF DAAC); "
           "https://monsoonlens.streamlit.app</description>"]
    for conf, col in style.items():
        out.append(f'<Style id="{conf}"><IconStyle><color>{col}</color><scale>1.1</scale><Icon><href>'
                   'http://maps.google.com/mapfiles/kml/shapes/caution.png</href></Icon></IconStyle></Style>')
    for r in rows:
        desc = (f"<b>Rank {r['rank']}, {r['confidence']} confidence (score {r['score']:.2f})</b><br/>"
                f"{html.escape(r['why'])}<br/>Second NISAR orbit: {r['second_nisar_orbit']}<br/>"
                f"NASADEM check: {html.escape(r['nasadem_check'])}<br/>Nearest report: "
                f"{html.escape(r['nearest_report'])}<br/><a href=\"{r['map_link']}\">Open in Google Maps</a>")
        out.append(f"<Placemark><name>{r['zone']} {html.escape(r['nearest_place'])}</name>"
                   f"<styleUrl>#{r['confidence']}</styleUrl><description><![CDATA[{desc}]]></description>"
                   f"<Point><coordinates>{r['lon']},{r['lat']},0</coordinates></Point></Placemark>")
    out.append("</Document></kml>")
    (C.DERIVED / "field_list.kml").write_text("\n".join(out), encoding="utf-8")


def _b64(p):
    return "data:image/webp;base64," + base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


def _html(rows, chip_dir):
    cards = []
    for r in rows:
        chips = "".join(
            f'<figure><img src="{_b64(chip_dir / f"{r["zone"]}_{k}.webp")}" alt="{lbl} radar image of {r["zone"]}">'
            f"<figcaption>{lbl}</figcaption></figure>"
            for k, lbl in (("before", "28 Jun"), ("after", "10 Jul"), ("coh", "Coherence")))
        cards.append(
            f'<section class="card"><header><span class="rank">{r["rank"]}</span><h2>{r["zone"]} '
            f'<small>{html.escape(r["nearest_place"])}</small></h2><span class="conf {r["confidence"]}">'
            f'{r["confidence"]} · {r["score"]:.2f}</span></header><div class="row"><div class="chips">{chips}</div>'
            f'<div class="facts"><p>{html.escape(r["why"])}</p><ul><li>Second NISAR orbit: {r["second_nisar_orbit"]}</li>'
            f'<li>NASADEM check: {html.escape(r["nasadem_check"])}</li><li>Nearest report: '
            f'{html.escape(r["nearest_report"])}</li><li>{r["lat"]:.5f}, {r["lon"]:.5f} · '
            f'<a href="{r["map_link"]}">Google Maps</a></li></ul><p class="tick">Checked on ____ by ________ · '
            f'Found: slide / no slide / could not reach</p></div></div></section>')
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MonsoonLens field check list</title>
<style>
body {{ font: 14px/1.45 'IBM Plex Sans', system-ui, sans-serif; color: #1d3346; margin: 24px auto; max-width: 980px; padding: 0 16px; }}
h1 {{ font-size: 26px; margin: 0 0 4px; }} .lede {{ color: #5d6b75; margin: 0 0 18px; }}
.card {{ border: 1px solid #d9dedd; border-radius: 10px; padding: 12px 14px; margin: 0 0 12px; break-inside: avoid; }}
header {{ display: flex; align-items: center; gap: 10px; }} header h2 {{ font-size: 18px; margin: 0; flex: 1; }}
header small {{ font-weight: 400; color: #5d6b75; }}
.rank {{ background: #1d3346; color: #fff; border-radius: 50%; width: 28px; height: 28px; display: grid; place-items: center; font-weight: 600; }}
.conf {{ font-size: 12px; padding: 2px 8px; border-radius: 99px; background: #fbe3d8; }} .conf.high {{ background: #eb6834; color: #fff; }}
.row {{ display: flex; gap: 14px; margin-top: 8px; flex-wrap: wrap; }} .chips {{ display: flex; gap: 6px; }}
figure {{ margin: 0; }} figure img {{ width: 120px; height: 120px; border-radius: 6px; display: block; }}
figcaption {{ font-size: 11px; color: #5d6b75; text-align: center; }} .facts {{ flex: 1; min-width: 260px; }}
.facts p {{ margin: 0 0 6px; }} ul {{ margin: 0; padding-left: 18px; }} .tick {{ margin-top: 8px; color: #5d6b75; font-size: 12px; }}
@media print {{ body {{ margin: 0; }} .card {{ page-break-inside: avoid; }} }}
</style></head><body>
<h1>Likely slide zones to check on the ground</h1>
<p class="lede">From NASA-ISRO NISAR radar passes on 28 June and 10 July 2026 over Pune district. {len(rows)} zones,
ranked by score. These are leads, not confirmed landslides. Each picture is 1.9 km across; the orange outline is the
zone. Radar colour: red HH, green HV, blue HH/HV. Coherence: dark means the ground changed between passes.
Made by MonsoonLens (team iGenfinity, NASA Space Apps 2026): https://monsoonlens.streamlit.app</p>
{''.join(cards)}
</body></html>"""
    (C.DERIVED / "field_list.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    print(run())
