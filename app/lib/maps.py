"""The interactive map (folium / Leaflet). Layer switching happens in the browser, so it is instant."""
from __future__ import annotations

import html

import folium
from folium.plugins import Fullscreen, MiniMap, MousePosition

from . import data, ui

ESRI = "https://server.arcgisonline.com/ArcGIS/rest/services"
BASEMAPS = {
    "Light": (f"{ESRI}/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}",
              "Base map &copy; Esri, HERE, Garmin, &copy; OpenStreetMap contributors"),
    "Dark": (f"{ESRI}/Canvas/World_Dark_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}",
             "Base map &copy; Esri, HERE, Garmin, &copy; OpenStreetMap contributors"),
    "Satellite": (f"{ESRI}/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}",
                  "Imagery &copy; Esri, Maxar, Earthstar Geographics"),
    "Topographic": (f"{ESRI}/World_Topo_Map/MapServer/tile/{{z}}/{{y}}/{{x}}",
                    "Base map &copy; Esri, HERE, Garmin, USGS, &copy; OpenStreetMap contributors"),
    "Streets": ("https://tile.openstreetmap.org/{z}/{x}/{y}.png", "&copy; OpenStreetMap contributors"),
}
LABELS = (f"{ESRI}/Canvas/World_Light_Gray_Reference/MapServer/tile/{{z}}/{{y}}/{{x}}", "Labels &copy; Esri")
LABELS_DARK = (f"{ESRI}/Canvas/World_Dark_Gray_Reference/MapServer/tile/{{z}}/{{y}}/{{x}}", "Labels &copy; Esri")
NAMES = {"Light": ("Light", "फिका", "Hell"), "Dark": ("Dark", "गडद", "Dunkel"), "Satellite": ("Satellite", "उपग्रह", "Satellit"),
         "Topographic": ("Topographic", "भूरचना", "Topografisch"), "Streets": ("Streets", "रस्ते", "Straßen")}


def basemap_name(key: str) -> str:
    n = NAMES.get(key, (key, key, key))
    return {"en": n[0], "mr": n[1], "de": n[2]}.get(ui.lang(), n[0])


def default_basemap() -> str:
    return "Dark" if ui.dark() else "Light"


def _dark_map(basemap: str) -> bool:
    return basemap in ("Dark", "Satellite")


