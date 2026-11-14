import streamlit as st

from lib import data, story, swipe, ui

ui.setup("Overview")
ui.demo_banner()
if not ui.require_results():
    st.stop()

before, after = data.dates()
v = data.value

left, right = st.columns([1.05, 1], gap="large")
with left:
    st.markdown(f'<h1 class="ml-hero">{ui.t("title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="ml-dates">{ui.t("dates_line", b=ui.day(before), a=ui.day(after), y=after[:4])}</div>',
                unsafe_allow_html=True)
    st.markdown(f'<p class="ml-lede">{ui.t("lede", cloud=story.cloud_sentence())}</p>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    if b1.button(ui.t("start_story"), type="primary", icon=":material/auto_stories:", width="stretch"):
        st.switch_page("views/1_Story.py")
    if b2.button(ui.t("explore"), icon=":material/map:", width="stretch"):
        st.switch_page("views/2_Explore.py")
with right:
    imgs = swipe.pair("hh")
    if imgs:
        swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {ui.day(before)}", f"{ui.t('after')}: {ui.day(after)}",
                     height=430, start=50)
        st.caption(ui.t("swipe_caption"))

st.markdown(f"## {ui.t('found')}")
rows = []
if v("water.flood_km2") is not None:
    rows.append(ui.finding(ui.COLORS["rise"], ui.fmt_num(v("water.rise_km2")), " km²", ui.t("rise")))
    rows.append(ui.finding(ui.COLORS["flood"], ui.fmt_num(v("water.flood_km2"), 2), " km²", ui.t("flood")))
else:
    rows.append(ui.finding(ui.COLORS["new_water"], ui.fmt_num(v("water.new_water_km2")), " km²", ui.t("new_water")))
sz, hi = v("slides.zones"), v("slides.high")
rows.append(ui.finding(ui.COLORS["slide_zones"], ui.fmt_num(sz, 0), "", ui.t("slides", high=ui.fmt_num(hi, 0))))
xt = data.crosstrack()
if xt:
    rows.append(ui.finding(ui.INK, ui.t("x_of_y", x=xt["confirmed"], y=xt["scored"]), "",
                           ui.t(("xt_good_small" if xt["small"] else "xt_good") if xt["good"] else "xt_weak",
                                lift=ui.fmt_num(xt["lift"] or 0, 0), cov=xt["coverage"])))
br = v("water.brighter_flat_km2")
rows.append(ui.finding(ui.COLORS["brighter"], ui.fmt_num(br), " km²", ui.t("brighter"), hatch=True))
fh, fo = v("validation.flood.hits"), v("validation.flood.observable")
sh, so = v("validation.slide.hits"), v("validation.slide.observable")
if (fo or 0) + (so or 0) > 0:
    rows.append(ui.finding(ui.INK, f"{(fh or 0) + (sh or 0)} of {(fo or 0) + (so or 0)}", "", ui.t("matched")))
st.markdown("".join(rows), unsafe_allow_html=True)

st.markdown(f"## {ui.t('couldnt')}")
lim = data.limits()
b_iso, a_iso = data.dates()
bullets = []
if lim["flood_miss"]:
    built = ui.t("lim_built_all", n=lim["flood_miss"]) if lim["flood_miss_built"] == lim["flood_miss"] else \
        ui.t("lim_built_some", k=lim["flood_miss_built"], n=lim["flood_miss"])
    bullets.append(ui.t("lim_streets", built_sentence=built))
if lim["peak"]:
    bullets.append(ui.t("lim_timing", p1=ui.day(lim["peak"][0]), p2=ui.day(lim["peak"][1]), b=ui.day(b_iso),
                        a=ui.day(a_iso)))
if lim["res_m"]:
    gentle = ui.t("lim_gentle", n=lim["slide_miss_gentle"]) if lim["slide_miss_gentle"] else ""
    bullets.append(ui.t("lim_small", res=ui.fmt_num(lim["res_m"], 0), smin=ui.fmt_num(lim["slope_min"], 0),
                        smax=ui.fmt_num(lim["slope_max"], 0), gentle_part=gentle))
if lim["hidden_share"] is not None:
    bullets.append(ui.t("lim_hidden", pct=ui.fmt_num(lim["hidden_share"] * 100, 0 if lim["hidden_share"] >= 0.1 else 1)))
bullets.append(ui.t("lim_early"))
st.markdown("\n".join(f"- {x}" for x in bullets))
if lim["zones"]:
    st.markdown(ui.t("lim_lead", u=lim["unreported"], z=lim["zones"]))
st.page_link("views/3_Method.py", label="See how each number was made, and the full validation table",
             icon=":material/fact_check:")
ui.sources_line()
