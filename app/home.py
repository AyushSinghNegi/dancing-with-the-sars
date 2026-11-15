import html

import streamlit as st

from lib import checks, data, hero, story, swipe, ui, view3d

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


# ---------------------------------------------------------------- how it works, in three steps
HOW = [
    ('<path d="M4 9l4-4 3 3-4 4zM13 16l4-4 3 3-4 4zM9.5 10.5l4 4M14 7a6 6 0 0 1 3 3M14 3.5a9.5 9.5 0 0 1 6.5 6.5"/>',
     tr("A satellite passes", "उपग्रह वरून जातो"),
     tr("NISAR flies over Pune every 12 days, day or night.", "निसार दर १२ दिवसांनी, दिवसा किंवा रात्री, पुण्यावरून जातो.")),
    ('<path d="M6.5 9.5a4 4 0 0 1 7.6-1.7A3.2 3.2 0 1 1 15 14H7a3 3 0 0 1-.5-4.5zM9 17v4M12 17v4M15 17v4"/>',
     tr("Radar sees through cloud", "रडार ढगांपलीकडे पाहते"),
     tr("Its radar passes through cloud and rain. Calm water looks dark.",
        "त्याचे रडार ढग आणि पावसातूनही जाते. शांत पाणी गडद दिसते.")),
    ('<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2zM9 4v14M15 6v14"/>',
     tr("We map the change", "आम्ही बदल नकाशावर दाखवतो"),
     tr("We compare passes before and after the storm and map what changed.",
        "वादळाआधीची आणि नंतरची निरीक्षणे ताडून आम्ही काय बदलले ते नकाशावर दाखवतो.")),
]
st.markdown(f"## {tr('How it works', 'हे कसे काम करते')}")
st.markdown('<ol class="ml-how">' + "".join(
    f'<li><span class="ic"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" '
    f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ic}</svg></span>'
    f'<b>{html.escape(t_)}</b><p>{html.escape(d_)}</p></li>' for ic, t_, d_ in HOW) + "</ol>", unsafe_allow_html=True)

# ---------------------------------------------------------------- 3D tour
if view3d.meta():
    st.markdown(f"## {tr('See it in 3D', '३D मध्ये पाहा')}")
    st.markdown('<p class="ml-sub">' + tr("A one-minute tour of what NISAR found, on a model of the land.",
                                          "जमिनीच्या मॉडेलवर निसारला काय सापडले याचा एका मिनिटाचा फेरफटका.") + "</p>",
                unsafe_allow_html=True)
    view3d.render(height=560, key="home3d")

# ---------------------------------------------------------------- what the radar found
st.markdown(f"## {ui.t('found')}")
sens = (m.get("sensitivity") or {}).get("range", {})
dc = m.get("dem_check") or {}
cards = []
if v("water.flood_km2") is not None:
    r = sens.get("rise_km2")
    cards.append(card(ui.COLORS["rise"], ui.fmt_num(v("water.rise_km2")), "km²", ui.t("rise"),
                      tr("Could be {a} to {b} km², depending on the water threshold.",
                         "पाण्याच्या मर्यादेनुसार {a} ते {b} चौ. किमी असू शकते.", a=ui.fmt_num(r[0]),
                         b=ui.fmt_num(r[1])) if r else ""))
    f = sens.get("flood_km2")
    cards.append(card(ui.COLORS["flood"], ui.fmt_num(v("water.flood_km2"), 2), "km²", ui.t("flood"),
                      tr("Could be {a} to {b} km²: very sensitive to the water threshold.",
                         "{a} ते {b} चौ. किमी असू शकते: पाण्याच्या मर्यादेवर खूप अवलंबून.",
                         a=ui.fmt_num(f[0], 2), b=ui.fmt_num(f[1], 1)) if f else ""))
sz, hi = v("slides.zones"), v("slides.high")
cards.append(card(ui.COLORS["slide_zones"], ui.fmt_num(sz, 0), "",
                  tr("likely slide zones on steep slopes, {h} of them high confidence",
                     "तीव्र उतारांवरील संभाव्य भूस्खलन क्षेत्रे, त्यापैकी {h} उच्च खात्रीची",
                     a=ui.fmt_num(th.get("slide_min_slope_deg", 15), 0), b=ui.fmt_num(th.get("slide_max_slope_deg", 45), 0),
                     h=ui.fmt_num(hi, 0)),
                  tr("Leads to check: {u} have no reported event within 2 km.",
                     "तपासण्याच्या जागा: {u} क्षेत्रांच्या २ किमी परिसरात कोणतीही घटना नोंदवलेली नाही.",
                     u=ui.fmt_num(v("validation.unreported_slide_zones") or 0, 0))))
