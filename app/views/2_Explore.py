import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

import html

from lib import view3d, charts, data, evidence as ev, maps, ui

ui.setup("Explore the map")
ui.demo_banner()
if not ui.require_results():
    st.stop()

before, after = data.dates()
tr = ui.tr
ss = st.session_state
ui.page_header(ui.t("explore"), tr(
    "Everything NISAR found around Pune: take the 3D tour, or open the flat map for each zone's radar evidence.",
    "निसारला पुण्याभोवती सापडलेले सर्व काही: ३D फेरफटका घ्या, किंवा प्रत्येक क्षेत्राच्या रडार पुराव्यासाठी सपाट नकाशा उघडा."),
    tr("All findings on one map", "सर्व निष्कर्ष एकाच नकाशावर"))

seasons = data.season_dates()
modes = (["3d"] if view3d.meta() else []) + ["change"] + (["season"] if len(seasons) >= 3 else [])
mode = st.segmented_control(
    tr("What the map shows", "नकाशा काय दाखवतो"), modes, key="explore_mode",
    default=None if "explore_mode" in ss else modes[0],
    format_func=lambda k: {"3d": tr("3D tour", "३D फेरफटका"),
                           "change": tr("Flat map: what changed, {b} to {a}", "सपाट नकाशा: काय बदलले, {b} ते {a}",
                                        b=ui.day(before), a=ui.day(after)),
                           "season": tr("Water through the season, {f} to {l}", "हंगामातील पाणी, {f} ते {l}",
                                        f=ui.day(seasons[0]) if seasons else "", l=ui.day(seasons[-1]) if seasons else "")}[k]
) or modes[0]

if mode == "3d":
    view3d.render(height=640, key="explore3d")
    st.caption(tr("For each zone's radar evidence and the tables, switch to the flat map above.",
                  "प्रत्येक क्षेत्राचा रडार पुरावा आणि तक्त्यांसाठी वर सपाट नकाशा निवडा."))
    ui.sources_line()
    st.stop()

if mode == "season":
    tl = data.table("timeline.csv")
    st.markdown(f'<div class="ml-dates">' + tr(
        "Open water on every NISAR pass of the same orbit and radar mode. Drag the slider to watch the reservoirs "
        "fill after the July storm.", "एकाच कक्षेतील आणि रडार पद्धतीतील प्रत्येक निसार निरीक्षणातील उघडे पाणी. जुलैच्या "
        "वादळानंतर धरणे भरताना पाहण्यासाठी स्लायडर ओढा.") + "</div>", unsafe_allow_html=True)
    d = st.select_slider(tr("NISAR pass", "निसार निरीक्षण"), options=seasons, value=seasons[0] if
                         ss.get("season_pick") not in seasons else ss["season_pick"], format_func=ui.date, key="season_pick")
    row = tl[tl["date"] == d].iloc[0] if tl is not None and (tl["date"] == d).any() else None
    first = tl[tl["date"] == seasons[0]].iloc[0] if tl is not None and (tl["date"] == seasons[0]).any() else None
    col = "water_in_jrc_extent_km2" if tl is not None and "water_in_jrc_extent_km2" in tl else "water_km2"
    if row is not None:
        delta = "" if first is None or d == seasons[0] else tr(" ({s}{v:.0f} km² since {f})", " ({f} पासून {s}{v:.0f} चौ. किमी)",
                                                              s="+" if row[col] >= first[col] else "−",
                                                              v=abs(row[col] - first[col]), f=ui.day(seasons[0]))
        st.markdown(f'<p class="ml-lede"><b>{row[col]:.0f} km²</b> ' + tr(
            "of open water inside the area where water has ever been recorded (JRC, 1984 to 2021) on {d}",
            "{d} रोजी, जिथे कधी ना कधी पाणी नोंदवले गेले आहे (JRC, १९८४ ते २०२१) अशा भागात उघडे पाणी", d=ui.date(d))
            + f"{delta}.</p>", unsafe_allow_html=True)
    ui.legend([(ui.COLORS["new_water"], tr("Open water on this pass", "या निरीक्षणातील उघडे पाणी"), "fill")])
    st_folium(maps.season(d), height=600, use_container_width=True, returned_objects=[], key=f"season_{d}_{ui.dark()}")
    if tl is not None and len(tl) > 1:
        st.plotly_chart(charts.timeline(tl), width="stretch", config={"displayModeBar": False})
        st.caption(ui.t("timeline_caption"))
    ui.sources_line()
    st.stop()

st.markdown(f'<div class="ml-dates">' + tr(
    "Layers: button at the top right of the map. Click a marker, or pick a row below, for details.",
    "स्तर: नकाशाच्या वर उजवीकडील बटण. तपशीलासाठी खुणेवर क्लिक करा किंवा खाली एक ओळ निवडा.") + "</div>",
    unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.2, 1])
