import streamlit as st
import streamlit.components.v1 as components
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
tr = ui.tr
track = (data.metrics().get("sources") or [{}])[0].get("granule_id", "").split("_")[5:6]
track = track[0] if track else ""

SHORT = {"rain": tr("The rain", "पाऊस"), "cloud": tr("Cloud", "ढग"), "swipe": tr("Before and after", "आधी आणि नंतर"),
         "changed": tr("What changed", "काय बदलले"), "weeks": tr("The weeks after", "नंतरचे आठवडे"),
         "limits": tr("Limits", "मर्यादा")}
INSTR = {"rain": tr("Rain measured from space: NASA GPM IMERG, daily", "अवकाशातून मोजलेला पाऊस: नासा GPM IMERG, रोजचा"),
         "cloud": tr("What optical satellites saw: NASA Worldview", "प्रकाशीय उपग्रहांना काय दिसले: नासा वर्ल्डव्ह्यू"),
         "swipe": tr("NISAR L-band radar, HH, track {t}", "निसार एल-बँड रडार, HH, मार्ग {t}", t=track),
         "changed": tr("NISAR findings, {b} to {a}", "निसारचे निष्कर्ष, {b} ते {a}", b=ui.day(before), a=ui.day(after)),
         "weeks": tr("NISAR, every pass of track {t} in the same radar mode", "निसार, एकाच रडार पद्धतीतील मार्ग {t} ची प्रत्येक निरीक्षणे",
                     t=track),
         "limits": tr("Reported events checked against the radar", "रडारशी ताडून पाहिलेल्या नोंदवलेल्या घटना")}


def go(k):
    st.session_state.step = k


# ---------------------------------------------------------------- chapter rail: one stop per chapter on an orbit track
with st.container(horizontal=True, key="rail"):
    for k, (_, _, key_k) in enumerate(steps):
        st.button(SHORT.get(key_k, str(k + 1)), key=f"rail_{k}", type="primary" if k == i else "secondary",
                  on_click=go, args=(k,), width="stretch")
done = (i / max(n - 1, 1)) * 100
st.markdown(f"<style>.st-key-rail::before {{ background: linear-gradient(90deg, var(--ml-water) {done:.1f}%, "
            f"var(--ml-line) {done:.1f}%); }}"
            + "".join(f".st-key-rail_{k} button::before {{ background: var(--ml-water); border-color: var(--ml-water); }}"
                      for k in range(i)) + "</style>", unsafe_allow_html=True)

head, body, key = steps[i]
with st.container(key=f"chapter{i}"):
    text, visual = st.columns([0.9, 1.4], gap="large")
with text:
    st.markdown(f'<p class="ml-kicker">{ui.t("step", i=i + 1, n=n)}</p>', unsafe_allow_html=True)
    st.markdown(f"## {head}")
    st.markdown(f'<p class="ml-lede">{body}</p>', unsafe_allow_html=True)
    nav_b, nav_n = st.columns(2)
    nav_b.button(ui.t("back"), disabled=i == 0, width="stretch", key="story_back", icon=":material/arrow_back:",
                 on_click=go, args=(max(0, i - 1),))
    if i < n - 1:
        nav_n.button(ui.t("next"), type="primary", width="stretch", key="story_next",
                     icon=":material/arrow_forward:", on_click=go, args=(i + 1,))
    else:
        if nav_n.button(tr("Check a place", "एखादे ठिकाण तपासा"), type="primary", width="stretch",
                        icon=":material/location_on:", key="story_next"):
            st.switch_page("views/4_Place.py")
    st.markdown('<p class="ml-hint">' + tr("Tip: the ← and → keys move between chapters.",
                                           "टीप: ← आणि → कळांनी प्रकरणांमध्ये पुढे-मागे जा.") + "</p>",
                unsafe_allow_html=True)

with visual, st.container(key="viz"):
    st.markdown(f'<p class="ml-instr"><i></i>{INSTR.get(key, "")}</p>', unsafe_allow_html=True)
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
            swipe.render(imgs[0], imgs[1], f"{ui.t('before')}: {ui.day(before)}",
                         f"{ui.t('after')}: {ui.day(after)}", height=500, start=35)
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
            for key, label, col in (("flood", "matched_floods", ui.COLORS["flood"]),
                                    ("slide", "matched_slides", ui.COLORS["slide_zones"])):
                s = summ.get(key, {})
                rows.append(ui.finding(col, ui.t("x_of_y", x=s.get("hits", 0), y=s.get("observable", 0)), "",
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

if i == n - 1:
    st.markdown(f"## {tr('Where next', 'पुढे कुठे')}")
    nxt = [(tr("District disaster teams", "जिल्हा आपत्ती पथके"),
            tr("A ranked check list of likely slide zones with radar images of each spot, a printable sheet and KML for phones.",
               "संभाव्य भूस्खलन क्षेत्रांची क्रमवार यादी, प्रत्येक जागेच्या रडार प्रतिमा, छापण्याजोगी यादी आणि फोनसाठी KML."),
            "views/5_Field.py", tr("Field check list", "क्षेत्रीय तपासणी यादी"), ":material/checklist:"),
           (tr("Everything on one map", "सर्व काही एकाच नकाशावर"),
            tr("Every layer, the season slider and the radar evidence for each zone and flood patch.",
               "प्रत्येक स्तर, हंगाम स्लायडर आणि प्रत्येक क्षेत्र व पुराच्या जागेचा रडार पुरावा."),
            "views/2_Explore.py", ui.t("explore"), ":material/map:"),
           (tr("Researchers and journalists", "संशोधक आणि पत्रकार"),
            tr("Every number traced to its NISAR file, the checks behind it, and the maps as GeoTIFF and GeoJSON.",
               "प्रत्येक आकडा त्याच्या निसार फाइलपर्यंत, त्यामागच्या तपासण्या, आणि नकाशे GeoTIFF व GeoJSON मध्ये."),
            "views/3_Method.py", tr("Method and limits", "पद्धत आणि मर्यादा"), ":material/science:")]
    with st.container(key="paths"):
        cols = st.columns(3)
    for c, (title, desc, page, label, icon) in zip(cols, nxt):
        with c.container(border=True):
            st.markdown(f"### {title}")
            st.markdown(f'<p class="ml-pathd">{desc}</p>', unsafe_allow_html=True)
            st.page_link(page, label=label, icon=icon)

# ← and → move between chapters (ignored while typing or when a map or slider has the keyboard)
with st.container(key="storykeys"):
    components.html("""<script>
const w = window.parent, d = w.document;
if (!w.__mlStoryKeys) {
  w.__mlStoryKeys = true;
  d.addEventListener('keydown', e => {
    const t = e.target, tag = t && t.tagName;
    if (e.altKey || e.ctrlKey || e.metaKey || tag === 'INPUT' || tag === 'TEXTAREA' || (t && t.isContentEditable)) return;
    const sel = e.key === 'ArrowRight' ? '.st-key-story_next button' : e.key === 'ArrowLeft' ? '.st-key-story_back button' : '';
    const b = sel && d.querySelector(sel);
    if (b && !b.disabled) { e.preventDefault(); b.click(); }
  });
}
</script>""", height=0)
ui.sources_line()
