import pandas as pd
import streamlit as st

from lib import data, ui

ui.setup("Method and limits")
ui.demo_banner()
if not ui.require_results():
    st.stop()

m = data.metrics()
th = m.get("thresholds", {})
before, after = data.dates()

st.markdown("# Method and limits")
st.markdown('<p class="ml-lede">Every number in this app comes from the pipeline in our public repository, '
            'run on the NISAR files listed below. Nothing is estimated by hand.</p>', unsafe_allow_html=True)

st.markdown("## How it works")
st.markdown(f"""
1. **Cut the radar to Pune.** NISAR's level-2 GCOV files hold radar brightness (gamma-nought, already
   corrected for terrain) on a map grid. A full frame is about 5 GB per layer, so we stream only the
   study box (lon {m['aoi']['west']} to {m['aoi']['east']}, lat {m['aoi']['south']} to {m['aoi']['north']})
   and average 2 × 2 or more native pixels into a {m['grid']['res_m']:.0f} m grid (UTM zone 43N). Averaging also
   reduces radar speckle; a Lee filter removes more.
2. **Find water on each date.** Smooth water reflects the radar away and looks dark in HH. The cut-off between
   water and land is set separately for each date with Otsu's method, trained on pixels that the JRC Global
   Surface Water record says are permanent water plus an equal number of land pixels, and kept between
   {th.get('water_db_bounds', ['?', '?'])[0]} and {th.get('water_db_bounds', ['?', '?'])[1]} dB.
3. **Keep only new water.** A pixel is new water if it is water on {after} but not on {before}, at least
   {th.get('change_db')} dB darker, outside permanent water (JRC occurrence ≥ {th.get('permanent_water_occurrence')}%),
   on ground flatter than {th.get('flood_max_slope_deg')}°, and part of a patch of at least
   {th.get('min_patch_pixels')} pixels.
4. **Flag possible hidden water.** At L-band, water under trees or between buildings makes the radar bounce twice
   and come back brighter. Flat ground that got {th.get('change_db')} dB brighter is shown as *possible* water,
   never added to flood totals.
5. **Find likely slide zones.** On slopes of {th.get('slide_min_slope_deg')}° or more, a zone needs all of:
   coherence (how well the ground matched itself between passes, from the NISAR GUNW product) below
   {th.get('coherence_low')}; coherence under 0.6 × its own 1 km neighbourhood (monsoon vegetation lowers coherence
   everywhere, so we look for local collapse); and HV dropping or HH rising by {th.get('change_db')} dB or more
   (vegetation stripped, rough debris). Each zone gets a 0 to 1 score from slope, radar change and coherence loss.
6. **Check against reports.** Reported floods and landslides (news and official sources, linked) are matched to
   detections within 500 m (floods) or 750 m (slides), or the report's own location precision if larger.
""")

st.markdown("## Data")
rows = [{"Data": f"NISAR L2 {('GCOV' if s['role'] != 'pair' else 'GUNW')} ({s['role']})",
         "File": s["granule_id"], "Valid share of box": f"{s['valid_fraction']:.0%}", "Link": s["url"]}
        for s in m.get("sources", [])]
rows += [
    {"Data": "Permanent water", "File": "JRC Global Surface Water v1.4 occurrence (Pekel et al., 2016)",
     "Valid share of box": "", "Link": "https://global-surface-water.appspot.com/"},
    {"Data": "Elevation and slope", "File": "Copernicus GLO-30 DEM (ESA)", "Valid share of box": "",
     "Link": "https://registry.opendata.aws/copernicus-dem/"},
]
if data.rainfall() is not None:
    rows.append({"Data": "Daily rainfall", "File": "GPM IMERG daily (NASA GES DISC, via Giovanni)",
                 "Valid share of box": "", "Link": "https://giovanni.gsfc.nasa.gov/"})
st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True,
             column_config={"Link": st.column_config.LinkColumn("Link")})

st.markdown("## Results with their sources")
ws = data.table("water_stats.csv")
if ws is not None:
    st.dataframe(ws, hide_index=True, use_container_width=True)
st.markdown(
    f"Sanity check: on {before} the radar saw **{(m.get('water', {}).get('permanent_water_seen_dark') or 0):.0%}** "
    "of the JRC permanent-water pixels as water. A low value would mean the threshold or the data is off.")

st.markdown("## Validation")
val = data.table("validation.csv")
if val is not None and len(val):
    st.dataframe(val, hide_index=True, use_container_width=True,
                 column_config={"source_url": st.column_config.LinkColumn("source")})
else:
    st.info("Runs once `data/reference/events.geojson` exists.")

st.markdown("## Limits")
st.markdown(f"""
- **Provisional data.** These are NISAR provisional products (released from June 2026); calibration may still change.
- **Two snapshots, twelve days apart.** Anything that flooded and drained between {before} and {after} is invisible.
- **Cities.** Buildings make flooded streets bright, not dark. Our new-water map under-counts urban flooding.
- **Pixel size.** {m['grid']['res_m']:.0f} m pixels. Slides narrower than about two pixels are easily missed.
- **Same-mode rule.** From 27 August to 2 October NISAR imaged this track in a different mode (2005, quad-pol);
  14 October is back in the July mode. Brightness is only compared between passes with the same track, mode and
  polarisation.
- **Leads, not verdicts.** Slide zones are places to check, not confirmed landslides.
""")
st.markdown("## Team")
st.markdown("Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen: Ayush Singh Negi (app and integration), "
            "Rajendra Singh Negi (data and science), Urvashi (validation, story and pitch).")
ui.sources_line()
