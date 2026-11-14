"""MonsoonLens: entry point. Run with:  streamlit run app/streamlit_app.py"""
import streamlit as st

pages = [
    st.Page("home.py", title="Overview", icon=":material/satellite_alt:", default=True),
    st.Page("views/1_Story.py", title="Story", url_path="story", icon=":material/auto_stories:"),
    st.Page("views/2_Explore.py", title="Explore the map", url_path="explore", icon=":material/map:"),
    st.Page("views/3_Method.py", title="Method and limits", url_path="method", icon=":material/science:"),
]
st.navigation(pages).run()
