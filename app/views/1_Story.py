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

st.markdown(f'<div class="ml-step">Step {i + 1} of {n}</div>', unsafe_allow_html=True)
st.progress((i + 1) / n)
head, body = steps[i]
text, visual = st.columns([0.9, 1.4], gap="large")
with text:
    st.markdown(f"## {head}")
    st.markdown(f'<p class="ml-lede">{body}</p>', unsafe_allow_html=True)
    nav_b, nav_n = st.columns(2)
    if nav_b.button("Back", disabled=i == 0, use_container_width=True):
        st.session_state.step = max(0, i - 1)
        st.rerun()
    if i < n - 1:
        if nav_n.button("Next", type="primary", use_container_width=True):
            st.session_state.step = i + 1
            st.rerun()
    else:
        nav_n.page_link("views/2_Explore.py", label=ui.t("explore"), icon=":material/map:")

with visual:
    if i == 0:
        rain = data.rainfall()
        if rain is not None:
            st.plotly_chart(charts.rainfall(rain, before, after), use_container_width=True,
                            config={"displayModeBar": False})
            st.caption(f"Daily rainfall averaged over the study box. Source: {rain['source'].iloc[0] if 'source' in rain else 'GPM IMERG'}.")
        else:
            st.info("Rainfall chart appears here once `data/reference/rainfall.csv` (GPM IMERG daily) is added.")
    elif i == 1:
        st.image(str(data.ROOT / "app/static/radar-clouds.svg"), use_container_width=True)
        st.caption("NISAR's L-band radar (wavelength about 24 cm) works day and night, through cloud and rain.")
    elif i == 2:
        imgs = swipe.pair("hh")
        if imgs:
            swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {data.nice_date(before, False)}",
                         f"{ui.t('after')}: {data.nice_date(after, False)}", height=500, start=35)
    elif i == 3:
        ui.legend([(ui.COLORS["new_water"], ui.t("legend_new_water"), "fill"),
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
            for key, label in (("flood", "reported floods"), ("slide", "reported landslides")):
                if key == "flood" and not data.water_usable():
                    st.info("Flood reports were not scored because the water classification failed its quality check.")
                    continue
                s = summ.get(key, {})
                rows.append(ui.finding(ui.INK, f"{s.get('hits', 0)} of {s.get('observable', 0)}", "",
                                       f"{label} that radar could observe had a detection nearby"))
            st.markdown("".join(rows), unsafe_allow_html=True)
            misses = val[val["result"].isin(["miss", "not observable"])]
            if len(misses):
                st.markdown("**Where radar fell short, and why**")
                st.dataframe(misses[["place", "type", "date", "result", "reason"]], hide_index=True,
                             use_container_width=True)
        else:
            st.info("The validation table appears here once reported events (`data/reference/events.geojson`) "
                    "are added and the pipeline is re-run.")
ui.sources_line()
