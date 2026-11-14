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
   corrected for terrain) on a map grid. A primary GCOV file is about 5–6 GB, so we stream only the
   study box (lon {m['aoi']['west']} to {m['aoi']['east']}, lat {m['aoi']['south']} to {m['aoi']['north']})
   and average 2 × 2 or more native pixels into a {m['grid']['res_m']:.0f} m grid (UTM zone 43N). Averaging also
   reduces radar speckle; a Lee filter removes more. Invalid source samples are excluded.
   Coherence also excludes samples flagged with RSLC processing anomalies.
2. **Find a shared water threshold.** Scikit-image Otsu splits the filtered {after} HH image in
   linear power. That single threshold ({th.get('water_threshold_db', 0):.2f} dB) is used on both dates;
   it is not clipped or fitted to the reference events. Dark pixels are candidate water, not confirmed water.
3. **Keep newly dark pixels.** A pixel is candidate new water if it is dark on {after} but not on {before},
   outside permanent water (JRC occurrence ≥ {th.get('permanent_water_occurrence')}%), and part of a patch
   of at least {th.get('min_patch_pixels')} pixels. The shared threshold is varied by ±1 dB on both dates
   for the reported sensitivity range. This brief-defined layer has no additional slope or change gate.
4. **Flag possible hidden water.** At L-band, water under trees or between buildings makes the radar bounce twice
   and come back brighter. Flat ground that got {th.get('change_db')} dB brighter is shown as *possible* water,
   never added to flood totals.
5. **Find likely slide zones.** NASADEM slopes of {th.get('slide_min_slope_deg')}° or more must also have
   GUNW coherence below {th.get('coherence_low')} and HV dropping by at least {th.get('change_db')} dB.
   Patches need at least {th.get('slide_min_patch_pixels', 3)} pixels. HH change and local coherence contrast are diagnostics only.
   The 0–1 evidence score is a heuristic ranking, not a calibrated probability.
6. **Check against reports.** Primary hits require a detection within {th.get('validation_radius_m')} m.
   Reported location precision is retained, and a separate precision-aware result shows matches under
   an expanded radius. Counts use only the fixed distance; approximate locations are not field truth.
""")

st.markdown("## Data")
rows = [{"Data": f"NISAR L2 {('GCOV' if s['role'] != 'pair' else 'GUNW')} ({s['role']})",
         "File": s["granule_id"], "Valid share of box": f"{s['valid_fraction']:.0%}", "Link": s["url"]}
        for s in m.get("sources", [])]
rows += [
    {"Data": "Permanent water", "File": "JRC Global Surface Water v1.4 occurrence (Pekel et al., 2016)",
     "Valid share of box": "", "Link": "https://global-surface-water.appspot.com/"},
    {"Data": "Elevation and slope", "File": "NASADEM_HGT.001 (NASA/USGS)", "Valid share of box": "",
     "Link": "https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001"},
]
if data.rainfall() is not None:
    rows.append({"Data": "Daily rainfall", "File": "; ".join(data.rainfall()["source"].dropna().unique()),
                 "Valid share of box": "", "Link": "https://power.larc.nasa.gov/" if data.rainfall()["source"].str.contains("POWER").any()
                 else "https://giovanni.gsfc.nasa.gov/"})
st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True,
             column_config={"Link": st.column_config.LinkColumn("Link")})

st.markdown("## Results with their sources")
ws = data.table("water_stats.csv")
if ws is not None:
    st.dataframe(ws, hide_index=True, use_container_width=True)
    if ws["meaning"].str.contains("otsu-clipped", na=False).any():
        st.info("The calibrated water threshold reached a configured limit. Review the ±1 dB sensitivity "
                "range in Explore when interpreting the detected area.")

seen = m.get("water", {}).get("permanent_water_seen_dark")
if seen is None:
    st.info("Permanent-water sanity check: not available.")
else:
    st.markdown(f"Sanity check: on {before} the radar saw **{seen:.0%}** of the valid JRC "
                "permanent-water pixels as water.")

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
- **Same-mode rule.** NISAR changed radar mode on this track from 27 August. Brightness is only compared between
  passes with matching track, frame, direction, mode and polarisation; the selected 14 October file is mode 4005.
- **Leads, not verdicts.** Slide zones are places to check, not confirmed landslides.
""")
st.markdown("## Team")
st.markdown("Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen: Ayush Singh Negi (app and integration), "
            "Rajendra Singh Negi (data and science), Urvashi (validation, story and pitch).")
ui.sources_line()
