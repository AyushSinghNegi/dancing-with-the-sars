"""Look, language and shared pieces of the MonsoonLens app."""
from __future__ import annotations

import html

import streamlit as st

from . import data

INK = "#1d3346"       # monsoon slate: text and buttons (blue is reserved for water)
MUTED = "#5d6b75"
RADAR = "#7d878f"
PAPER = "#f4f6f5"
LINE = "#d9dedd"
COLORS = {"new_water": "#2a78d6", "flood": "#1c5cab", "rise": "#6da7ec", "slide_zones": "#eb6834", "brighter": "#1baf7a", "permanent": "#b7d3f6"}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@600;700&family=IBM+Plex+Sans+Devanagari:wght@400;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');
html, body, .stApp, .stMarkdown, button, input, textarea, select, label, p, li, td, th {{
  font-family: 'IBM Plex Sans', 'IBM Plex Sans Devanagari', system-ui, sans-serif;
}}
[data-testid="stIconMaterial"], .material-symbols-rounded {{
  font-family: 'Material Symbols Rounded' !important;
}}
.stApp {{ background: {PAPER}; color: {INK}; }}
.block-container {{ padding-top: 2.2rem; max-width: 1180px; }}
h1, h2, h3, .ml-display {{
  font-family: 'IBM Plex Sans Condensed', 'IBM Plex Sans Devanagari', sans-serif;
  color: {INK}; letter-spacing: -0.01em;
}}
h1 {{ font-size: 2.6rem; line-height: 1.05; font-weight: 700; }}
h2 {{ font-size: 1.7rem; line-height: 1.15; font-weight: 700; margin-top: 1.6rem; }}
h3 {{ font-size: 1.2rem; font-weight: 600; }}
p, li {{ font-size: 1.02rem; line-height: 1.6; max-width: 72ch; }}
.ml-lede {{ font-size: 1.18rem; line-height: 1.55; color: {INK}; max-width: 60ch; }}
.ml-muted {{ color: {MUTED}; font-size: 0.93rem; }}
.ml-hero {{ font-size: clamp(2rem, 3.1vw, 3.3rem); line-height: 1.03; font-weight: 700; margin: 0 0 0.6rem 0; text-wrap: balance; }}
.ml-dates {{ font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; color: {RADAR};
  font-size: 1.05rem; margin-bottom: 1.2rem; }}
.ml-finding {{ display: grid; grid-template-columns: 18px 7.5rem 1fr; gap: 0.2rem 0.9rem;
  align-items: baseline; padding: 0.7rem 0; border-top: 1px solid {LINE}; }}
.ml-finding:last-child {{ border-bottom: 1px solid {LINE}; }}
.ml-swatch {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; transform: translateY(2px); }}
.ml-swatch.hatch {{ background-image: repeating-linear-gradient(45deg, currentColor 0 3px, transparent 3px 6px); }}
.ml-num {{ font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 1.6rem; color: {INK};
  white-space: nowrap; }}
.ml-num small {{ font-size: 0.95rem; font-weight: 600; color: {MUTED}; margin-left: 0.15rem; }}
.ml-text {{ font-size: 1rem; line-height: 1.45; }}
.ml-banner {{ background: #fff4d6; border: 1px solid #e9c46a; color: #5a4300; padding: 0.7rem 1rem;
  border-radius: 6px; font-size: 0.95rem; margin-bottom: 1rem; }}
