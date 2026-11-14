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
    if nav_b.button(ui.t("back"), disabled=i == 0, use_container_width=True):
        st.session_state.step = max(0, i - 1)
        st.rerun()
    if i < n - 1:
        if nav_n.button(ui.t("next"), type="primary", use_container_width=True):
            st.session_state.step = i + 1
            st.rerun()
    else:
        nav_n.page_link("views/2_Explore.py", label=ui.t("explore"), icon=":material/map:")

with visual:
    if i == 0:
        rain = data.rainfall()
        if rain is not None:
            st.plotly_chart(charts.rainfall(rain, before, after, passes=data.passes()), use_container_width=True,
                            config={"displayModeBar": False})
            st.caption(ui.t("rain_caption", src=rain["source"].iloc[0] if "source" in rain else "see Method"))
        else:
            st.info("Rainfall chart appears here once `data/reference/rainfall.csv` is added.")
    elif i == 1:
        st.markdown(
            f"""<svg viewBox="0 0 560 300" width="100%" role="img" aria-label="Radar pulses pass through cloud; a camera sees only cloud">
  <rect width="560" height="300" fill="#eef1f0" rx="8"/>
  <g fill="#c9d1d6"><ellipse cx="150" cy="120" rx="95" ry="32"/><ellipse cx="210" cy="104" rx="70" ry="30"/>
  <ellipse cx="390" cy="118" rx="100" ry="34"/><ellipse cx="330" cy="102" rx="65" ry="28"/></g>
  <rect x="245" y="22" width="70" height="22" rx="4" fill="{ui.INK}"/><rect x="205" y="28" width="36" height="10" fill="#7d878f"/>
  <rect x="319" y="28" width="36" height="10" fill="#7d878f"/>
  <text x="280" y="16" text-anchor="middle" font-size="13" fill="{ui.INK}" font-family="IBM Plex Sans">NISAR</text>
  <path d="M265 44 L170 250" stroke="#2a78d6" stroke-width="3" stroke-dasharray="10 6"/>
  <path d="M295 44 L390 250" stroke="#7d878f" stroke-width="3"/>
  <text x="150" y="275" font-size="13" fill="{ui.INK}" font-family="IBM Plex Sans">L-band radar: through cloud</text>
  <text x="372" y="275" font-size="13" fill="{ui.INK}" font-family="IBM Plex Sans">camera: stops at cloud</text>
  <rect x="0" y="250" width="560" height="50" fill="#d6dcd2"/><path d="M60 250 Q120 238 200 250 Z" fill="#2a78d6"/>
  <line x1="380" y1="132" x2="400" y2="132" stroke="#7d878f" stroke-width="3"/>
</svg>""", unsafe_allow_html=True)
        st.caption("NISAR's L-band radar (wavelength about 24 cm) works day and night, through cloud and rain.")
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
                             use_container_width=True)
        else:
            st.info("The validation table appears here once reported events (`data/reference/events.geojson`) "
                    "are added and the pipeline is re-run.")
ui.sources_line()
