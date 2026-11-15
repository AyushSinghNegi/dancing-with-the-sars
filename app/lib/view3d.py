"""3D view: the study box as a relief model (Copernicus elevation, height ×2) with NISAR's findings painted on it,
3D pins for slide zones, flood patches and reported events, town names, and a guided tour that flies the camera
to each finding with a one-line explanation.

Runs deck.gl in the visitor's browser (loaded from the jsDelivr CDN, as the folium maps load Leaflet). The relief and
radar images and the elevation file are served by the app (pipeline/terrain3d.py makes them).
"""
from __future__ import annotations

import html as _html
import json

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from . import data, ui

DECK = "https://cdn.jsdelivr.net/npm/deck.gl@9.4.1/dist.min.js"
EX = 2.0            # vertical exaggeration, said on screen


def meta():
    return data.bounds().get("terrain")


@st.cache_data(show_spinner=False)
def _dem(v: str):
    m = data.bounds().get("terrain")
    p = data.overlay_path("hh_after")
    if not m or not p:
        return None
    f = p.parent.parent / m["dem"]
    if not f.exists():
        return None
    a = np.asarray(Image.open(f).convert("RGB")).astype(np.float64)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def _z(dem, m, lat, lon):
    """Height of the model's surface at a point, in the same units deck.gl draws (metres × EX, lowest point at 0)."""
    w, s, e, n = m["bounds"]
    size = dem.shape[0]
    c = int(round((lon - w) / (e - w) * (size - 1)))
    r = int(round((n - lat) / (n - s) * (size - 1)))
    if not (0 <= r < size and 0 <= c < size):
        return 0.0
    return float((dem[r, c] - m["min_m"]) * EX)


def scene():
    m, dem = meta(), _dem(data.ver())
    if not m or dem is None:
        return None
    tr = ui.tr
    z = lambda la, lo: round(_z(dem, m, la, lo), 1)
    zones = [{"id": p["id"], "p": [p["lon"], p["lat"], z(p["lat"], p["lon"])], "c": p["confidence"],
              "s": round(p.get("score") or 0, 2), "sl": round(p.get("slope_deg") or 0),
              "near": p.get("near") or ""} for p in data.zones()]
    floods = [{"id": p["id"], "p": [p["lon"], p["lat"], z(p["lat"], p["lon"])], "a": p.get("area_ha")}
              for p in data.flood_patches()]
    ev = (data.events() or {}).get("features", [])
    events = [{"id": f["properties"]["id"], "p": [*f["geometry"]["coordinates"][:2],
                                                  z(f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0])],
               "t": f["properties"].get("type", ""), "place": f["properties"].get("place", ""),
               "d": f["properties"].get("date", "")} for f in ev if f.get("geometry")
              and m["bounds"][0] <= f["geometry"]["coordinates"][0] <= m["bounds"][2]
              and m["bounds"][1] <= f["geometry"]["coordinates"][1] <= m["bounds"][3]]
    pl = data.places()
    places = []
    if pl is not None:
        for _, r in pl[pl["place"].isin(["city", "town"])].iterrows():
            places.append({"n": r["name"], "p": [r["lon"], r["lat"], z(r["lat"], r["lon"])],
                           "big": r["place"] == "city"})
    return {"m": m, "zones": zones, "floods": floods, "events": events, "places": places}


