"""Check a place: what NISAR found within a few kilometres of a village, a town or a point on the map."""
import html

import folium
import streamlit as st
from streamlit_folium import st_folium

from lib import data, evidence as ev, maps, ui

ui.setup("Check a place")
ui.demo_banner()
if not ui.require_results():
    st.stop()
tr = ui.tr
ss = st.session_state
before, after = data.dates()

ui.page_header(tr('Check a place', 'एखादे ठिकाण तपासा'), tr(
    "Pick your village or town, or click the map, to see what NISAR found nearby between {b} and {a}.",
    "तुमचे गाव किंवा शहर निवडा, किंवा नकाशावर क्लिक करा, आणि {b} ते {a} दरम्यान निसारला जवळपास काय सापडले ते पाहा.",
    b=ui.day(before), a=ui.day(after)), tr("People who live there", "तिथे राहणारे लोक"))

places = data.places()
b = data.bounds().get("bounds_latlon")
if places is None or not b:
    st.info("The place list is not built yet: run `python -m pipeline.gazetteer`.")
    st.stop()
(south, west), (north, east) = b


def _label(row) -> str:
    kind = {"city": tr("city", "शहर"), "town": tr("town", "शहर"), "suburb": tr("suburb", "उपनगर"),
            "village": tr("village", "गाव")}.get(row["place"], row["place"])
    if ui.lang() in ("mr", "hi") and row["name_mr"]:
        return f"{row['name_mr']} ({row['name']}) · {kind}"
    return f"{row['name']}" + (f" ({row['name_mr']})" if row["name_mr"] else "") + f" · {kind}"


by_id = {int(r.osm_id): r for r in places.itertuples(index=False)}
labels = {int(r.osm_id): _label(r._asdict()) for r in places.itertuples(index=False)}


def _set_place(osm_id: int):
    r = by_id[osm_id]
    ss.pt = {"lat": float(r.lat), "lon": float(r.lon), "osm_id": osm_id, "name": r.name, "name_mr": r.name_mr}


# Start from the link if it names a place or a point (shareable results).
if "pt" not in ss:
    q = st.query_params
    try:
        if "place" in q and int(q["place"]) in by_id:
            _set_place(int(q["place"]))
        elif "lat" in q and "lon" in q:
            ss.pt = {"lat": float(q["lat"]), "lon": float(q["lon"]), "osm_id": None, "name": None, "name_mr": ""}
    except (TypeError, ValueError):
        pass
    if "r" in q and q["r"] in ("2", "5", "10"):
        ss.place_r = int(q["r"])

pt = ss.get("pt")
opts = list(by_id)
cur = pt.get("osm_id") if pt else None
with st.container(key="tour_place"):
    c1, c2 = st.columns([3, 1.3])
choice = c1.selectbox(tr("Village, town or suburb", "गाव, शहर किंवा उपनगर"), opts,
                      index=opts.index(cur) if cur in opts else None, format_func=lambda i: labels[i],
                      placeholder=tr("Type a name, for example Lonavala", "नाव टाइप करा, उदा. लोणावळा"))
if choice is not None and choice != cur:
    _set_place(choice)
    st.rerun()
r_km = c2.segmented_control(tr("Distance", "अंतर"), [2, 5, 10], default=ss.get("place_r", 5),
                            format_func=lambda k: f"{k} km", key="place_r_ctl") or 5
ss.place_r = r_km

pt = ss.get("pt")
if pt:
    st.query_params.clear()
    if ui.lang() != "en":
        st.query_params["lang"] = ui.lang()
    if pt.get("osm_id"):
        st.query_params.update({"place": str(pt["osm_id"]), "r": str(r_km)})
    else:
        st.query_params.update({"lat": f"{pt['lat']:.5f}", "lon": f"{pt['lon']:.5f}", "r": str(r_km)})

# ---------------------------------------------------------------- what is near
zones, floods, water = data.zones(), data.flood_patches(), data.water_patches()
events = (data.events() or {}).get("features", [])
val = data.table("validation.csv")
vres = {} if val is None else {str(a): (str(r), str(w) if w == w else "") for a, r, w in
                                zip(val["id"], val["result"], val["reason"])}


def near(items, lat, lon, k):
    out = []
    for p in items:
        d = data.km(lat, lon, p["lat"], p["lon"])
        if d <= k:
            out.append((d, p))
    return sorted(out, key=lambda x: x[0])


def _map(location=None, zoom=10, min_conf="medium"):
    return maps.build(location=location, zoom=zoom, min_conf=min_conf, collapsed=True)