.ml-banner b {{ color: #3d2e00; }}
.ml-note {{ border-left: 3px solid {INK}; padding: 0.2rem 0 0.2rem 0.9rem; color: {INK}; margin: 0.8rem 0; }}
.ml-legend {{ display: flex; flex-wrap: wrap; gap: 0.4rem 1.1rem; font-size: 0.9rem; color: {INK}; margin: 0.4rem 0 0.6rem; }}
.ml-legend span {{ display: inline-flex; align-items: center; gap: 0.4rem; }}
.ml-step {{ font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; color: {RADAR}; font-size: 1rem; }}
.ml-source {{ font-size: 0.82rem; color: {MUTED}; }}
.ml-source a {{ color: {MUTED}; }}
.stButton > button, .stLinkButton > a, .stPageLink a {{ border-radius: 6px; }}
.stButton > button[kind="primary"] {{ background: {INK}; border-color: {INK}; }}
[data-testid="stSidebar"] {{ background: #eaeeed; }}
:focus-visible {{ outline: 3px solid #2a78d6 !important; outline-offset: 2px; }}
@media (max-width: 640px) {{
  .ml-finding {{ grid-template-columns: 16px 6rem 1fr; }}
  .ml-num {{ font-size: 1.3rem; }}
  h1 {{ font-size: 2rem; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; transition: none !important; }} }}
</style>
"""

# Marathi strings: drafted by the team's assistant, to be checked by a native speaker before submission.
T = {
    "title": {"en": "What NISAR radar saw in the 2026 Pune monsoon",
              "mr": "२०२६ च्या पुणे पावसाळ्यात निसार रडारने काय पाहिले"},
    "lede": {"en": "Monsoon cloud hides the ground exactly when people most need to see it. NASA and ISRO's NISAR "
                   "satellite sends radar through cloud and rain. We compared its passes over Pune before and after "
                   "the floods and landslides of 3 to 8 July 2026.",
             "mr": "पावसाळ्यातील ढग नेमके तेव्हाच जमीन झाकतात जेव्हा ती पाहण्याची सर्वात जास्त गरज असते. नासा आणि इस्रोचा "
                   "निसार उपग्रह ढग आणि पावसातून रडार पाठवतो. ३ ते ८ जुलै २०२६ च्या पूर आणि भूस्खलनांच्या आधी आणि "
                   "नंतरच्या पुण्यावरील निरीक्षणांची आम्ही तुलना केली."},
    "found": {"en": "What the radar found", "mr": "रडारला काय सापडले"},
    "new_water": {"en": "of new open water on flat ground, outside rivers and reservoirs",
                  "mr": "नद्या आणि धरणांबाहेर, सपाट जमिनीवर नवीन साचलेले पाणी"},
    "rise": {"en": "of new water as Pune's reservoirs and rivers rose and filled",
             "mr": "पुण्याची धरणे आणि नद्या भरल्यामुळे वाढलेले नवीन पाणी"},
    "flood": {"en": "of flood water still standing on 10 July where no water had been recorded since 1984",
              "mr": "१९८४ पासून कधीही पाणी न नोंदवलेल्या ठिकाणी १० जुलैला अजूनही साचलेले पुराचे पाणी"},
    "legend_flood": {"en": "Flooding (never water before)", "mr": "पूर (आधी कधीही पाणी नव्हते)"},
    "legend_rise": {"en": "Reservoirs and rivers rising", "mr": "धरणे आणि नद्या वाढल्या"},
    "slides": {"en": "likely slide zones on slopes steeper than 15°, {high} of them high confidence",
               "mr": "१५° पेक्षा जास्त उताराच्या भागात संभाव्य भूस्खलन क्षेत्रे, त्यापैकी {high} उच्च खात्रीची"},
    "xt_good": {"en": "of the slide zones that a second NISAR track could see were found by it too, "
                      "{lift}× more often than chance",
                "mr": "दुसऱ्या निसार मार्गाला दिसू शकलेल्या भूस्खलन क्षेत्रांपैकी तिथेही सापडलेली क्षेत्रे, योगायोगापेक्षा "
                      "{lift}× जास्त वेळा"},
    "xt_good_small": {"en": "of the slide zones a second NISAR track could see were found by it too: {lift}× more often "
                            "than chance, from a small sample, as that track covers {cov} of the area",
                      "mr": "दुसऱ्या निसार मार्गाला दिसू शकलेल्या भूस्खलन क्षेत्रांपैकी तिथेही सापडलेली क्षेत्रे: योगायोगापेक्षा "
                            "{lift}× जास्त वेळा; पण नमुना लहान आहे, कारण तो मार्ग क्षेत्राचा फक्त {cov} भाग पाहतो"},
    "xt_story_good_small": {"en": "A second NISAR track, passing on {b} and {a} from a different orbit, sees {cov} of the "
                                  "area. Of the {n} zones inside its view, it found {c} again on its own: {lift}× more "
                                  "often than chance, though {n} is a small sample.",
                            "mr": "{b} आणि {a} रोजी वेगळ्या कक्षेतून गेलेला दुसरा निसार मार्ग क्षेत्राचा {cov} भाग पाहतो. "
                                  "त्याच्या दृष्टीतील {n} क्षेत्रांपैकी {c} त्याने स्वतंत्रपणे पुन्हा शोधली: योगायोगापेक्षा "
                                  "{lift}× जास्त वेळा, पण {n} हा लहान नमुना आहे."},
    "xt_weak": {"en": "of the slide zones that a second NISAR track could see were found by it too, about what "
                      "chance would give: treat single-track zones with extra care",
                "mr": "दुसऱ्या निसार मार्गाला दिसू शकलेल्या भूस्खलन क्षेत्रांपैकी तिथेही सापडलेली क्षेत्रे, साधारण "
                      "योगायोगाइतकी: एकाच मार्गावरील क्षेत्रे काळजीपूर्वक तपासा"},
    "xt_story_good": {"en": "A second NISAR track, passing on {b} and {a} from a different orbit, found {c} of the {n} "
                            "zones it could see on its own: {lift}× more often than chance.",
                      "mr": "{b} आणि {a} रोजी वेगळ्या कक्षेतून गेलेल्या दुसऱ्या निसार मार्गाने, त्याला दिसू शकलेल्या "
                            "{n} पैकी {c} क्षेत्रे स्वतंत्रपणे शोधली: योगायोगापेक्षा {lift}× जास्त वेळा."},
    "xt_story_weak": {"en": "A second NISAR track, passing on {b} and {a}, found only {c} of the {n} zones it could see, "
                            "about what chance would give, so treat each zone as a lead to check.",
                      "mr": "{b} आणि {a} रोजी गेलेल्या दुसऱ्या निसार मार्गाने त्याला दिसू शकलेल्या {n} पैकी फक्त {c} "
                            "क्षेत्रे शोधली, साधारण योगायोगाइतकी; म्हणून प्रत्येक क्षेत्र तपासण्याजोगे समजा."},
    "xt_col": {"en": "Second track", "mr": "दुसरा मार्ग"},
    "brighter": {"en": "where water may be hiding under trees or between buildings (not counted as flood)",
                 "mr": "जिथे झाडांखाली किंवा इमारतींमध्ये पाणी असू शकते (पुरात मोजलेले नाही)"},
    "matched": {"en": "of reported events that radar could observe were matched by a detection",
                "mr": "रडारला दिसू शकणाऱ्या नोंदवलेल्या घटनांपैकी शोधलेल्या घटना"},
    "start_story": {"en": "Start the story", "mr": "कथा सुरू करा"},
    "explore": {"en": "Explore the map", "mr": "नकाशा पाहा"},
    "method": {"en": "How we did it", "mr": "आम्ही हे कसे केले"},
    "before": {"en": "Before", "mr": "आधी"},
    "after": {"en": "After", "mr": "नंतर"},
    "couldnt": {"en": "What radar could not see", "mr": "रडारला काय दिसले नाही"},
    "demo": {"en": "<b>Demo data.</b> The radar values on this page are synthetic, made in NISAR's file format so the "
                   "app could be built before the real Pune files were processed. Terrain, rivers and reservoirs are "
                   "real; floods and slide zones are not.",
             "mr": "<b>प्रात्यक्षिक डेटा.</b> या पानावरील रडार मूल्ये कृत्रिम आहेत. भूभाग, नद्या आणि धरणे खरी आहेत; पूर "
                   "आणि भूस्खलन क्षेत्रे खरी नाहीत."},
    "no_data": {"en": "Results are not built yet. Run `python -m pipeline.run_all`.",
                "mr": "निकाल अजून तयार नाहीत."},
    "layers": {"en": "Layers", "mr": "स्तर"},
    "legend_new_water": {"en": "New open water", "mr": "नवीन साचलेले पाणी"},
    "legend_slides": {"en": "Likely slide zone", "mr": "संभाव्य भूस्खलन क्षेत्र"},
    "legend_brighter": {"en": "Possible water under cover", "mr": "झाकलेले संभाव्य पाणी"},
    "legend_permanent": {"en": "Rivers and reservoirs", "mr": "नद्या आणि धरणे"},
    "legend_events": {"en": "Reported event", "mr": "नोंदवलेली घटना"},
    "lang": {"en": "Language", "mr": "भाषा"},
    "step": {"en": "Step {i} of {n}", "mr": "{n} पैकी टप्पा {i}"},
    "back": {"en": "Back", "mr": "मागे"},
    "next": {"en": "Next", "mr": "पुढे"},
    "story_title": {"en": "Story", "mr": "कथा"},
    "matched_floods": {"en": "reported floods that radar could observe had a detection nearby",
                       "mr": "रडारला दिसू शकणाऱ्या नोंदवलेल्या पुरांजवळ शोध लागला"},
    "matched_slides": {"en": "reported landslides that radar could observe had a detection nearby",
                       "mr": "रडारला दिसू शकणाऱ्या नोंदवलेल्या भूस्खलनांजवळ शोध लागला"},
    "x_of_y": {"en": "{x} of {y}", "mr": "{y} पैकी {x}"},
    "fell_short": {"en": "Where radar fell short, and why", "mr": "रडार कुठे कमी पडले आणि का"},
    "rain_caption": {"en": "Daily rainfall averaged over the study box. Source: {src}.",
                     "mr": "अभ्यास क्षेत्रातील सरासरी रोजचा पाऊस. स्रोत: {src}."},
    "swipe_caption": {"en": "Drag to compare. Dark is smooth: water. Bright is rough: buildings, trees, rock. "
                            "Area shown: the part of the study box with the most change.",
                      "mr": "तुलना करण्यासाठी ओढा. गडद म्हणजे गुळगुळीत पृष्ठभाग: पाणी. उजळ म्हणजे खडबडीत: इमारती, "
                            "झाडे, खडक. दाखवलेला भाग: अभ्यास क्षेत्रातील सर्वात जास्त बदल झालेला भाग."},
}


def english_only_note():
    """Technical pages are in English only; say so in Marathi instead of switching silently."""
    if lang() == "mr":
        st.info("हे तांत्रिक पान सध्या बहुतांश इंग्रजीत आहे. आकडे आणि कथा मराठीत पाहण्यासाठी "
                "मुख्य पान आणि कथा पाहा.")


def lang() -> str:
    return st.session_state.get("lang", "en")


def t(key: str, **kw) -> str:
    s = T.get(key, {}).get(lang()) or T.get(key, {}).get("en", key)
    return s.format(**kw) if kw else s


def setup(page_title: str):
    st.set_page_config(page_title=f"MonsoonLens: {page_title}", page_icon="🛰️", layout="wide",
                       initial_sidebar_state="auto")
    st.markdown(CSS, unsafe_allow_html=True)
    data.publish_overlays()
    with st.sidebar:
        choice = st.radio(t("lang"), ["English", "मराठी"], horizontal=True,
                          index=0 if lang() == "en" else 1, key="lang_choice")
        st.session_state["lang"] = "en" if choice == "English" else "mr"
        st.caption("MonsoonLens, built by team iGenfinity for NASA Space Apps 2026")


def demo_banner():
    if data.source()["demo"]:
        st.markdown(f'<div class="ml-banner">{t("demo")}</div>', unsafe_allow_html=True)


def require_results() -> bool:
    if not data.source()["dir"]:
        st.warning(t("no_data"))
        return False
    return True


def fmt_num(v, digits=1):
    if v is None:
        return "not available"
    if isinstance(v, (int,)) or float(v).is_integer() and abs(v) >= 10:
        return f"{int(round(v)):,}"
    return f"{v:,.{digits}f}"


def finding(color: str, number: str, unit: str, text: str, hatch=False):
    sw = f'<span class="ml-swatch{" hatch" if hatch else ""}" style="background-color:{color};color:{color}"></span>' \
        if not hatch else f'<span class="ml-swatch hatch" style="color:{color};border:1px solid {color}"></span>'
    return (f'<div class="ml-finding">{sw}<div class="ml-num">{html.escape(number)}<small>{html.escape(unit)}</small></div>'
            f'<div class="ml-text">{html.escape(text)}</div></div>')


def legend(items):
    parts = []
    for color, label, kind in items:
        if kind == "hatch":
            sw = f'<span class="ml-swatch hatch" style="color:{color};border:1px solid {color}"></span>'
        elif kind == "dot":
            sw = f'<span class="ml-swatch" style="background:#fff;border:2px solid {INK};border-radius:50%"></span>'
        elif kind == "outline":
            sw = f'<span class="ml-swatch" style="background:{color}55;border:2px solid {color}"></span>'
        else:
            sw = f'<span class="ml-swatch" style="background:{color}"></span>'
        parts.append(f"<span>{sw}{html.escape(label)}</span>")
    st.markdown(f'<div class="ml-legend">{"".join(parts)}</div>', unsafe_allow_html=True)


def sources_line():
    srcs = data.metrics().get("sources", [])
    if not srcs:
        return
    names = ", ".join(f'<a href="{s["url"]}">{s["granule_id"][:31]}…{s["granule_id"][-31:-24]}</a>' for s in srcs)
    st.markdown(f'<p class="ml-source">Radar: NISAR L2 provisional products {names} (NASA/JPL-Caltech, ISRO, via ASF DAAC). '
                f'Built {data.metrics().get("generated", "")[:16].replace("T", " ")} UTC, pipeline '
                f'v{data.metrics().get("pipeline_version", "")}.</p>', unsafe_allow_html=True)
