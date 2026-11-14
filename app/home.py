import html

import streamlit as st

from lib import checks, data, hero, story, swipe, ui

ui.setup("Overview")
ui.demo_banner()
if not ui.require_results():
    st.stop()

tr = ui.tr
before, after = data.dates()
v = data.value
m = data.metrics()
th = m.get("thresholds", {})

# ---------------------------------------------------------------- hero
np_ = data.next_pass()
with st.container(key="hero"):
    left, right = st.columns([1.24, 1], gap="large", vertical_alignment="center")
    with left:
        if np_:
            st.markdown(f'<p class="ml-kicker"><i></i>{tr("Next expected NISAR pass over Pune: {d}", "पुण्यावरील पुढचे अपेक्षित निसार निरीक्षण: {d}", d=ui.date(np_[1]))}</p>',
                        unsafe_allow_html=True)
        st.markdown(f'<h1 class="ml-hero">{ui.t("title")}</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="ml-dates">{ui.t("dates_line", b=ui.day(before), a=ui.day(after), y=after[:4])}</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<p class="ml-lede">{ui.t("lede", cloud=story.cloud_sentence())}</p>', unsafe_allow_html=True)
        with st.container(horizontal=True, gap="small", key="herobtns"):
            if st.button(ui.t("start_story"), type="primary", icon=":material/auto_stories:", width="content"):
                st.switch_page("views/1_Story.py")
            if st.button(tr("Explore the map", "नकाशा पाहा"), icon=":material/map:", width="content"):
                st.switch_page("views/2_Explore.py")
            if st.button(tr("Check a place", "एखादे ठिकाण तपासा"), icon=":material/location_on:", width="content"):
                st.switch_page("views/4_Place.py")
    with right:
        if not hero.render(after, height=440):
            imgs = swipe.pair("hh")
            if imgs:
                swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {ui.day(before)}", f"{ui.t('after')}: {ui.day(after)}",
                             height=430, start=50)


ICONS = {  # simple 24 px line icons for the three audiences
    ":material/location_on:": '<path d="M12 21s-6.5-6.6-6.5-11.5a6.5 6.5 0 0 1 13 0C18.5 14.4 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.4"/>',
    ":material/checklist:": '<path d="M4 6.5l1.6 1.6L8.5 5M4 12.5l1.6 1.6 2.9-3.1M4 18.5l1.6 1.6 2.9-3.1M11 7h9M11 13h9M11 19h9"/>',
    ":material/science:": '<path d="M9.5 3h5M10.5 3v5.5L5 18.5A1.7 1.7 0 0 0 6.5 21h11a1.7 1.7 0 0 0 1.5-2.5L13.5 8.5V3M7.5 15h9"/>',
}


def icon_html(name):
    return (f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, "")}</svg>')


def card(color, number, unit, label, sure, hatch=False):
    return (f'<div class="ml-stat{" hatch" if hatch else ""}" style="--c:{color}"><div class="k">{html.escape(number)}'
            f'<small>{html.escape(unit)}</small></div><p class="lbl">{html.escape(label)}</p>'
            + (f'<p class="sure">{html.escape(sure)}</p>' if sure else "") + "</div>")


# ---------------------------------------------------------------- what the radar found
st.markdown(f"## {ui.t('found')}")
sens = (m.get("sensitivity") or {}).get("range", {})
dc = m.get("dem_check") or {}
cards = []
if v("water.flood_km2") is not None:
    r = sens.get("rise_km2")
    cards.append(card(ui.COLORS["rise"], ui.fmt_num(v("water.rise_km2")), "km²", ui.t("rise"),
                      tr("With the water threshold 1 dB lower or higher: {a} to {b} km².",
                         "पाण्याची मर्यादा १ dB कमी-जास्त केल्यास: {a} ते {b} चौ. किमी.", a=ui.fmt_num(r[0]),
                         b=ui.fmt_num(r[1])) if r else ""))
    f = sens.get("flood_km2")
    cards.append(card(ui.COLORS["flood"], ui.fmt_num(v("water.flood_km2"), 2), "km²", ui.t("flood"),
                      tr("Depends strongly on the water threshold: {a} to {b} km² with it moved 1 dB either way.",
                         "पाण्याच्या मर्यादेवर खूप अवलंबून: ती १ dB कमी-जास्त केल्यास {a} ते {b} चौ. किमी.",
                         a=ui.fmt_num(f[0], 2), b=ui.fmt_num(f[1], 1)) if f else ""))
sz, hi = v("slides.zones"), v("slides.high")
cards.append(card(ui.COLORS["slide_zones"], ui.fmt_num(sz, 0), "",
                  tr("likely slide zones on slopes of {a}° to {b}°, {h} of them high confidence",
                     "{a}° ते {b}° उतारावरील संभाव्य भूस्खलन क्षेत्रे, त्यापैकी {h} उच्च खात्रीची",
                     a=ui.fmt_num(th.get("slide_min_slope_deg", 15), 0), b=ui.fmt_num(th.get("slide_max_slope_deg", 45), 0),
                     h=ui.fmt_num(hi, 0)),
                  tr("Leads to check, not verdicts: {u} have no reported event within 2 km.",
                     "तपासण्याचे संकेत, निर्णय नाहीत: {u} क्षेत्रांच्या २ किमी परिसरात कोणतीही घटना नोंदवलेली नाही.",
                     u=ui.fmt_num(v("validation.unreported_slide_zones") or 0, 0))))