if pt:
    lat, lon = pt["lat"], pt["lon"]
    inside = south <= lat <= north and west <= lon <= east
    z_near = near(zones, lat, lon, r_km)
    f_near = near(floods, lat, lon, r_km)
    rise_ha = sum(p["area_ha"] for d, p in near(water, lat, lon, r_km) if p.get("kind") == "rise")
    ev_pts = [{"lat": f["geometry"]["coordinates"][1], "lon": f["geometry"]["coordinates"][0], **f["properties"]}
              for f in events]
    e_near = near(ev_pts, lat, lon, r_km)
    if pt.get("name"):
        where = (pt["name_mr"] or pt["name"]) if ui.lang() in ("mr", "hi") else pt["name"]
    else:
        where = tr("the point you picked", "तुम्ही निवडलेला बिंदू")
    zoom = {2: 13, 5: 12, 10: 11}[r_km]
    m = _map(location=[lat, lon], zoom=zoom, min_conf="low")
    pin = maps.ink_for(maps.default_basemap())
    folium.Circle([lat, lon], radius=r_km * 1000, color=pin, weight=2, fill=True, fill_opacity=0.05,
                  dash_array="6 6").add_to(m)
    folium.CircleMarker([lat, lon], radius=7, color="#fff", weight=2.5, fill=True, fill_color="#3d8ef0",
                        fill_opacity=1, tooltip=where).add_to(m)
else:
    m = _map()

left, right = st.columns([1.35, 1], gap="large")
with left:
    out = st_folium(m, height=520, use_container_width=True, returned_objects=["last_clicked"],
                    key=f"place_map_{pt['lat'] if pt else 0}_{pt['lon'] if pt else 0}_{r_km}_{ui.dark()}")
    st.caption(tr("Click the map to check any other point.", "दुसरा कोणताही बिंदू तपासण्यासाठी नकाशावर क्लिक करा."))
clk = (out or {}).get("last_clicked")
if clk and (not pt or abs(clk["lat"] - pt["lat"]) > 1e-6 or abs(clk["lng"] - pt["lon"]) > 1e-6):
    if clk != ss.get("last_click"):
        ss.last_click = clk
        ss.pt = {"lat": clk["lat"], "lon": clk["lng"], "osm_id": None, "name": None, "name_mr": ""}
        st.rerun()

with right:
    if not pt:
        st.markdown(f"### {tr('Start with a place', 'एखाद्या ठिकाणापासून सुरुवात करा')}")
        st.markdown(tr(
            "Choose one of {n} villages, towns and suburbs in the study area (names from OpenStreetMap), or click "
            "the map. The result has its own link, so you can send it to someone.",
            "अभ्यास क्षेत्रातील {n} गावे, शहरे आणि उपनगरांपैकी एक निवडा (नावे OpenStreetMap वरून), किंवा नकाशावर "
            "क्लिक करा. निकालाची स्वतःची लिंक असते, ती तुम्ही कोणालाही पाठवू शकता.", n=len(places)))
        ex = [i for n in ("Lonavala", "Tamhini", "Pune") for i, r in by_id.items() if r.name == n]
        if ex:
            st.markdown(f"**{tr('Try one of these', 'यापैकी एक वापरून पाहा')}**")
            with st.container(horizontal=True, gap="small", key="place_examples"):
                for i in ex:
                    r = by_id[i]
                    st.button(r.name_mr if ui.lang() in ("mr", "hi") and r.name_mr else r.name, key=f"ex_{i}",
                              icon=":material/location_on:", on_click=_set_place, args=(i,))
    elif not inside:
        st.warning(tr("This point is outside the area we processed NISAR data for. Pick a place inside the dashed box.",
                      "हा बिंदू आम्ही निसार डेटा तपासलेल्या भागाबाहेर आहे. ठिपक्यांच्या चौकटीतील ठिकाण निवडा."))
    else:
        st.markdown(f'<p class="ml-kicker">{html.escape(tr("Within {k} km of", "{k} किमीच्या आत:", k=r_km))}</p>'
                    f'<h2 style="margin-top:0">{html.escape(where)}</h2>', unsafe_allow_html=True)
        high = sum(p["confidence"] == "high" for d, p in z_near)
        tiles = [
            (ui.COLORS["slide_zones"], str(len(z_near)), "", tr("likely slide zones", "संभाव्य भूस्खलन क्षेत्रे")
             + (tr(", {h} high confidence", ", त्यापैकी {h} उच्च खात्रीची", h=high) if high else ""), False),
            (ui.COLORS["flood"], str(len(f_near)), "", tr("flood patches still standing on {a}",
                                                          "{a} रोजी अजूनही साचलेल्या पुराच्या जागा", a=ui.day(after)),
             False),
            (ui.COLORS["rise"], ui.fmt_num(rise_ha, 1), "ha", tr("of new water as reservoirs and rivers rose",
                                                                 "धरणे आणि नद्या वाढल्याने नवीन पाणी"), False),
            ("currentColor", str(len(e_near)), "", tr("reported floods or landslides", "नोंदवलेले पूर किंवा भूस्खलन"), False),
        ]
        st.markdown(f'<div lang="{ui.lang()}" class="ml-grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">' + "".join(
            f'<div class="ml-stat" style="--c:{c}"><div class="k">{html.escape(k)}<small>{html.escape(u)}</small></div>'
            f'<p class="lbl" style="margin-bottom:0">{html.escape(l)}</p></div>' for c, k, u, l, _ in tiles)
            + "</div>", unsafe_allow_html=True)
        if not z_near and not f_near and not e_near:
            nz = min(((data.km(lat, lon, p["lat"], p["lon"]), p) for p in zones), default=None, key=lambda x: x[0])
            st.markdown(tr(
                "NISAR found no slide zone or flood water here. That is not an all-clear: radar misses water between "
                "buildings, slides narrower than 40 m, and anything that came and went between passes.",
                "निसारला इथे भूस्खलन क्षेत्र किंवा पुराचे पाणी सापडले नाही. याचा अर्थ सर्व सुरक्षित असा नाही: इमारतींमधील "
                "पाणी, ४० मीटरपेक्षा अरुंद भूस्खलने आणि दोन निरीक्षणांच्या मधे आलेले-गेलेले पाणी रडारला दिसत नाही."))
            if nz:
                st.caption(tr("Nearest likely slide zone: {id}, {k} km away.", "सर्वात जवळचे संभाव्य भूस्खलन क्षेत्र: "
                              "{id}, {k} किमी दूर.", id=nz[1]["id"], k=ui.num(nz[0])))
        st.caption(tr("Copy the address bar to share this result.",
                      "हा निकाल पाठवण्यासाठी ब्राउझरमधील पत्ता कॉपी करा."))

