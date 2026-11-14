import streamlit as st
from streamlit_folium import st_folium

from lib import charts, data, evidence, maps, story, swipe, ui

ui.setup("Story")
ui.demo_banner()
if not ui.require_results():
    st.stop()

steps = story.steps()
n = len(steps)
if "step" not in st.session_state:
    st.session_state.step = 0
i = st.session_state.step = min(st.session_state.step, n - 1)
before, after = data.dates()

st.markdown(f'<div class="ml-step">{ui.t("step", i=i + 1, n=n)}</div>', unsafe_allow_html=True)
st.progress((i + 1) / n)
head, body, key = steps[i]
text, visual = st.columns([0.9, 1.4], gap="large")
with text:
    st.markdown(f"## {head}")
    st.markdown(f'<p class="ml-lede">{body}</p>', unsafe_allow_html=True)
    nav_b, nav_n = st.columns(2)
    if nav_b.button(ui.t("back"), disabled=i == 0, width="stretch"):
        st.session_state.step = max(0, i - 1)
        st.rerun()
    if i < n - 1:
        if nav_n.button(ui.t("next"), type="primary", width="stretch"):
            st.session_state.step = i + 1
            st.rerun()
    else:
        if nav_n.button(ui.tr("Check a place", "एखादे ठिकाण तपासा"), type="primary", width="stretch",
                        icon=":material/location_on:"):
            st.switch_page("views/4_Place.py")
        st.markdown(f'<p class="ml-kicker" style="margin-top:1rem">{ui.tr("Where next", "पुढे कुठे")}</p>',
                    unsafe_allow_html=True)
        st.page_link("views/5_Field.py", label=ui.tr("Field check list for district teams",
                                                     "जिल्हा पथकांसाठी क्षेत्रीय तपासणी यादी"), icon=":material/checklist:")
        st.page_link("views/2_Explore.py", label=ui.t("explore"), icon=":material/map:")
        st.page_link("views/3_Method.py", label=ui.tr("Method and limits", "पद्धत आणि मर्यादा"),
                     icon=":material/science:")

with visual:
    if key == "rain":
        rain = data.rainfall()
        if rain is not None:
            st.plotly_chart(charts.rainfall(rain, before, after, passes=data.passes()), width="stretch",
                            config={"displayModeBar": False})
            st.caption(ui.t("rain_caption", src=rain["source"].iloc[0] if "source" in rain else "see Method"))
        else:
            st.info("Rainfall chart appears here once `data/reference/rainfall.csv` is added.")
    elif key == "cloud":
        c = data.cloud_check()
        if c and c.get("image_path"):
            st.image(c["image_path"], width="stretch")
            st.caption(ui.t("cloud_caption", sensors=", ".join(s.split()[0] if s.split()[0] != "Suomi" else "Suomi NPP"
                                                               for s in c["sensors"]),
                            f=ui.day(c["from"]), t=ui.day(c["to"]), n=c["all_cloud"],
                            p1=ui.day(c["pass_days_broken_cloud"][0]), p2=ui.day(c["pass_days_broken_cloud"][-1]),
                            url=c.get("source_url", "https://worldview.earthdata.nasa.gov")))
        st.caption(ui.tr("NISAR's L-band radar (wavelength about 24 cm) works day and night, through cloud and rain.",
                         "निसारचे एल-बँड रडार (तरंगलांबी सुमारे २४ सेंमी) दिवस-रात्र, ढग आणि पावसातूनही काम करते."))
    elif key == "swipe":
        imgs = swipe.pair("hh")
        if imgs:
            swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {data.nice_date(before, False)}",
                         f"{ui.t('after')}: {data.nice_date(after, False)}", height=500, start=35)
    elif key == "changed":
        ui.legend([(ui.COLORS["flood"], ui.t("legend_flood"), "fill"),
                   (ui.COLORS["rise"], ui.t("legend_rise"), "fill"),
                   (ui.COLORS["slide_zones"], ui.t("legend_slides"), "outline"),
                   (ui.COLORS["brighter"], ui.t("legend_brighter"), "hatch"),
                   (ui.COLORS["permanent"], ui.t("legend_permanent"), "fill"),
                   (None, ui.t("legend_events"), "dot")])
        m = maps.build(zoom=10, collapsed=True)
        st_folium(m, height=470, use_container_width=True, returned_objects=[], key=f"story_map_{ui.dark()}")
    elif key == "weeks":
        tl = story.timeline_rows()
        st.plotly_chart(charts.timeline(tl), width="stretch", config={"displayModeBar": False})
        st.caption(ui.t("timeline_caption"))
        if data.season_dates() and st.button(ui.tr("Watch the water spread on the map", "नकाशावर पाणी पसरताना पाहा"),
                                             icon=":material/play_circle:"):
            st.session_state["explore_mode"] = "season"
            st.switch_page("views/2_Explore.py")
    else:
        val = data.table("validation.csv")
        summ = data.metrics().get("validation", {})
        if val is not None and len(val):
            obs = val[val["observable"] == "yes"]
            rows = []
            for key, label in (("flood", "matched_floods"), ("slide", "matched_slides")):
                s = summ.get(key, {})
                rows.append(ui.finding("currentColor", ui.t("x_of_y", x=s.get("hits", 0), y=s.get("observable", 0)), "",
                                       ui.t(label)))
            st.markdown("".join(rows), unsafe_allow_html=True)
            dc = data.metrics().get("dem_check") or {}
            rh = dc.get("reported_slide_hits") or {}
            if rh and rh.get("nasadem", 0) < rh.get("main", 0):
                hits = [s for s in dc["reported_slides"] if s["main"] == "hit"]
                d = ui.t("and_join", a=f"{hits[0]['main_distance_m'] / 1000:.1f}",
                         b=f"{hits[-1]['main_distance_m'] / 1000:.1f}") if len(hits) > 1 else \
                    f"{hits[0]['main_distance_m'] / 1000:.1f}"
                st.caption(ui.t("slide_fragile_one", d=d) if len(rh["main_hit_zones"]) == 1 and len(hits) == 2
                           else ui.t("slide_fragile", k=rh["nasadem"], n=rh["main"]))
            misses = val[val["result"].isin(["miss", "not observable"])]
            if len(misses):
                st.markdown(f"**{ui.t('fell_short')}**")
                tr = ui.tr
                shown = misses[["place", "type", "date", "result", "reason"]].copy()
                shown["type"] = shown["type"].astype(str).map(evidence.type_word)
                shown["result"] = shown["result"].map({"miss": tr("radar missed it", "रडारला दिसले नाही"),
                                                       "not observable": tr("radar could not observe it",
                                                                            "रडारला पाहता आले नाही")}).fillna(shown["result"])
                st.dataframe(shown, hide_index=True, width="stretch",
                             column_config={"place": tr("Place", "ठिकाण"), "type": tr("Event", "घटना"),
                                            "date": tr("Date", "तारीख"), "result": tr("Result", "निकाल"),
                                            "reason": tr("Why (in English)", "कारण (इंग्रजीत)")})
        else:
            st.info("The validation table appears here once reported events (`data/reference/events.geojson`) "
                    "are added and the pipeline is re-run.")
ui.sources_line()