tl = story.timeline_rows()
if tl is not None:
    first, last = tl.iloc[0], tl.iloc[-1]
    cards.append(card(ui.COLORS["new_water"], ui.fmt_num(last["water_in_jrc_extent_km2"], 0), "km²",
                      tr("of open water in rivers and reservoirs on {d}, up from {v} km² on {f}",
                         "{d} रोजी नद्या आणि धरणांतील उघडे पाणी, {f} रोजी {v} चौ. किमी होते", d=ui.day(last["date"]),
                         v=ui.fmt_num(first["water_in_jrc_extent_km2"], 0), f=ui.day(first["date"])),
                      tr("{n} NISAR passes, same orbit and radar mode. Watch it on the map's season slider.",
                         "{n} निसार निरीक्षणे, एकच कक्षा आणि रडार पद्धत. नकाशावरील हंगाम स्लायडरवर पाहा.", n=len(tl))))
cards.append(card(ui.COLORS["brighter"], ui.fmt_num(v("water.brighter_flat_km2")), "km²", ui.t("brighter"),
                  tr("Shown as possible water, never added to the flood figure.",
                     "संभाव्य पाणी म्हणून दाखवले, पुराच्या आकड्यात कधीच मिळवले नाही."), hatch=True))
st.markdown(f'<div lang="{ui.lang()}" class="ml-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- how we checked it
st.markdown(f"## {tr('How we checked it', 'आम्ही कसे तपासले')}")
checks.render()

# ---------------------------------------------------------------- who it is for
st.markdown(f"## {tr('Who it is for', 'हे कोणासाठी')}")
paths = [
    (tr("People who live there", "तिथे राहणारे लोक"), tr(
        "Pick your village or town and see what NISAR found within 2, 5 or 10 km, with a link you can send on.",
        "तुमचे गाव किंवा शहर निवडा आणि निसारला २, ५ किंवा १० किमीच्या आत काय सापडले ते पाहा, पुढे पाठवता येईल अशा लिंकसह."),
     "views/4_Place.py", tr("Check a place", "एखादे ठिकाण तपासा"), ":material/location_on:"),
    (tr("District disaster teams", "जिल्हा आपत्ती पथके"), tr(
        "A ranked check list of likely slide zones with radar images of each spot, a printable sheet and KML for phones.",
        "संभाव्य भूस्खलन क्षेत्रांची क्रमवार यादी, प्रत्येक जागेच्या रडार प्रतिमा, छापण्याजोगी यादी आणि फोनसाठी KML."),
     "views/5_Field.py", tr("Field check list", "क्षेत्रीय तपासणी यादी"), ":material/checklist:"),
    (tr("Researchers and journalists", "संशोधक आणि पत्रकार"), tr(
        "Every number traced to its NISAR file, the checks behind it, and the maps as GeoTIFF and GeoJSON.",
        "प्रत्येक आकडा त्याच्या निसार फाइलपर्यंत, त्यामागच्या तपासण्या, आणि नकाशे GeoTIFF व GeoJSON मध्ये."),
     "views/3_Method.py", tr("Method and data", "पद्धत आणि डेटा"), ":material/science:"),
]
with st.container(key="paths"):
    cols = st.columns(3)
for c, (title, desc, page, label, icon), col in zip(cols, paths, ("#3d8ef0", "#f0743a", "#6fe3ff")):
    with c.container(border=True):
        st.markdown(f'<div class="ml-path-ic" style="--c:{col}"><span>{icon_html(icon)}</span></div>', unsafe_allow_html=True)
        st.markdown(f"### {title}")
        st.markdown(f'<p class="ml-pathd">{html.escape(desc)}</p>', unsafe_allow_html=True)
        st.page_link(page, label=label, icon=icon)

# ---------------------------------------------------------------- what radar could not see
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
if np_:
    st.markdown(f'<div class="ml-pass"><span>🛰️</span><span>' + tr(
        "NISAR passes over Pune every 12 days, cloud or not. Last pass in our data: <b>{l}</b>; if it keeps its 12-day "
        "repeat, the next is <b>{n}</b>. The same open code turns each new pass into these maps and lists.",
        "निसार दर १२ दिवसांनी पुण्यावरून जातो, ढग असोत वा नसोत. आमच्या डेटातील शेवटचे निरीक्षण: <b>{l}</b>; १२ "
        "दिवसांचे चक्र कायम राहिल्यास पुढचे <b>{n}</b>. तोच मुक्त कोड प्रत्येक नव्या निरीक्षणाचे हे नकाशे आणि याद्या बनवतो.",
        l=ui.date(np_[0]), n=ui.date(np_[1])) + "</span></div>", unsafe_allow_html=True)
st.page_link("views/3_Method.py", label=tr("See how each number was made, and the full validation table",
                                          "प्रत्येक आकडा कसा तयार झाला आणि संपूर्ण पडताळणी तक्ता पाहा"),
             icon=":material/fact_check:")
ui.sources_line()