bm_keys = list(maps.BASEMAPS)
basemap = c1.selectbox(tr("Base map", "मूळ नकाशा"), bm_keys, index=bm_keys.index(maps.default_basemap()),
                       format_func=maps.basemap_name)
opacity = c2.slider(tr("Layer opacity", "स्तराची पारदर्शकता"), 0.2, 1.0, 0.85, 0.05)
conf = c3.selectbox(tr("Slide zones shown", "दाखवलेली भूस्खलन क्षेत्रे"), ["high", "medium", "low"], index=1,
                    format_func=lambda x: {"high": tr("High confidence only", "फक्त उच्च खात्री"),
                                           "medium": tr("Medium and high", "मध्यम आणि उच्च"),
                                           "low": tr("All, including low", "सर्व, कमीसह")}[x])
ui.legend([(ui.COLORS["flood"], ui.t("legend_flood"), "fill"),
           (ui.COLORS["rise"], ui.t("legend_rise"), "fill"),
           (ui.COLORS["slide_zones"], ui.t("legend_slides"), "outline"),
           (ui.COLORS["brighter"], ui.t("legend_brighter"), "hatch"),
           (ui.COLORS["permanent"], ui.t("legend_permanent"), "fill"),
           (None, ui.t("legend_events"), "dot")])
focus = ss.get("explore_focus")          # ("zone"|"flood", id)
fprops = None
if focus:
    pool = data.zones() if focus[0] == "zone" else data.flood_patches()
    fprops = next((p for p in pool if p.get("id") == focus[1]), None)
loc = [fprops["lat"], fprops["lon"]] if fprops else None
# Zoomed to one finding, satellite imagery says more than the plain base map.
m = maps.build(basemap="Satellite" if fprops and basemap in ("Light", "Dark") else basemap, opacity=opacity,
               min_conf="low" if fprops else conf, location=loc,
               zoom=14 if fprops else 10, collapsed=True)
st_folium(m, height=640, use_container_width=True, returned_objects=[],
          key=f"explore_{basemap}_{opacity}_{conf}_{focus}_{ui.dark()}")
if fprops:
    cA, cB = st.columns([4, 1])
    cA.markdown(f'<p class="ml-kicker">{html.escape(tr("Map zoomed to {i}", "नकाशा {i} वर केंद्रित", i=fprops["id"]))}</p>',
                unsafe_allow_html=True)
    if cB.button(tr("Show the whole area", "संपूर्ण भाग दाखवा"), use_container_width=True):
        ss.explore_focus = None
        st.rerun()
    if focus[0] == "zone":
        ev.show_zone(fprops)
    else:
        ev.show_flood(fprops)

tab_z, tab_w, tab_t, tab_e, tab_d = st.tabs([tr("Slide zones", "भूस्खलन क्षेत्रे"), tr("Flood water", "पुराचे पाणी"),
                                             tr("Rain and timeline", "पाऊस आणि कालरेषा"),
                                             tr("Reported events", "नोंदवलेल्या घटना"), tr("Downloads", "डाउनलोड")])
