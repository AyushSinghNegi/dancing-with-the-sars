"""MonsoonLens: entry point. Run with:  streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path

import streamlit as st

# Streamlit Community Cloud pulls new code into the running server but keeps helper modules that were
# already imported (lib.*) in memory, so a merge could keep serving old code. Whenever any lib file
# changes, drop those modules so the pages below import the new ones.
_LIB = Path(__file__).resolve().parent / "lib"
_stamp = tuple(sorted((p.name, p.stat().st_mtime_ns, p.stat().st_size) for p in _LIB.glob("*.py")))
if getattr(sys, "_monsoonlens_lib_stamp", None) != _stamp:
    for _name in [m for m in list(sys.modules) if m == "lib" or m.startswith("lib.")]:
        del sys.modules[_name]
    sys._monsoonlens_lib_stamp = _stamp

# Page names in the visitor's language. The sidebar language switch has already updated its state when this runs.
_ss, _q = st.session_state, st.query_params.get("lang")
_lang = {"English": "en", "मराठी": "mr", "Deutsch": "de"}.get(_ss.get("lang_choice")) or _ss.get("lang") or \
    (_q if _q in ("en", "mr", "de") else "en")
_T = {"en": ("Overview", "Story", "Explore the map", "Check a place", "Field check list", "Method and limits"),
      "mr": ("आढावा", "कथा", "नकाशा पाहा", "एखादे ठिकाण तपासा", "क्षेत्रीय तपासणी यादी", "पद्धत आणि मर्यादा"),
      "de": ("Überblick", "Geschichte", "Karte erkunden", "Ort prüfen", "Feld-Checkliste", "Methode und Grenzen")}[_lang]
pages = [
    st.Page("home.py", title=_T[0], icon=":material/satellite_alt:", default=True),
    st.Page("views/1_Story.py", title=_T[1], url_path="story", icon=":material/auto_stories:"),
    st.Page("views/2_Explore.py", title=_T[2], url_path="explore", icon=":material/map:"),
    st.Page("views/4_Place.py", title=_T[3], url_path="place", icon=":material/location_on:"),
    st.Page("views/5_Field.py", title=_T[4], url_path="field", icon=":material/checklist:"),
    st.Page("views/3_Method.py", title=_T[5], url_path="method", icon=":material/science:"),
]
st.navigation(pages).run()