def map_css(basemap: str) -> str:
    """Layer switcher, popups and the pulsing markers, in the colours of the map underneath."""
    dk = ui.dark()
    panel, text, line = ("rgba(10,18,34,.92)", "#e6edf6", "rgba(160,190,230,.22)") if dk else \
        ("rgba(255,255,255,.94)", "#1d3346", "rgba(29,51,70,.14)")
    return f"""<style>
.leaflet-container {{ background: {'#0b1220' if _dark_map(basemap) else '#eef1f4'}; font-family: 'IBM Plex Sans', system-ui, sans-serif; }}
.leaflet-control-layers, .leaflet-bar a, .leaflet-control-mouseposition, .leaflet-control-scale-line {{
  background: {panel} !important; color: {text} !important; border-color: {line} !important; }}
.leaflet-control-layers {{ font: 12.5px/1.35 'IBM Plex Sans', system-ui, sans-serif; border-radius: 12px !important;
  box-shadow: 0 6px 24px rgba(0,0,0,.18) !important; backdrop-filter: blur(6px); }}
.leaflet-control-layers-expanded {{ padding: 8px 12px 8px 10px; max-height: 70%; overflow-y: auto; }}
.leaflet-control-layers label {{ margin: 2px 0; }}
.leaflet-control-layers-separator {{ border-top-color: {line} !important; }}
.leaflet-bar {{ border-radius: 10px !important; overflow: hidden; border: 1px solid {line} !important; }}
.leaflet-control-mouseposition {{ font: 11.5px/1.3 'IBM Plex Sans', system-ui, sans-serif; padding: 3px 8px;
  border-radius: 8px; margin-bottom: 6px !important; }}
.leaflet-control-attribution {{ font: 10.5px/1.4 'IBM Plex Sans', system-ui, sans-serif !important;
  background: {panel} !important; color: {text} !important; border-radius: 8px 0 0 0; }}
.leaflet-control-attribution a {{ color: {'#7dbbff' if dk else '#1f6fd1'} !important; }}
.leaflet-popup-content-wrapper, .leaflet-popup-tip {{ background: {panel}; color: {text}; border-radius: 12px; }}
.leaflet-popup-content {{ font: 13px/1.45 'IBM Plex Sans', system-ui, sans-serif; color: {text}; }}
.leaflet-popup-content a {{ color: {'#7dbbff' if dk else '#1f6fd1'}; }}
.leaflet-tooltip {{ font: 12.5px/1.35 'IBM Plex Sans', system-ui, sans-serif; border-radius: 8px; }}
.leaflet-control-minimap {{ border-radius: 10px; border: 1px solid {line} !important; }}
.ml-pulse {{ position: relative; width: 18px; height: 18px; }}
.ml-pulse i {{ position: absolute; inset: 3px; border-radius: 50%; background: #f0743a; border: 2px solid #fff;
  box-shadow: 0 0 10px rgba(240,116,58,.9); }}
.ml-pulse::before, .ml-pulse::after {{ content: ""; position: absolute; inset: 0; border-radius: 50%;
  border: 2px solid #f0743a; animation: ml-ping 2.4s cubic-bezier(0,.4,.4,1) infinite; }}
.ml-pulse::after {{ animation-delay: 1.2s; }}
@keyframes ml-ping {{ from {{ transform: scale(.6); opacity: .9; }} to {{ transform: scale(2.6); opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .ml-pulse::before, .ml-pulse::after {{ animation: none; opacity: 0; }} }}
</style>"""


def _ink(basemap: str) -> str:
    return "#d7e6fa" if _dark_map(basemap) else ui.INK


ink_for = _ink


def _labels(basemap: str):
    return LABELS_DARK if basemap == "Dark" else LABELS


def _extras(m, basemap: str):
    """Mini overview map and the cursor's latitude and longitude, for people who will go to the spot."""
    url, attr = BASEMAPS["Dark" if _dark_map(basemap) else "Light"]
    MiniMap(tile_layer=folium.TileLayer(url, attr=attr), position="bottomright", width=110, height=90,
            zoom_level_offset=-5, toggle_display=True).add_to(m)
    MousePosition(position="bottomleft", separator=", ", num_digits=5, prefix="", empty_string="",
                  lat_formatter="function(n){return n.toFixed(5)+'° N'}",
                  lng_formatter="function(n){return n.toFixed(5)+'° E'}").add_to(m)

# name -> (label key or text, shown by default)
RASTERS = [
    ("rgb_before", "Radar colour, 28 Jun", False),
    ("rgb_after", "Radar colour, 10 Jul", False),
    ("hh_before", "Radar HH, 28 Jun", False),
    ("hh_after", "Radar HH, 10 Jul", False),
    ("change", "Change in HH (blue darker, red brighter)", False),
    ("coherence", "Coherence 28 Jun to 10 Jul (dark = changed)", False),
    ("permanent", "Rivers and reservoirs (JRC)", True),
    ("brighter", "Possible water under cover", True),
    ("rise", "Reservoirs and rivers rising", True),
    ("flood", "Flooding (no water recorded here 1984 to 2021)", True),
]

SLIDE_SVG = ('<svg width="18" height="18" viewBox="0 0 18 18"><path d="M9 2 L16.5 15.5 H1.5 Z" fill="#fff" '
             'stroke="#1d3346" stroke-width="2" stroke-linejoin="round"/></svg>')
FLOOD_SVG = ('<svg width="18" height="18" viewBox="0 0 18 18"><path d="M9 2 C9 2 3.5 8.5 3.5 11.5 A5.5 5.5 0 0 0 '
             '14.5 11.5 C14.5 8.5 9 2 9 2 Z" fill="#fff" stroke="#1d3346" stroke-width="2"/></svg>')
