import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from lib import charts, data, maps, ui

ui.setup("Explore the map")
ui.demo_banner()
if not ui.require_results():
    st.stop()

before, after = data.dates()
st.markdown(f"# {ui.t('explore')}")
st.markdown(f'<div class="ml-dates">NISAR passes on {data.nice_date(before, False)} and {data.nice_date(after)}. '
            'Switch radar layers with the layer button at the top right of the map; click a slide zone or a marker for details.</div>',
            unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.2, 1])
basemap = c1.selectbox("Base map", list(maps.BASEMAPS), index=0)
opacity = c2.slider("Layer opacity", 0.2, 1.0, 0.85, 0.05)
conf = c3.selectbox("Slide zones shown", ["high", "medium", "low"], index=1,
                    format_func=lambda x: {"high": "High confidence only", "medium": "Medium and high",
                                           "low": "All, including low"}[x])
ui.legend([(ui.COLORS["new_water"], ui.t("legend_new_water"), "fill"),
           (ui.COLORS["slide_zones"], ui.t("legend_slides"), "outline"),
           (ui.COLORS["brighter"], ui.t("legend_brighter"), "hatch"),
           (ui.COLORS["permanent"], ui.t("legend_permanent"), "fill"),
           (ui.INK, ui.t("legend_events"), "dot")])
m = maps.build(basemap=basemap, opacity=opacity, min_conf=conf, zoom=10, collapsed=True)
st_folium(m, height=640, use_container_width=True, returned_objects=[], key=f"explore_{basemap}_{opacity}_{conf}")

tab_z, tab_w, tab_t, tab_e, tab_d = st.tabs(["Slide zones", "Water", "Rain and timeline", "Reported events",
                                             "Downloads"])
with tab_z:
    gj = data.geojson("slide_zones.geojson")
    if gj and gj["features"]:
        df = pd.DataFrame([f["properties"] for f in gj["features"]])
        if "near" not in df:
            df["near"] = ""
        df["near"] = df["near"].fillna("")
        df["map"] = [f"https://www.google.com/maps/search/?api=1&query={a},{b}" for a, b in zip(df["lat"], df["lon"])]
        cols = ["id", "near", "confidence", "score", "area_ha", "slope_deg", "hv_change_db", "hh_change_db",
                "coherence", "coherence_vs_local", "lat", "lon", "map"]
        st.markdown(f"{len(df)} likely slide zones, sorted by score. Score adds three pieces of evidence: "
                    "steepness, radar change, and coherence lost compared with the surrounding kilometre.")
        cc = st.column_config
        st.dataframe(df[[c for c in cols if c in df]], hide_index=True, use_container_width=True,
                     column_config={"id": "Zone", "confidence": "Confidence",
                                    "score": cc.ProgressColumn("Score", min_value=0, max_value=1, format="%.2f"),
                                    "area_ha": cc.NumberColumn("Area (ha)", format="%.1f"),
                                    "slope_deg": cc.NumberColumn("Slope (°)", format="%.0f"),
                                    "hv_change_db": cc.NumberColumn("HV change (dB)", format="%.1f"),
                                    "hh_change_db": cc.NumberColumn("HH change (dB)", format="%.1f"),
                                    "coherence": cc.NumberColumn("Coherence", format="%.2f"),
                                    "coherence_vs_local": cc.NumberColumn("Coherence vs 1 km", format="%.2f"),
                                    "lat": cc.NumberColumn("Lat", format="%.4f"),
                                    "lon": cc.NumberColumn("Lon", format="%.4f"),
                                    "near": "Nearest place",
                                    "map": cc.LinkColumn("Map", display_text="Open")})
        field = df[["id", "near", "confidence", "score", "area_ha", "slope_deg", "lat", "lon", "map"]].rename(
            columns={"near": "nearest_place", "map": "map_link"})
        st.download_button("Download field check list (CSV)", field.to_csv(index=False).encode(),
                           file_name="monsoonlens_slide_zones_field_checklist.csv", mime="text/csv",
                           help="Every likely slide zone with its nearest named place and a map link, "
                                "for teams checking on the ground.")
        st.caption("Place names: © OpenStreetMap contributors (Nominatim). Zones are leads to check, "
                   "not confirmed landslides.")
    else:
        st.info("No slide zones in this run.")
with tab_w:
    ws = data.table("water_stats.csv")
    if ws is not None:
        st.dataframe(ws, hide_index=True, use_container_width=True)
with tab_t:
    rain = data.rainfall()
    if rain is not None:
        st.plotly_chart(charts.rainfall(rain, before, after), use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Daily rainfall (GPM IMERG) appears here once `data/reference/rainfall.csv` is added.")
    tl = data.table("timeline.csv")
    if tl is not None and len(tl) > 1:
        st.markdown("**Water outside rivers and reservoirs, every NISAR pass on this track**")
        st.plotly_chart(charts.timeline(tl), use_container_width=True, config={"displayModeBar": False})
        st.caption("Hollow markers: radar mode or polarisation differs from the June pass, so brightness is not "
                   "directly comparable.")
    else:
        st.info("The monsoon timeline appears once more NISAR dates are cropped (`python -m pipeline.crop --timeline`).")
with tab_e:
    val = data.table("validation.csv")
    if val is not None and len(val):
        st.dataframe(val[["id", "type", "date", "place", "observable", "result", "distance_m", "reason",
                          "source_name", "source_url"]], hide_index=True, use_container_width=True,
                     column_config={"source_url": st.column_config.LinkColumn("source")})
    else:
        st.info("Reported events appear here once `data/reference/events.geojson` is added.")
with tab_d:
    st.markdown("GeoTIFFs are on the analysis grid (UTM zone 43N, 40 m). GeoJSON is in WGS84.")
    files = [(k, data.download_path(k)) for k in data.metrics().get("downloads", {})]
    files += [("slide_zones", None)]
    for key, path in files:
        if path is not None and path.exists():
            st.download_button(f"{key.replace('_', ' ')} (GeoTIFF)", path.read_bytes(), file_name=f"monsoonlens_{key}.tif",
                               key=f"dl_{key}")
    for name in ("slide_zones.geojson", "new_water.geojson", "validation.csv", "water_stats.csv", "metrics.json"):
        p = data.source()["dir"] and (data.ROOT / data.source()["dir"] / name)
        if p and p.exists():
            st.download_button(name, p.read_bytes(), file_name=f"monsoonlens_{name}", key=f"dl_{name}")
ui.sources_line()