tl = story.timeline_rows()
if tl is not None:
    first, last = tl.iloc[0], tl.iloc[-1]
    cards.append(card(ui.COLORS["new_water"], ui.fmt_num(last["water_in_jrc_extent_km2"], 0), "km²",
                      tr("of open water in rivers and reservoirs on {d}, up from {v} km² on {f}",
                         "{d} रोजी नद्या आणि धरणांतील उघडे पाणी, {f} रोजी {v} चौ. किमी होते", d=ui.day(last["date"]),
                         v=ui.fmt_num(first["water_in_jrc_extent_km2"], 0), f=ui.day(first["date"])),
                      tr("{n} NISAR passes, same orbit.", "{n} निसार निरीक्षणे, एकच कक्षा.", n=len(tl))))
cards.append(card(ui.COLORS["brighter"], ui.fmt_num(v("water.brighter_flat_km2")), "km²", ui.t("brighter"), "",
                  hatch=True))
st.markdown(f'<div lang="{ui.lang()}" class="ml-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- how we checked it
st.markdown(f"## {tr('How we checked it', 'आम्ही कसे तपासले')}")
checks.render()

# ---------------------------------------------------------------- who it is for
st.markdown(f"## {tr('Who it is for', 'हे कोणासाठी')}")
paths = [
    (tr("People who live there", "तिथे राहणारे लोक"), tr(
        "See what NISAR found near your village or town.", "तुमच्या गावाजवळ किंवा शहराजवळ निसारला काय सापडले ते पाहा."),
     "views/4_Place.py", tr("Check a place", "एखादे ठिकाण तपासा"), ":material/location_on:"),
    (tr("District disaster teams", "जिल्हा आपत्ती पथके"), tr(
        "A ranked list of slide zones to check, with radar images, for print and phones.",
        "तपासण्याजोग्या भूस्खलन क्षेत्रांची क्रमवार यादी, रडार प्रतिमांसह, छपाई आणि फोनसाठी."),
     "views/5_Field.py", tr("Field check list", "क्षेत्रीय तपासणी यादी"), ":material/checklist:"),
    (tr("Researchers and journalists", "संशोधक आणि पत्रकार"), tr(
        "Every number traced to its NISAR file, with the checks and the data.",
        "प्रत्येक आकडा त्याच्या निसार फाइलपर्यंत, तपासण्या आणि डेटासह."),
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
LIM = [(tr("Water between buildings", "इमारतींमधले पाणी"),
        tr("Radar bounces off walls, so city flooding is under-counted.",
           "रडार भिंतींवरून परावर्तित होते, म्हणून शहरातील पूर कमी मोजला जातो.")),
       (tr("Between passes", "दोन निरीक्षणांच्या मधे"),
        tr("Water that came and went between {b} and {a} is not seen.", "{b} ते {a} दरम्यान आलेले आणि ओसरलेले पाणी दिसत नाही.",
           b=ui.day(b_iso), a=ui.day(a_iso))),
       (tr("Small slides", "लहान भूस्खलने"),
        tr("Slides narrower than about {r} m can slip through.", "सुमारे {r} मीटरपेक्षा अरुंद भूस्खलने सुटू शकतात.",
           r=ui.fmt_num((lim["res_m"] or 40) * 2, 0)))]
if lim["hidden_share"] is not None:
    LIM.append((tr("Hidden slopes", "लपलेले उतार"),
                tr("{p}% of steep ground faces away from the radar and is left out.",
                   "तीव्र उतारांपैकी {p}% भाग रडारपासून दूर वळलेला आहे, तो वगळला आहे.",
                   p=ui.fmt_num(lim["hidden_share"] * 100, 0 if lim["hidden_share"] >= 0.1 else 1))))
LIM.append((tr("Early data", "सुरुवातीचा डेटा"),
            tr("These NISAR products are provisional; the numbers may shift.",
               "ही निसार उत्पादने तात्पुरती आहेत; आकडे बदलू शकतात.")))
st.markdown('<div class="ml-cardgrid">' + "".join(
    f'<div class="lim"><b>{html.escape(t_)}</b><p>{html.escape(d_)}</p></div>' for t_, d_ in LIM) + "</div>",
    unsafe_allow_html=True)
st.page_link("views/3_Method.py", label=tr("See how each number was made, and the full validation table",
                                          "प्रत्येक आकडा कसा तयार झाला आणि संपूर्ण पडताळणी तक्ता पाहा"),
             icon=":material/fact_check:")
ui.sources_line()