def _tour(sc):
    """Camera stops, built from the data: where each kind of finding actually is."""
    tr, met = ui.tr, data.metrics()
    w, s, e, n = sc["m"]["bounds"]
    cx, cy = (w + e) / 2, (s + n) / 2
    before, after = data.dates()
    stops = [dict(t=tr("Where this is", "हे कुठे आहे"),
                  x=tr("Pune district, Maharashtra, India: an 85 km box from the Western Ghats hills (left) to Pune "
                       "city (right). Heights are doubled so the hills read.",
                       "पुणे जिल्हा, महाराष्ट्र, भारत: पश्चिम घाटाच्या डोंगरांपासून (डावीकडे) पुणे शहरापर्यंत (उजवीकडे) ८५ "
                       "किमीचा भाग. डोंगर स्पष्ट दिसावेत म्हणून उंची दुप्पट दाखवली आहे."),
                  v=dict(longitude=cx, latitude=cy - 0.1, zoom=8.95, pitch=50, bearing=-12))]
    stops.append(dict(t=tr("The Western Ghats", "पश्चिम घाट"),
                      x=tr("Steep, forested hills where the monsoon rain falls hardest. In early July the whole area "
                           "averaged up to {r} mm of rain in a day, and slopes gave way.",
                           "मान्सूनचा पाऊस सर्वाधिक पडतो ते तीव्र उताराचे जंगली डोंगर. जुलैच्या सुरुवातीला संपूर्ण भागात "
                           "एका दिवसात सरासरी {r} मिमीपर्यंत पाऊस पडला आणि उतार ढासळले.",
                           r=_rain_peak()),
                      v=dict(longitude=73.47, latitude=18.52, zoom=10.4, pitch=64, bearing=-75)))
    big = sorted([p for p in data.water_patches() if p.get("kind") != "flood"], key=lambda p: -(p.get("area_ha") or 0))
    if big:
        b = big[0]
        stops.append(dict(t=tr("Reservoirs filled up", "धरणे भरली"),
                          x=tr("Blue edges are new water: between {b} and {a}, Pune's reservoirs and rivers grew by "
                               "{k} km².", "निळ्या कडा म्हणजे नवीन पाणी: {b} ते {a} दरम्यान पुण्याची धरणे आणि नद्या {k} "
                               "चौ. किमीने वाढल्या.", b=ui.day(before), a=ui.day(after),
                               k=ui.fmt_num(data.value("water.rise_km2") or 0)),
                          v=dict(longitude=b["lon"], latitude=b["lat"] - 0.025, zoom=11.6, pitch=58, bearing=20)))
    hz = [p for p in sc["zones"] if p["c"] == "high"] or sc["zones"]
    if hz:
        lon = float(np.median([p["p"][0] for p in hz])); lat = float(np.median([p["p"][1] for p in hz]))
        stops.append(dict(t=tr("Likely slide zones", "संभाव्य भूस्खलन क्षेत्रे"),
                          x=tr("Orange pins: {n} places on steep slopes where the ground changed between passes. Tall "
                               "pins are the {h} high-confidence ones. Leads to check, not confirmed landslides.",
                               "नारिंगी खुणा: दोन निरीक्षणांदरम्यान जमीन बदललेल्या तीव्र उतारावरील {n} जागा. उंच खुणा {h} "
                               "उच्च खात्रीच्या आहेत. या तपासण्याच्या जागा आहेत, निश्चित भूस्खलने नाहीत.",
                               n=len(sc["zones"]), h=sum(p["c"] == "high" for p in sc["zones"])),
                          v=dict(longitude=lon, latitude=lat + 0.02, zoom=10.7, pitch=56, bearing=165)))
    if sc["floods"]:
        fl = sorted(data.flood_patches(), key=lambda p: -(p.get("area_ha") or 0))[0]
        stops.append(dict(t=tr("Flooded land", "पुराखालची जमीन"),
                          x=tr("Dark-blue pins: water still standing on {a} where no water was recorded from 1984 to "
                               "2021, {k} km² in all.", "गडद निळ्या खुणा: १९८४ ते २०२१ मध्ये कधीही पाणी नोंदले न गेलेल्या "
                               "ठिकाणी {a} रोजी साचलेले पाणी, एकूण {k} चौ. किमी.", a=ui.day(after),
                               k=ui.fmt_num(data.value("water.flood_km2") or 0, 2)),
                          v=dict(longitude=fl["lon"] - 0.03, latitude=fl["lat"] - 0.05, zoom=11.2, pitch=58, bearing=-20)))
    pune = [p for p in sc["places"] if p["n"] == "Pune"]
    if pune:
        val = met.get("validation", {}).get("flood", {})
        stops.append(dict(t=tr("Pune city", "पुणे शहर"),
                          x=tr("White pins are floods and landslides people reported. Radar sees water between buildings "
                               "poorly, so many city reports were missed. Overall, {h} of {o} reported floods it could "
                               "observe had a detection nearby.",
                               "पांढऱ्या खुणा म्हणजे लोकांनी नोंदवलेले पूर आणि भूस्खलने. इमारतींमधले पाणी रडारला नीट दिसत "
                               "नाही, म्हणून शहरातील अनेक नोंदी सुटल्या. एकूण, रडारला दिसू शकणाऱ्या {o} पैकी {h} पुरांजवळ "
                               "काहीतरी सापडले.", h=val.get("hits", 0), o=val.get("observable", 0)),
                          v=dict(longitude=pune[0]["p"][0], latitude=pune[0]["p"][1] - 0.07, zoom=10.9, pitch=55,
                                 bearing=15)))
    stops.append(dict(t=tr("Your turn", "आता तुम्ही पाहा"),
                      x=tr("Drag to turn the model, scroll or pinch to zoom, and point at a pin for details.",
                           "मॉडेल फिरवण्यासाठी ओढा, झूमसाठी स्क्रोल किंवा पिंच करा आणि माहितीसाठी खुणेवर पॉइंटर न्या."),
                      v=dict(longitude=cx, latitude=cy - 0.1, zoom=9.4, pitch=45, bearing=8)))
    return stops