with tab_z:
    gj = data.geojson("slide_zones.geojson")
    if gj and gj["features"]:
        df = pd.DataFrame([f["properties"] for f in gj["features"]])
        if "near" not in df:
            df["near"] = ""
        df["near"] = df["near"].fillna("")
        df["map"] = [f"https://www.google.com/maps/search/?api=1&query={a},{b}" for a, b in zip(df["lat"], df["lon"])]
        df["confidence"] = df["confidence"].map({"high": tr("High", "उच्च"), "medium": tr("Medium", "मध्यम"),
                                                 "low": tr("Low", "कमी")}).fillna(df["confidence"])
        if "track106" in df:
            df["track106"] = df["track106"].map({"confirmed": tr("found again", "पुन्हा सापडले"),
                                                 "partial": tr("partly", "अंशतः"),
                                                 "not seen": tr("not seen", "दिसले नाही"),
                                                 "not covered": tr("outside view", "दृष्टीबाहेर")}).fillna("")
        cols = ["id", "near", "confidence", "score", "track106", "area_ha", "slope_deg", "hv_change_db",
                "hh_change_db", "coherence", "coherence_vs_local", "lat", "lon", "map"]
        st.markdown(tr("{n} likely slide zones, highest score first. Select a row to zoom to it and see its radar "
                       "evidence.", "{n} संभाव्य भूस्खलन क्षेत्रे, सर्वाधिक गुण आधी. नकाशा केंद्रित करून रडार पुरावा "
                       "पाहण्यासाठी एक ओळ निवडा.", n=len(df)))
        cc = st.column_config
        zev = st.dataframe(df[[c for c in cols if c in df]], hide_index=True, width="stretch", on_select="rerun",
                     selection_mode="single-row", key="explore_zone_table",
                     column_config={"id": tr("Zone", "क्षेत्र"), "confidence": tr("Confidence", "खात्री"),
                                    "track106": cc.TextColumn(tr("2nd orbit", "दुसरी कक्षा"),
                                                              help=tr("NISAR track 106, 3 to 15 July",
                                                                      "निसार मार्ग १०६, ३ ते १५ जुलै")),
                                    "score": cc.ProgressColumn(tr("Score", "गुण"), min_value=0, max_value=1,
                                                               format="%.2f"),
                                    "area_ha": cc.NumberColumn(tr("Area (ha)", "क्षेत्रफळ (हे.)"), format="%.1f"),
                                    "slope_deg": cc.NumberColumn(tr("Slope (°)", "उतार (°)"), format="%.0f"),
                                    "hv_change_db": cc.NumberColumn(tr("HV change (dB)", "HV बदल (dB)"), format="%.1f"),
                                    "hh_change_db": cc.NumberColumn(tr("HH change (dB)", "HH बदल (dB)"), format="%.1f"),
                                    "coherence": cc.NumberColumn(tr("Coherence", "कोहेरन्स"), format="%.2f"),
                                    "coherence_vs_local": cc.NumberColumn(tr("Coherence vs 1 km", "कोहेरन्स, १ किमीच्या तुलनेत"),
                                                                          format="%.2f"),
                                    "lat": cc.NumberColumn("Lat", format="%.4f"),
                                    "lon": cc.NumberColumn("Lon", format="%.4f"),
                                    "near": tr("Nearest place", "जवळचे ठिकाण"),
                                    "map": cc.LinkColumn(tr("Map", "नकाशा"), display_text=tr("Open", "उघडा"))})
        zsel = (zev.selection.rows if zev and hasattr(zev, "selection") else []) or []
        if zsel:
            zid = df.iloc[zsel[0]]["id"]
            if ss.get("last_zone_pick") != zid:      # act on a new pick only, so "Show the whole area" sticks
                ss.last_zone_pick = zid
                ss.explore_focus = ("zone", zid)
                st.rerun()
        st.page_link("views/5_Field.py", label=tr("Field check list: print it, KML for phones, CSV",
                                                   "क्षेत्रीय तपासणी यादी: छपाई, फोनसाठी KML, CSV"),
                     icon=":material/checklist:")
        st.caption(tr("Place names: © OpenStreetMap contributors (Nominatim). Zones are leads to check, not confirmed "
                      "landslides.", "ठिकाणांची नावे: © OpenStreetMap योगदानकर्ते (Nominatim). क्षेत्रे तपासण्याचे संकेत "
                      "आहेत, निश्चित भूस्खलने नाहीत."))
    else:
        st.info(tr("No slide zones in this run.", "या निकालात भूस्खलन क्षेत्रे नाहीत."))
with tab_w:
    fl = data.flood_patches()
    if fl:
        st.markdown(tr("{n} flood patches: water on {a} where none was recorded from 1984 to 2021. Select one to see "
                       "its radar before and after.", "{n} पुराच्या जागा: {a} रोजीचे पाणी, जिथे १९८४ ते २०२१ मध्ये पाणी "
                       "नोंदवले नव्हते. आधी-नंतरचे रडार पाहण्यासाठी एक निवडा.", n=len(fl), a=ui.day(after)))
        fdf = pd.DataFrame([{"id": p["id"], "area_ha": p["area_ha"], "drop_db": p.get("drop_db"),
                             "near_report": p.get("nearest_event_place", ""), "report_km": p.get("nearest_event_km"),
                             "lat": p["lat"], "lon": p["lon"]} for p in sorted(fl, key=lambda p: p["id"])])
        fev = st.dataframe(fdf, hide_index=True, width="stretch", on_select="rerun", selection_mode="single-row",
                           key="explore_flood_table",
                           column_config={"id": tr("Patch", "जागा"), "area_ha": st.column_config.NumberColumn(
                               tr("Area (ha)", "क्षेत्रफळ (हे.)"), format="%.2f"),
                               "drop_db": st.column_config.NumberColumn(tr("Darker by (dB)", "किती गडद (dB)"),
                                                                        format="%.1f"),
                               "near_report": tr("Nearest reported flood", "सर्वात जवळचा नोंदवलेला पूर"),
                               "report_km": st.column_config.NumberColumn("km", format="%.1f"),
                               "lat": st.column_config.NumberColumn("Lat", format="%.4f"),
                               "lon": st.column_config.NumberColumn("Lon", format="%.4f")})
        fsel = (fev.selection.rows if fev and hasattr(fev, "selection") else []) or []
        if fsel:
            fid = fdf.iloc[fsel[0]]["id"]
            if ss.get("last_flood_pick") != fid:
                ss.last_flood_pick = fid
                ss.explore_focus = ("flood", fid)
                st.rerun()
    ws = data.table("water_stats.csv")
    if ws is not None:
        with st.expander(tr("All water numbers and thresholds", "पाण्याचे सर्व आकडे आणि मर्यादा")):
            st.dataframe(ws, hide_index=True, width="stretch")
