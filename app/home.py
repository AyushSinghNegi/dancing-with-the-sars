import streamlit as st

from lib import data, swipe, ui

ui.setup("Overview")
ui.demo_banner()
if not ui.require_results():
    st.stop()

before, after = data.dates()
v = data.value

left, right = st.columns([1.05, 1], gap="large")
with left:
    st.markdown(f'<h1 class="ml-hero">{ui.t("title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="ml-dates">NISAR L-band radar passes on {data.nice_date(before, False)} and '
                f'{data.nice_date(after)}, Pune district, India</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="ml-lede">{ui.t("lede")}</p>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    if b1.button(ui.t("start_story"), type="primary", icon=":material/auto_stories:", use_container_width=True):
        st.switch_page("views/1_Story.py")
    if b2.button(ui.t("explore"), icon=":material/map:", use_container_width=True):
        st.switch_page("views/2_Explore.py")
with right:
    imgs = swipe.pair("hh")
    if imgs:
        swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {data.nice_date(before, False)}",
                     f"{ui.t('after')}: {data.nice_date(after, False)}", height=430, start=50)
        st.caption(ui.t("swipe_caption"))

st.markdown(f"## {ui.t('found')}")
rows = []
nw = v("water.new_water_km2")
rows.append(ui.finding(ui.COLORS["new_water"], ui.fmt_num(nw), " km²", ui.t("new_water")))
sz, hi = v("slides.zones"), v("slides.high")
rows.append(ui.finding(ui.COLORS["slide_zones"], ui.fmt_num(sz, 0), "", ui.t("slides", high=ui.fmt_num(hi, 0))))
br = v("water.brighter_flat_km2")
rows.append(ui.finding(ui.COLORS["brighter"], ui.fmt_num(br), " km²", ui.t("brighter"), hatch=True))
fh, fo = v("validation.flood.hits"), v("validation.flood.observable")
sh, so = v("validation.slide.hits"), v("validation.slide.observable")
if (fo or 0) + (so or 0) > 0:
    rows.append(ui.finding(ui.INK, f"{(fh or 0) + (sh or 0)} of {(fo or 0) + (so or 0)}", "", ui.t("matched")))
st.markdown("".join(rows), unsafe_allow_html=True)

st.markdown(f"## {ui.t('couldnt')}")
st.markdown(
    "- **Streets between tall buildings.** Radar bounces off walls and back to the satellite, so flooded city "
    "streets can look bright, not dark. We mark those places as *possible water*, and never count them as flood.\n"
    f"- **Water that drained early.** The second pass was on {data.nice_date(after)}. Floods that came and went between the "
    "passes leave no trace.\n"
    "- **Small slides.** Our map has 40 m pixels. A slide narrower than that can slip through.\n"
    "- **Every detection is a lead, not a verdict.** Slide zones are places to check on the ground or in "
    "local reports.")
st.page_link("views/3_Method.py", label="See how each number was made, and the full validation table",
             icon=":material/fact_check:")
ui.sources_line()