def _rain_peak():
    r = data.rainfall()
    if r is None or "precip_mm" not in r:
        return "?"
    return f"{float(r['precip_mm'].max()):.0f}"


def render(height=600, tour=True, key="v3d", start=None):
    """Draw the 3D view. Returns False when the terrain files are missing (the caller shows the flat map)."""
    sc = scene()
    if not sc:
        return False
    tr = ui.tr
    base = data.publish_overlays()
    m = sc["m"]
    url = lambda f: f"{base}/{f.split('/')[-1]}" if f else None
    stops = _tour(sc)
    if start is not None:
        stops[0]["v"] = start
    L = {
        "relief": tr("Relief", "उठाव"), "radar": tr("Radar", "रडार"),
        "zones": tr("Slide zones", "भूस्खलन क्षेत्रे"), "floods": tr("Flooding", "पूर"),
        "events": tr("Reported", "नोंदवलेले"), "names": tr("Names", "नावे"),
        "next": tr("Next", "पुढे"), "back": tr("Back", "मागे"), "start": tr("Take the tour", "फेरफटका सुरू करा"),
        "play": tr("Play", "चालू करा"), "pause": tr("Pause", "थांबवा"),
        "lg_old": tr("Water before the storm", "वादळापूर्वीचे पाणी"), "lg_new": tr("New water by {a}", "{a} पर्यंत नवीन पाणी"),
        "lg_flood": tr("Flooding on dry land", "कोरड्या जमिनीवरील पूर"), "lg_zone": tr("Likely slide zone", "संभाव्य भूस्खलन क्षेत्र"),
        "lg_event": tr("Reported flood or landslide", "नोंदवलेला पूर किंवा भूस्खलन"),
        "note": tr("Heights ×2. Elevation: Copernicus GLO-30. Radar: NISAR.", "उंची ×२. उंची: Copernicus GLO-30. रडार: निसार."),
        "where": tr("Pune district, India", "पुणे जिल्हा, भारत"),
        "zone": tr("Likely slide zone", "संभाव्य भूस्खलन क्षेत्र"), "slope": tr("slope", "उतार"), "score": tr("score", "गुण"),
        "high": tr("high confidence", "उच्च खात्री"), "medium": tr("medium confidence", "मध्यम खात्री"),
        "low": tr("low confidence", "कमी खात्री"), "near": tr("near", "जवळ"),
        "flood": tr("Flood patch", "पुराची जागा"), "ha": tr("ha of water", "हे. पाणी"),
        "event": tr("Reported", "नोंदवलेले"), "landslide": tr("landslide", "भूस्खलन"), "floodw": tr("flood", "पूर"),
        "nogl": tr("The 3D view needs WebGL, which this browser has turned off. The flat map below shows the same "
                 "findings.", "३D दृश्यासाठी WebGL लागते, जे या ब्राउझरमध्ये बंद आहे. खालचा सपाट नकाशा तेच निष्कर्ष दाखवतो."),
        "north": tr("Point north", "उत्तरेकडे वळवा"),
        "aria": tr("3D model of the study area with NISAR's findings", "निसारच्या निष्कर्षांसह अभ्यास क्षेत्राचे ३D मॉडेल"),
    }
    L["lg_new"] = L["lg_new"].format(a=ui.day(data.dates()[1]))
    cfg = dict(deck=DECK, dem=url(m["dem"]), tex={"relief": url(m["relief"]), "radar": url(m.get("radar"))},
               bounds=m["bounds"], minm=m["min_m"], ex=EX, zones=sc["zones"], floods=sc["floods"],
               events=sc["events"], places=sc["places"], stops=stops, tour=tour, L=L)
    page = _PAGE.replace("__CFG__", json.dumps(cfg, ensure_ascii=False)).replace("__H__", str(height)) \
        .replace("__ARIA__", _html.escape(L["aria"])).replace("__DECK__", DECK)
    components.html(page, height=height + 2)
    return True


