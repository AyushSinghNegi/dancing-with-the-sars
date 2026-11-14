import streamlit as st
from streamlit_folium import st_folium

from lib import charts, data, maps, story, swipe, ui

ui.setup("Story")
ui.demo_banner()
if not ui.require_results():
    st.stop()

steps = story.steps()
n = len(steps)
if "step" not in st.session_state:
    st.session_state.step = 0
i = st.session_state.step
before, after = data.dates()

st.markdown(f'<div class="ml-step">{ui.t("step", i=i + 1, n=n)}</div>', unsafe_allow_html=True)
st.progress((i + 1) / n)
head, body = steps[i]
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
        nav_n.page_link("views/2_Explore.py", label=ui.t("explore"), icon=":material/map:")

with visual:
    if i == 0:
        rain = data.rainfall()
        if rain is not None:
            st.plotly_chart(charts.rainfall(rain, before, after, passes=data.passes()), width="stretch",
                            config={"displayModeBar": False})
            st.caption(ui.t("rain_caption", src=rain["source"].iloc[0] if "source" in rain else "see Method"))
        else:
            st.info("Rainfall chart appears here once `data/reference/rainfall.csv` is added.")
    elif i == 1:
        c = data.cloud_check()
        if c and c.get("image_path"):
            st.image(c["image_path"], width="stretch")
            st.caption(ui.t("cloud_caption", sensors=", ".join(s.split()[0] if s.split()[0] != "Suomi" else "Suomi NPP"
                                                               for s in c["sensors"]),
                            f=ui.day(c["from"]), t=ui.day(c["to"]), n=c["all_cloud"],
                            p1=ui.day(c["pass_days_broken_cloud"][0]), p2=ui.day(c["pass_days_broken_cloud"][-1]),
                            url=c.get("source_url", "https://worldview.earthdata.nasa.gov")))
        st.caption("NISAR's L-band radar (wavelength about 24 cm) works day and night, through cloud and rain."
                   if ui.lang() == "en" else
                   "निसारचे एल-बँड रडार (तरंगलांबी सुमारे २४ सेंमी) दिवस-रात्र, ढग आणि पावसातूनही काम करते.")
    elif i == 2:
        imgs = swipe.pair("hh")
        if imgs:
            swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {data.nice_date(before, False)}",
                         f"{ui.t('after')}: {data.nice_date(after, False)}", height=500, start=35)
    elif i == 3:
        ui.legend([(ui.COLORS["flood"], ui.t("legend_flood"), "fill"),
                   (ui.COLORS["rise"], ui.t("legend_rise"), "fill"),
                   (ui.COLORS["slide_zones"], ui.t("legend_slides"), "outline"),
                   (ui.COLORS["brighter"], ui.t("legend_brighter"), "hatch"),
                   (ui.COLORS["permanent"], ui.t("legend_permanent"), "fill"),
                   (ui.INK, ui.t("legend_events"), "dot")])
        m = maps.build(basemap="Light", zoom=10, collapsed=True)
        st_folium(m, height=470, use_container_width=True, returned_objects=[], key="story_map")
    else:
        val = data.table("validation.csv")
        summ = data.metrics().get("validation", {})
        if val is not None and len(val):
            obs = val[val["observable"] == "yes"]
            rows = []
            for key, label in (("flood", "matched_floods"), ("slide", "matched_slides")):
                s = summ.get(key, {})
                rows.append(ui.finding(ui.INK, ui.t("x_of_y", x=s.get("hits", 0), y=s.get("observable", 0)), "",
                                       ui.t(label)))
            st.markdown("".join(rows), unsafe_allow_html=True)
            misses = val[val["result"].isin(["miss", "not observable"])]
            if len(misses):
                st.markdown(f"**{ui.t('fell_short')}**")
                st.dataframe(misses[["place", "type", "date", "result", "reason"]], hide_index=True,
                             width="stretch")
        else:
            st.info("The validation table appears here once reported events (`data/reference/events.geojson`) "
                    "are added and the pipeline is re-run.")
ui.sources_line()
