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

pages = [
    st.Page("home.py", title="Overview", icon=":material/satellite_alt:", default=True),
    st.Page("views/1_Story.py", title="Story", url_path="story", icon=":material/auto_stories:"),
    st.Page("views/2_Explore.py", title="Explore the map", url_path="explore", icon=":material/map:"),
    st.Page("views/3_Method.py", title="Method and limits", url_path="method", icon=":material/science:"),
]
st.navigation(pages).run()