if pt and south <= pt["lat"] <= north and west <= pt["lon"] <= east:
    if z_near:
        st.markdown(f"## {tr('Likely slide zones', 'संभाव्य भूस्खलन क्षेत्रे')}")
        z_sorted = sorted(z_near, key=lambda x: -x[1]["score"])
        for d, p in z_sorted[:3]:
            st.markdown(f'<p class="ml-kicker">{html.escape(tr("{k} km away", "{k} किमी दूर", k=ui.num(d)))}</p>',
                        unsafe_allow_html=True)
            ev.show_zone(p, open_note=False)
        if len(z_sorted) > 3:
            with st.expander(tr("{n} more zones", "आणखी {n} क्षेत्रे", n=len(z_sorted) - 3)):
                for d, p in z_sorted[3:]:
                    ev.show_zone(p, open_note=False)
        st.caption(ev.e("lead") + " " + ev.e("chip_note"))
    if f_near:
        st.markdown(f"## {tr('Flood water', 'पुराचे पाणी')}")
        for d, p in f_near[:4]:
            ev.show_flood(p)
    if e_near:
        st.markdown(f"## {tr('What people reported', 'लोकांनी काय नोंदवले')}")
        rows = []
        for d, p in e_near:
            res, why = vres.get(str(p.get("id")), ("", ""))
            res_txt = {"hit": tr("radar found something within range", "रडारला जवळपास काहीतरी सापडले"),
                       "miss": tr("radar missed it", "रडारला दिसले नाही"),
                       "not observable": tr("radar could not observe it", "रडार हे पाहू शकले नाही"),
                       "not scored": tr("not scored", "मोजले नाही")}.get(res, res)
            src = p.get("source_url", "")
            link = f' · <a href="{html.escape(src)}" target="_blank" rel="noopener">{html.escape(p.get("source_name") or "source")}</a>' if src else ""
            rows.append(f'<li><b>{html.escape(str(p.get("place", "")))}</b>: {html.escape(ev.type_word(p.get("type", "")))}, '
                        f'{html.escape(str(p.get("date", "")))}, {ui.num(d)} km{link}<br><span class="ml-muted">'
                        f'{html.escape(res_txt)}{(": " + html.escape(why)) if why else ""}</span></li>')
        st.markdown(f'<ul>{"".join(rows)}</ul>', unsafe_allow_html=True)

np_ = data.next_pass()
if np_:
    st.markdown(f'<div class="ml-pass"><span>🛰️</span><span>' + tr(
        "NISAR passes over Pune every 12 days, cloud or not. Last pass in our data: <b>{l}</b>. If it keeps its 12-day "
        "repeat, the next is <b>{n}</b>, and this page can be rebuilt from it.",
        "निसार दर १२ दिवसांनी पुण्यावरून जातो, ढग असोत वा नसोत. आमच्या डेटातील शेवटचे निरीक्षण: <b>{l}</b>. १२ दिवसांचे "
        "चक्र कायम राहिल्यास पुढचे <b>{n}</b> रोजी, आणि हे पान त्यावरून पुन्हा तयार करता येईल.",
        l=ui.date(np_[0]), n=ui.date(np_[1])) + "</span></div>", unsafe_allow_html=True)
st.markdown('<p class="ml-source">Place names © OpenStreetMap contributors (ODbL). Radar: NISAR L2 GCOV and GUNW '
            '(NASA/JPL-Caltech and ISRO, via ASF DAAC).</p>', unsafe_allow_html=True)
ui.sources_line()