with tab_t:
    rain = data.rainfall()
    if rain is not None:
        st.plotly_chart(charts.rainfall(rain, before, after, passes=data.passes()), width="stretch", config={"displayModeBar": False})
    else:
        st.info(tr("Rainfall chart appears here once `data/reference/rainfall.csv` is added.",
                   "`data/reference/rainfall.csv` जोडल्यावर पावसाचा आलेख येथे दिसेल."))
    tl = data.table("timeline.csv")
    if tl is not None and len(tl) > 1:
        st.markdown("**" + tr("Surface area of Pune's rivers and reservoirs on each NISAR pass of this orbit",
                              "या कक्षेतील प्रत्येक निसार निरीक्षणात पुण्याच्या नद्या आणि धरणांचे पृष्ठफळ") + "**")
        st.plotly_chart(charts.timeline(tl), width="stretch", config={"displayModeBar": False})
        st.caption(tr("Dark water on each date, counted inside the area where the JRC record has seen water at least "
                      "once (1984 to 2021), so rain-soaked fields are left out. Every point is the same orbit and radar "
                      "mode; NISAR used a different mode on this orbit from 27 August to 2 October, so those passes are "
                      "not shown.", "प्रत्येक तारखेचे गडद पाणी, JRC नोंदीत (१९८४ ते २०२१) किमान एकदा पाणी दिसलेल्या "
                      "भागात मोजलेले, त्यामुळे पावसाने भिजलेली शेते वगळली आहेत. प्रत्येक बिंदू एकाच कक्षेचा आणि रडार "
                      "पद्धतीचा आहे; २७ ऑगस्ट ते २ ऑक्टोबर दरम्यान निसारने या कक्षेत वेगळी पद्धत वापरली, म्हणून ती "
                      "निरीक्षणे दाखवलेली नाहीत."))
    else:
        st.info("The monsoon timeline appears once more NISAR dates are cropped (`python -m pipeline.crop --timeline`).")
with tab_e:
    val = data.table("validation.csv")
    if val is not None and len(val):
        st.dataframe(val[["id", "type", "date", "place", "observable", "result", "distance_m", "reason",
                          "source_name", "source_url"]], hide_index=True, width="stretch",
                     column_config={"source_url": st.column_config.LinkColumn("source")})
    else:
        st.info("Reported events appear here once `data/reference/events.geojson` is added.")
with tab_d:
    st.markdown(tr("GeoTIFFs are on the analysis grid (UTM zone 43N, 40 m). GeoJSON is in WGS84. File descriptions are "
                   "in English.", "GeoTIFF विश्लेषण ग्रिडवर आहेत (UTM झोन 43N, 40 मी). GeoJSON WGS84 मध्ये आहे. "
                   "फाइल वर्णने इंग्रजीत आहेत."))
    what = {"new_water.tif": "all new water (GeoTIFF)", "flooding.tif": "flooding only, never water before (GeoTIFF)",
            "possible_water_under_cover.tif": "possible water under trees or buildings (GeoTIFF)",
            "slide_zones.tif": "likely slide zones (GeoTIFF)", "hh_change_db.tif": "HH radar change in dB (GeoTIFF)",
            "slide_zones.geojson": "slide zones with scores and nearest place (GeoJSON)",
            "new_water.geojson": "new-water patches, flood and reservoir rise (GeoJSON)",
            "validation.csv": "reported events, matched or missed, with reasons (CSV)",
            "water_stats.csv": "water areas and thresholds (CSV)",
            "crosstrack.json": "second-track check results (JSON)",
            "dem_check.json": "elevation-map check results (JSON)", "metrics.json": "every number in this app (JSON)"}
    links = [f'<li><a href="{url}" download="monsoonlens_{name}">{what.get(name, name)}</a> '
             f'<span class="ml-muted">{size / 1e6:.1f} MB</span></li>' if size >= 1e5 else
             f'<li><a href="{url}" download="monsoonlens_{name}">{what.get(name, name)}</a> '
             f'<span class="ml-muted">{max(size // 1000, 1)} KB</span></li>' for name, url, size in data.downloads()]
    st.markdown("<ul class='ml-downloads'>" + "".join(links) + "</ul>", unsafe_allow_html=True)
ui.sources_line()