_PAGE = r"""
<div id="wrap" role="region" aria-label="__ARIA__">
  <div id="sky"></div>
  <div id="map"></div>
  <div class="where" id="where"></div>
  <div class="ctrl" id="ctrl"></div>
  <button class="compass" id="compass" type="button"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M12 2l4 10h-8z" fill="#f0743a"/><path d="M12 22l-4-10h8z" fill="#cfd9e6"/></svg></button>
  <div class="legend" id="legend"></div>
  <div class="tour" id="tour"></div>
  <p class="note" id="note"></p>
  <div class="tip" id="tip" hidden></div>
</div>
<style>
  html, body { margin: 0; background: transparent; font-family: 'IBM Plex Sans', system-ui, sans-serif; }
  #wrap { position: relative; height: __H__px; border-radius: 18px; overflow: hidden; color: #e8eef7;
    background: radial-gradient(1200px 500px at 50% 115%, #10284f 0%, #0a1630 45%, #060b16 100%);
    box-shadow: 0 0 0 1px rgba(111,227,255,.18), 0 16px 44px rgba(0,0,0,.35); }
  #sky { position: absolute; inset: 0; opacity: .8; background-image:
    radial-gradient(1px 1px at 30px 40px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 190px 90px, #cfe3ff 50%, transparent 51%),
    radial-gradient(1.3px 1.3px at 330px 25px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 460px 120px, #fff 50%, transparent 51%),
    radial-gradient(1px 1px at 600px 60px, #bcd6ff 50%, transparent 51%), radial-gradient(1.2px 1.2px at 720px 150px, #fff 50%, transparent 51%);
    background-size: 760px 190px; }
  #map { position: absolute; inset: 0; }
  .where { position: absolute; top: 12px; left: 12px; display: flex; align-items: center; gap: 7px; padding: 6px 12px;
    border-radius: 99px; font-size: 13px; font-weight: 600; background: rgba(7,12,23,.62); border: 1px solid rgba(255,255,255,.14);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
  .ctrl { position: absolute; top: 12px; right: 56px; display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 6px; max-width: 70%; }
  .seg { display: inline-flex; border-radius: 99px; overflow: hidden; border: 1px solid rgba(255,255,255,.18); background: rgba(7,12,23,.62); }
  .seg button, .chip { font: 600 12.5px 'IBM Plex Sans', system-ui, sans-serif; color: #dbe6f4; background: transparent; border: 0;
    padding: 6px 11px; cursor: pointer; }
  .seg button[aria-pressed="true"] { background: #3d8ef0; color: #fff; }
  .chip { border-radius: 99px; border: 1px solid rgba(255,255,255,.18); background: rgba(7,12,23,.62); display: inline-flex;
    align-items: center; gap: 6px; }
  .chip i { width: 9px; height: 9px; border-radius: 50%; }
  .chip[aria-pressed="false"] { opacity: .5; }
  button:focus-visible { outline: 3px solid #6fe3ff; outline-offset: 2px; }
  .compass { position: absolute; top: 10px; right: 12px; width: 36px; height: 36px; border-radius: 50%; display: grid;
    place-items: center; padding: 0; background: rgba(7,12,23,.7); border: 1px solid rgba(255,255,255,.2); cursor: pointer; }
  .legend { position: absolute; left: 12px; bottom: 12px; padding: 9px 12px; border-radius: 12px; font-size: 12px; line-height: 1.7;
    background: rgba(7,12,23,.66); border: 1px solid rgba(255,255,255,.12); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
  .legend div { display: flex; align-items: center; gap: 8px; white-space: nowrap; }
  .legend .sw { width: 14px; height: 10px; border-radius: 3px; flex: none; }
  .legend .pin { width: 10px; height: 10px; border-radius: 50%; border: 2px solid #fff; flex: none; box-sizing: border-box; }
  .tour { position: absolute; right: 12px; bottom: 30px; width: min(380px, calc(100% - 24px)); padding: 12px 14px 12px;
    border-radius: 14px; background: rgba(7,12,23,.78); border: 1px solid rgba(111,227,255,.25);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); box-shadow: 0 10px 30px rgba(0,0,0,.35); }
  .tour h3 { margin: 4px 0 4px; font: 600 17px 'IBM Plex Sans Condensed', 'IBM Plex Sans', sans-serif; color: #fff; }
  .tour p { margin: 0 0 10px; font-size: 13.5px; line-height: 1.5; color: #d3deec; }
  .dots { display: flex; gap: 5px; }
  .dots span { width: 18px; height: 4px; border-radius: 2px; background: rgba(255,255,255,.22); }
  .dots span.on { background: #6fe3ff; }
  .row { display: flex; gap: 8px; }
  .btn { font: 600 13px 'IBM Plex Sans', system-ui, sans-serif; padding: 7px 14px; border-radius: 99px; cursor: pointer;
    border: 1px solid rgba(255,255,255,.22); background: transparent; color: #e8eef7; }
  .btn.primary { background: #3d8ef0; border-color: #3d8ef0; color: #fff; }
  .btn:disabled { opacity: .4; cursor: default; }
  .note { position: absolute; right: 14px; bottom: 6px; margin: 0; font-size: 10.5px; color: rgba(220,230,245,.65); }
  .tip { position: absolute; pointer-events: none; z-index: 5; max-width: 260px; padding: 8px 10px; border-radius: 10px; font-size: 12.5px;
    line-height: 1.45; background: rgba(7,12,23,.92); border: 1px solid rgba(111,227,255,.3); }
  .tip b { color: #fff; }
  .fail { position: absolute; inset: 0; display: grid; place-items: center; padding: 30px; text-align: center; font-size: 14px; }
  @media (max-width: 640px) {
    .ctrl { top: 52px; left: 12px; right: 12px; max-width: none; justify-content: flex-start; gap: 4px; }
    .seg button, .chip { font-size: 11.5px; padding: 5px 9px; }
    .legend { font-size: 11px; line-height: 1.55; padding: 6px 9px; bottom: 8px; left: 8px; }
    .note { display: none; }
    .tour { left: 8px; right: 8px; width: auto; bottom: 8px; }
    #wrap.tour-on .legend { display: none; }
    .tour p { font-size: 13px; }
  }
</style>
<script src="__DECK__"></script>
<script>
(function () {
  const C = __CFG__, L = C.L;
  const $ = id => document.getElementById(id);
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.deck) { $('map').innerHTML = '<div class="fail">' + L.nogl + '</div>'; return; }
  const {Deck, TerrainLayer, LineLayer, ScatterplotLayer, TextLayer, FlyToInterpolator, LinearInterpolator} = deck;
  const state = {tex: 'relief', show: {zones: true, floods: true, events: true, names: true}, i: 0, playing: false, orbit: !reduce, hover: null};
  const RGB = {zone: [240, 116, 58], flood: [47, 111, 208], event: [245, 248, 252]};
  const H = {high: 4200, medium: 2800, low: 2000};

  $('where').innerHTML = '<svg viewBox="0 0 24 24" width="15" height="15"><path d="M12 21s-6.5-6.6-6.5-11.5a6.5 6.5 0 0 1 13 0C18.5 14.4 12 21 12 21z" fill="#f0743a"/><circle cx="12" cy="9.5" r="2.4" fill="#fff"/></svg>' + L.where;
  $('note').textContent = L.note;
  $('legend').innerHTML =
    '<div><span class="sw" style="background:#b7d3f6"></span>' + L.lg_old + '</div>' +
    '<div><span class="sw" style="background:#3d8ef0"></span>' + L.lg_new + '</div>' +
    '<div><span class="pin" style="background:#2f6fd0"></span>' + L.lg_flood + '</div>' +
    '<div><span class="pin" style="background:#f0743a"></span>' + L.lg_zone + '</div>' +
    '<div><span class="pin" style="background:#f5f8fc;border-color:#1d3346"></span>' + L.lg_event + '</div>';

  function ctrl() {
    let h = '<span class="seg">';
    for (const t of ['relief', 'radar']) if (C.tex[t]) h += '<button type="button" data-tex="' + t + '" aria-pressed="' + (state.tex === t) + '">' + L[t] + '</button>';
    h += '</span>';
    const chip = (k, col) => '<button type="button" class="chip" data-show="' + k + '" aria-pressed="' + state.show[k] + '"><i style="background:' + col + '"></i>' + L[k] + '</button>';
    h += chip('zones', '#f0743a') + chip('floods', '#2f6fd0') + chip('events', '#f5f8fc') + chip('names', '#6fe3ff');
    $('ctrl').innerHTML = h;
    $('ctrl').querySelectorAll('[data-tex]').forEach(b => b.onclick = () => { state.tex = b.dataset.tex; ctrl(); draw(); });
    $('ctrl').querySelectorAll('[data-show]').forEach(b => b.onclick = () => { const k = b.dataset.show; state.show[k] = !state.show[k]; ctrl(); draw(); });
  }

  const ex = C.ex, B = C.bounds;
  const pinTop = (p, h) => [p[0], p[1], p[2] + h];
  function layers() {
    const out = [new TerrainLayer({
      id: 'terrain-' + state.tex, elevationData: C.dem, texture: C.tex[state.tex], bounds: B,
      elevationDecoder: {rScaler: 256 * ex, gScaler: ex, bScaler: ex / 256, offset: (-32768 - C.minm) * ex},
      meshMaxError: 4, loadOptions: {terrain: {skirtHeight: 0}}, material: {ambient: 0.55, diffuse: 0.55, shininess: 8, specularColor: [30, 30, 30]}
    })];
    const pins = [];
    if (state.show.zones) for (const z of C.zones) pins.push({k: 'zone', o: z, p: z.p, h: H[z.c] || 650, r: z.c === 'high' ? 7 : 5});
    if (state.show.floods) for (const f of C.floods) pins.push({k: 'flood', o: f, p: f.p, h: 2400, r: 5});
    if (state.show.events) for (const e of C.events) pins.push({k: 'event', o: e, p: e.p, h: 3200, r: 6});
    out.push(new LineLayer({id: 'stems', data: pins, getSourcePosition: d => d.p, getTargetPosition: d => pinTop(d.p, d.h),
      getColor: d => [...RGB[d.k], 210], getWidth: d => d.k === 'zone' && d.o.c === 'high' ? 2.5 : 1.5, widthUnits: 'pixels'}));
    out.push(new ScatterplotLayer({id: 'heads', data: pins, getPosition: d => pinTop(d.p, d.h), getRadius: d => d.r,
      radiusUnits: 'pixels', billboard: true, stroked: true, getLineColor: d => d.k === 'event' ? [29, 51, 70] : [255, 255, 255],
      lineWidthUnits: 'pixels', getLineWidth: 1.6, getFillColor: d => RGB[d.k], pickable: true, autoHighlight: true,
      highlightColor: [111, 227, 255, 255], onClick: ({object}) => object && fly({longitude: object.p[0], latitude: object.p[1] - 0.02, zoom: 12.3, pitch: 60, bearing: vs.bearing}, 1800)}));
    if (state.show.names) out.push(new TextLayer({id: 'names', data: C.places, getPosition: d => [d.p[0], d.p[1], d.p[2] + (d.big ? 700 : 450)],
      getText: d => d.n, getSize: d => d.big ? 17 : 13, getColor: [255, 255, 255, 240], fontFamily: 'IBM Plex Sans, system-ui, sans-serif',
      fontWeight: 600, outlineWidth: 4, outlineColor: [7, 12, 23, 230], fontSettings: {sdf: true}, characterSet: 'auto',
      getTextAnchor: 'middle', getAlignmentBaseline: 'bottom', billboard: true,
      extensions: deck.CollisionFilterExtension ? [new deck.CollisionFilterExtension()] : [],
      getCollisionPriority: d => d.big ? 10 : 0, collisionTestProps: {sizeScale: 1.6}}));
    return out;
  }

  // narrower screens see less, so pull every camera stop back a little
  const zf = Math.log2(Math.min(1, ($('wrap').clientWidth || 980) / 980));
  for (const s of C.stops) s.v.zoom += zf;
  let vs = Object.assign({}, C.stops[0].v);
  const map = new Deck({
    parent: $('map'), initialViewState: vs, controller: {touchRotate: true, inertia: 300},
    layers: [], useDevicePixels: Math.min(2, window.devicePixelRatio || 1),
    onViewStateChange: ({viewState, interactionState}) => {
      vs = viewState;
      $('compass').firstChild.style.transform = 'rotate(' + (-viewState.bearing) + 'deg)';
      if (interactionState && (interactionState.isDragging || interactionState.isZooming || interactionState.isRotating || interactionState.isPanning)) stopAuto();
      return viewState;
    },
    onHover: info => tip(info),
    getCursor: ({isHovering, isDragging}) => isDragging ? 'grabbing' : (isHovering ? 'pointer' : 'grab'),
    onError: (err) => { console.error('deck error', err && (err.message || err)); }
  });
  function draw() { map.setProps({layers: layers()}); }

  function tip(info) {
    const t = $('tip'), d = info.object;
    if (!d || !d.o) { t.hidden = true; return; }
    const o = d.o; let h = '';
    if (d.k === 'zone') h = '<b>' + L.zone + ' ' + o.id + '</b><br>' + L[o.c] + ', ' + L.slope + ' ' + o.sl + '°' + (o.near ? '<br>' + L.near + ' ' + o.near : '');
    else if (d.k === 'flood') h = '<b>' + L.flood + ' ' + o.id + '</b><br>' + o.a + ' ' + L.ha;
    else h = '<b>' + L.event + ' ' + (o.t === 'landslide' ? L.landslide : L.floodw) + '</b><br>' + o.place + '<br>' + o.d;
    t.innerHTML = h; t.hidden = false;
    t.style.left = Math.min(info.x + 14, $('wrap').clientWidth - 270) + 'px'; t.style.top = Math.max(8, info.y - 10) + 'px';
  }

  function fly(v, ms) {
    vs = Object.assign({}, vs, v);
    map.setProps({initialViewState: Object.assign({}, vs, {transitionDuration: reduce ? 0 : ms, transitionInterpolator: new FlyToInterpolator({speed: 1.2})})});
  }
  let orbitTimer = null;
  function orbit() {
    if (!state.orbit || reduce) return;
    const v = Object.assign({}, vs, {bearing: vs.bearing + 24, transitionDuration: 24000,
      transitionInterpolator: new LinearInterpolator(['bearing']), onTransitionEnd: () => { orbitTimer = setTimeout(orbit, 50); }});
    vs = Object.assign({}, vs, {bearing: vs.bearing + 24});
    map.setProps({initialViewState: v});
  }
  function stopAuto() { state.orbit = false; state.playing = false; clearTimeout(orbitTimer); clearTimeout(playTimer); card(); }

  let playTimer = null;
  function go(i) {
    state.i = Math.max(0, Math.min(C.stops.length - 1, i)); clearTimeout(orbitTimer);
    const s = C.stops[state.i];
    vs = Object.assign({}, vs, s.v);
    map.setProps({initialViewState: Object.assign({}, s.v, {transitionDuration: reduce ? 0 : 3200,
      transitionInterpolator: new FlyToInterpolator({speed: 1.1}),
      onTransitionEnd: () => { if (state.playing) playTimer = setTimeout(() => state.i < C.stops.length - 1 ? go(state.i + 1) : (state.playing = false, card()), 4200); }})});
    card();
  }
  function card() {
    if (!C.tour) { $('tour').style.display = 'none'; return; }
    const s = C.stops[state.i], n = C.stops.length;
    let h = '<div class="dots">' + C.stops.map((_, k) => '<span class="' + (k <= state.i ? 'on' : '') + '"></span>').join('') + '</div>';
    h += '<h3>' + s.t + '</h3><p>' + s.x + '</p><div class="row">';
    if (state.i === 0 && !state.started) h += '<button class="btn primary" id="tStart">' + L.start + '</button>';
    else {
      h += '<button class="btn" id="tBack"' + (state.i === 0 ? ' disabled' : '') + '>' + L.back + '</button>';
      h += '<button class="btn primary" id="tNext"' + (state.i === n - 1 ? ' disabled' : '') + '>' + L.next + '</button>';
      if (!reduce) h += '<button class="btn" id="tPlay">' + (state.playing ? L.pause : L.play) + '</button>';
    }
    h += '</div>';
    $('tour').innerHTML = h;
    const on = (id, f) => { const b = $(id); if (b) b.onclick = f; };
    on('tStart', () => { state.started = true; state.playing = !reduce; state.orbit = false; go(1); });
    on('tBack', () => { state.playing = false; clearTimeout(playTimer); go(state.i - 1); });
    on('tNext', () => { state.playing = false; clearTimeout(playTimer); go(state.i + 1); });
    on('tPlay', () => { state.playing = !state.playing; clearTimeout(playTimer); if (state.playing) go(state.i < n - 1 ? state.i + 1 : 1); else card(); });
  }
  $('compass').title = L.north; $('compass').setAttribute('aria-label', L.north);
  $('compass').onclick = () => { stopAuto(); fly({bearing: 0}, 900); };
  if (C.tour) $('wrap').classList.add('tour-on');
  ctrl(); draw(); card();
  setTimeout(orbit, 1200);
})();
</script>
"""