OTHER_SVG = ('<svg width="16" height="16" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="2" '
             'fill="#fff" stroke="#1d3346" stroke-width="2"/></svg>')


def center():
    b = data.bounds().get("bounds_latlon")
    if not b:
        return [18.52, 73.86]
    return [(b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2]


def build(basemap=None, opacity=0.85, show=None, location=None, zoom=10, height=600, events=True,
          zones=True, min_conf="medium", collapsed=False):
    """Return a folium.Map with every layer available in the layer switcher."""
    basemap = basemap or default_basemap()
    m = folium.Map(location=location or center(), zoom_start=zoom, tiles=None, control_scale=True,
                   prefer_canvas=True, zoom_snap=0.25, zoom_delta=0.5)
    b0 = data.bounds().get("bounds_latlon")
    if location is None and b0:
        # Fit the whole study box on any screen (a fixed zoom cut off the Western Ghats on phones).
        m.fit_bounds(b0, padding=(6, 6))
    m.get_root().header.add_child(folium.Element(map_css(basemap)))
    folium.map.CustomPane("labels", z_index=650, pointer_events=False).add_to(m)
    for name, (url, attr) in BASEMAPS.items():
        folium.TileLayer(url, attr=attr, name=name, overlay=False, control=True, show=(name == basemap),
                         max_zoom=18).add_to(m)
    b = data.bounds().get("bounds_latlon")
    show = show if show is not None else {n for n, _, on in RASTERS if on}
    for name, label, _ in RASTERS:
        url = data.overlay_url(name)
        if not url or not b:
            continue
        # folium only accepts absolute URLs or files; give it a placeholder, then point it at our static URL
        ov = folium.raster_layers.ImageOverlay(image="data:image/png;base64,", bounds=b, name=label,
                                               opacity=opacity, interactive=False, cross_origin=False, zindex=2,
                                               show=(name in show))
        ov.url = url
        ov.add_to(m)
    lab = _labels(basemap)
    folium.TileLayer(lab[0], attr=lab[1], name="Place names", overlay=True, control=True, show=True,
                     pane="labels", max_zoom=18).add_to(m)
    if zones:
        add_slide_zones(m, min_conf)
    add_flood_patches(m)
    if events:
        add_events(m)
    if b:
        folium.Rectangle(b, color=_ink(basemap), weight=1.2, fill=False, dash_array="4 4", name="Study box",
                         tooltip="Study box (NISAR crop)").add_to(m)
    folium.LayerControl(collapsed=collapsed, position="topright").add_to(m)
    Fullscreen(position="topleft").add_to(m)
    _extras(m, basemap)
    return m


def add_slide_zones(m, min_conf="medium"):
    gj = data.geojson("slide_zones.geojson")
    if not gj:
        return
    order = {"low": 0, "medium": 1, "high": 2}
    feats = [f for f in gj["features"] if order[f["properties"]["confidence"]] >= order[min_conf]]
    if not feats:
        return
    fg = folium.FeatureGroup(name=f"Likely slide zones ({len(feats)})", show=True)
    xt = any("track106" in f["properties"] for f in feats)
    dem = any("nasadem" in f["properties"] for f in feats)
    if dem:   # one readable popup line: "found", or "not found: steeper than 45°"
        feats = [{**f, "properties": {**f["properties"], "dem_txt": f["properties"].get("nasadem", "") + (
            ": " + f["properties"]["nasadem_reason"].replace(" in NASADEM", "")
            if f["properties"].get("nasadem_reason") else "")}} for f in feats]
    pop_f = ["id", "confidence", "score", "area_ha", "slope_deg", "hv_change_db", "hh_change_db", "coherence",
             "coherence_vs_local"] + (["track106"] if xt else []) + (["dem_txt"] if dem else [])
    pop_a = ["Zone", "Confidence", "Score (0-1)", "Area (ha)", "Mean slope (°)", "HV change (dB)", "HH change (dB)",
             "Coherence", "Coherence vs 1 km area"] + (["Second NISAR track (3-15 Jul)"] if xt else []) + \
        (["With NASA's NASADEM elevation map"] if dem else [])
    folium.GeoJson(
        {"type": "FeatureCollection", "features": feats},
        style_function=lambda f: {"color": ui.COLORS["slide_zones"], "weight": 2.5,
                                  "fillColor": ui.COLORS["slide_zones"],
                                  "fillOpacity": 0.45 if f["properties"]["confidence"] == "high" else 0.2},
        highlight_function=lambda f: {"weight": 4, "fillOpacity": 0.6},
        tooltip=folium.GeoJsonTooltip(fields=["id", "confidence", "area_ha", "slope_deg"],
                                      aliases=["Zone", "Confidence", "Area (ha)", "Slope (°)"]),
        popup=folium.GeoJsonPopup(fields=pop_f, aliases=pop_a),
    ).add_to(fg)
    # Zones are often under half a hectare: a marker at each centre keeps them visible at any zoom.
    for f in feats:
        p = f["properties"]
        both = p.get("track106") == "confirmed"
        tip = f"{p['id']}: likely slide zone ({p['confidence']}), {p.get('near') or ''}"
        if both:
            tip += "; also found by a second NISAR track"
        if p["confidence"] == "high":   # the few strongest leads pulse, so the eye finds them first
            folium.Marker([p["lat"], p["lon"]], tooltip=tip,
                          icon=folium.DivIcon(html='<div class="ml-pulse"><i></i></div>', icon_size=(18, 18),
                                              icon_anchor=(9, 9), class_name="ml-pulse-wrap")).add_to(fg)
        else:
            folium.CircleMarker([p["lat"], p["lon"]], radius=6 if both else 5,
                                color=ui.COLORS["slide_zones"], weight=3.5 if both else 2, fill=True,
                                fill_opacity=0.7 if both else 0.35, tooltip=tip).add_to(fg)
    fg.add_to(m)


def add_flood_patches(m):
    gj = data.geojson("new_water.geojson")
    if not gj:
        return
    feats = [f for f in gj["features"] if f["properties"].get("kind") == "flood"]
    if not feats:
        return
    fg = folium.FeatureGroup(name=f"Flood patches ({len(feats)})", show=True)
    for f in feats:
        p = f["properties"]
        folium.CircleMarker([p["lat"], p["lon"]], radius=6, color=ui.COLORS["flood"], weight=2, fill=True,
                            fill_opacity=0.4,
                            tooltip=f"Flood water on 10 July: {p['area_ha']} ha, {p.get('drop_db', '')} dB darker"
                                    + (f", near {p['near']}" if p.get("near") else "")).add_to(fg)
    fg.add_to(m)


def add_events(m):
    ev = data.events()
    if not ev or not ev.get("features"):
        return
    val = data.table("validation.csv")
    result = {} if val is None else dict(zip(val["id"].astype(str), val["result"].astype(str)))
    reason = {} if val is None else dict(zip(val["id"].astype(str), val["reason"].fillna("").astype(str)))
    fg = folium.FeatureGroup(name=f"Reported events ({len(ev['features'])})", show=True)
    for f in ev["features"]:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        typ = str(p.get("type", ""))
        svg = SLIDE_SVG if typ == "landslide" else FLOOD_SVG if typ in ("flood", "waterlogging",
                                                                          "river_overflow") else OTHER_SVG
        rid = str(p.get("id", ""))
        res = result.get(rid, "")
        res_txt = {"hit": "Radar detection nearby", "miss": "No radar detection nearby",
                   "not observable": "Radar could not observe this"}.get(res, res)
        src = p.get("source_url", "")
        body = (f"<b>{html.escape(str(p.get('place', '')))}</b><br>{html.escape(typ.replace('_', ' '))}, "
                f"{html.escape(str(p.get('date', '')))}<br>{html.escape(res_txt)}"
                + (f"<br><i>{html.escape(reason.get(rid, ''))}</i>" if reason.get(rid) else "")
                + (f'<br><a href="{html.escape(src)}" target="_blank">{html.escape(str(p.get("source_name") or "source"))}</a>'
                   if src else ""))
        folium.Marker([lat, lon], icon=folium.DivIcon(html=svg, icon_size=(18, 18), icon_anchor=(9, 9)),
                      tooltip=f"{p.get('place', '')} ({typ.replace('_', ' ')})",
                      popup=folium.Popup(body, max_width=280)).add_to(fg)
    fg.add_to(m)


def one_pass(date: str, location=None, zoom=10, basemap=None, water=True, collapsed=True):
    """What NISAR saw on one pass: its radar colour image, and the open water mapped on that date."""
    basemap = basemap or default_basemap()
    m = folium.Map(location=location or center(), zoom_start=zoom, tiles=None, control_scale=True,
                   prefer_canvas=True, zoom_snap=0.25, zoom_delta=0.5)
    b = data.bounds().get("bounds_latlon")
    if location is None and b:
        m.fit_bounds(b, padding=(6, 6))
    m.get_root().header.add_child(folium.Element(map_css(basemap)))
    folium.map.CustomPane("labels", z_index=650, pointer_events=False).add_to(m)
    url, attr = BASEMAPS[basemap]
    folium.TileLayer(url, attr=attr, name=basemap, max_zoom=18, control=False).add_to(m)
    layers = [(data.pass_images().get(date), f"Radar colour, {date}", 1.0, True),
              (data.overlay_url(f"water_d{date}"), f"Open water, {date}", 0.9, water)]
    for ov_url, name, opacity, show in layers:
        if not ov_url or not b:
            continue
        ov = folium.raster_layers.ImageOverlay(image="data:image/png;base64,", bounds=b, name=name, opacity=opacity,
                                               interactive=False, cross_origin=False, zindex=2, show=show)
        ov.url = ov_url
        ov.add_to(m)
    lab = _labels(basemap)
    folium.TileLayer(lab[0], attr=lab[1], name="Place names", overlay=True, control=True, show=True, pane="labels",
                     max_zoom=18).add_to(m)
    if b:
        folium.Rectangle(b, color=_ink(basemap), weight=1.2, fill=False, dash_array="4 4", control=False,
                         tooltip="Study box (NISAR crop)").add_to(m)
    folium.LayerControl(collapsed=collapsed, position="topright").add_to(m)
    Fullscreen(position="topleft").add_to(m)
    _extras(m, basemap)
    return m


def season(date: str, basemap=None, opacity=0.9):
    """Open water on one NISAR pass (season slider), on a plain base map."""
    basemap = basemap or default_basemap()
    m = folium.Map(location=center(), zoom_start=10, tiles=None, control_scale=True, prefer_canvas=True,
                   zoom_snap=0.25, zoom_delta=0.5)
    b = data.bounds().get("bounds_latlon")
    if b:
        m.fit_bounds(b, padding=(6, 6))
    m.get_root().header.add_child(folium.Element(map_css(basemap)))
    folium.map.CustomPane("labels", z_index=650, pointer_events=False).add_to(m)
    url, attr = BASEMAPS[basemap]
    folium.TileLayer(url, attr=attr, name=basemap, max_zoom=18).add_to(m)
    ov_url = data.overlay_url(f"water_d{date}")
    if ov_url and b:
        ov = folium.raster_layers.ImageOverlay(image="data:image/png;base64,", bounds=b, name=f"Open water, {date}",
                                               opacity=opacity, interactive=False, cross_origin=False, zindex=2)
        ov.url = ov_url
        ov.add_to(m)
    lab = _labels(basemap)
    folium.TileLayer(lab[0], attr=lab[1], name="Place names", overlay=True, pane="labels",
                     max_zoom=18).add_to(m)
    if b:
        folium.Rectangle(b, color=_ink(basemap), weight=1.2, fill=False, dash_array="4 4",
                         tooltip="Study box (NISAR crop)").add_to(m)
    Fullscreen(position="topleft").add_to(m)
    _extras(m, basemap)
    return m
