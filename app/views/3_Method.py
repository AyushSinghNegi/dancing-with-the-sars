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
ui.english_only_note()
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
   water and land is set separately for each date with the minimum-error method of Kittler and Illingworth, trained
   on reservoir and river cores that the JRC Global Surface Water record says are water at least
   {th.get('water_train_occurrence', 90)}% of the time, plus an equal number of land pixels, and kept between
   {th.get('water_db_bounds', ['?', '?'])[0]} and {th.get('water_db_bounds', ['?', '?'])[1]} dB. In these NISAR
   products open water sits near -16 dB and dry land near -5 dB.
3. **Keep only new water.** A pixel is new water if it is water on {after} but not on {before}, at least
   {th.get('change_db')} dB darker, outside permanent water (JRC occurrence ≥ {th.get('permanent_water_occurrence')}%),
   on ground flatter than {th.get('flood_max_slope_deg')}°, and part of a patch of at least
   {th.get('min_patch_pixels')} pixels.
4. **Flag possible hidden water.** At L-band, water under trees or between buildings makes the radar bounce twice
   and come back brighter. Flat ground that got {th.get('change_db')} dB brighter is shown as *possible* water,
   never added to flood totals.
5. **Find likely slide zones.** On slopes of {th.get('slide_min_slope_deg')}° to {th.get('slide_max_slope_deg', 45)}°,
   outside the radar's layover and shadow, a zone needs all of: coherence (how well the ground matched itself
   between passes, from the NISAR GUNW product) below {th.get('coherence_low')}; coherence under 0.6 × its own 1 km
   neighbourhood (monsoon vegetation lowers coherence everywhere, so we look for local collapse); and HH rising by
   {th.get('slide_hh_rise_db', 3)} dB or more (rough debris) or HV dropping by {th.get('slide_hv_drop_db', 2)} dB or
   more (vegetation stripped), measured against the scene's own median change on dry land. Each zone gets a 0 to 1
   score from slope, radar change and coherence loss.
6. **Check against reports.** Reported floods and landslides (news and official sources, linked) are matched to
   detections within 500 m (floods) or 750 m (slides), or the report's own location precision if larger.
7. **Check with a second track.** When the files are processed, the same slide rule runs on an independent NISAR
   pair from another orbit (track 106, 3 to 15 July, which also spans the rain peak). A real slope failure
   changes the ground for good, so it should show in both; speckle or a geometry artefact of one orbit usually
   does not. Chance level comes from moving every zone to random steep, dry places and repeating the test.
8. **Check with a second elevation map.** Slope and slope direction come from the Copernicus GLO-30 elevation map.
   We run the same slide rule again with NASA's NASADEM elevation map and record which zones it keeps.
""")

st.markdown("## Data")
ROLE = {"before": "before, track 034", "after": "after, track 034", "pair": "coherence, track 034",
        "check_before": "second-track check, before, track 106", "check_after": "second-track check, after, track 106",
        "check_pair": "second-track check, coherence, track 106"}
rows = [{"Data": f"NISAR L2 {'GUNW' if s['role'].endswith('pair') else 'GCOV'} ({ROLE.get(s['role'], s['role'])})",
         "File": s["granule_id"], "Valid share of box": f"{s['valid_fraction']:.0%}", "Link": s["url"]}
        for s in m.get("sources", [])]
rows += [
    {"Data": "Permanent water", "File": "JRC Global Surface Water v1.4 occurrence (Pekel et al., 2016)",
     "Valid share of box": "", "Link": "https://global-surface-water.appspot.com/"},
    {"Data": "Elevation and slope", "File": "Copernicus GLO-30 DEM (ESA)", "Valid share of box": "",
     "Link": "https://registry.opendata.aws/copernicus-dem/"},
]
if m.get("dem_check"):
    rows.append({"Data": "Elevation, second-map check", "File": "NASADEM_HGT v001 (NASA / USGS)",
                 "Valid share of box": "", "Link": m["dem_check"]["check_dem_url"]})
rain = data.rainfall()
if rain is not None:
    src = str(rain["source"].iloc[0]) if "source" in rain else "daily rainfall"
    link = "https://power.larc.nasa.gov/" if "POWER" in src else "https://giovanni.gsfc.nasa.gov/"
    rows.append({"Data": "Daily rainfall", "File": src, "Valid share of box": "", "Link": link})
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
             column_config={"Link": st.column_config.LinkColumn("Link")})

st.markdown("## Results with their sources")
ws = data.table("water_stats.csv")
if ws is not None:
    st.dataframe(ws, hide_index=True, width="stretch")
st.markdown(
    f"Sanity check: on {before} the radar saw **{(m.get('water', {}).get('permanent_water_seen_dark') or 0):.0%}** "
    "of the JRC permanent-water pixels as water. A low value would mean the threshold or the data is off.")

st.markdown("## Validation")
val = data.table("validation.csv")
if val is not None and len(val):
    st.dataframe(val, hide_index=True, width="stretch",
                 column_config={"source_url": st.column_config.LinkColumn("source")})
else:
    st.info("Runs once `data/reference/events.geojson` exists.")

xt = data.crosstrack()
if xt:
    st.markdown("## Second-track check")
    c, ch = xt["status_counts"], xt.get("chance", {})
    pb, pa = (data.nice_date(xt["pair"][k], False) for k in ("before", "after"))
    st.markdown(
        f"Same slide rule, run on NISAR track {xt['pair']['track']} ({pb} to {pa}). A track-034 zone counts as "
        f"**found again** when a track-{xt['pair']['track']} zone lies within {xt['buffer_m']:.0f} m (allowing for "
        "small position differences between orbits). **Partial** means only one piece of the evidence is there "
        "(coherence loss or the backscatter jump): that alone is common in the monsoon, so we do not count it.")
    tbl = pd.DataFrame([
        {"": "Our zones", "Found again": str(c.get("confirmed", 0)), "Partial": str(c.get("partial", 0)),
         "Not seen": str(c.get("not seen", 0)), "Not covered by track 106": str(c.get("not covered", 0)),
         "Found-again rate": f"{xt['real']['confirmed']:.0%}"},
        {"": f"Same zones moved to random steep places ({ch.get('trials', 0)} trials)", "Found again": "",
         "Partial": "", "Not seen": "", "Not covered by track 106": "",
         "Found-again rate": f"{(ch.get('confirmed') or 0):.1%}"},
    ])
    st.dataframe(tbl, hide_index=True, width="stretch")
    if xt["lift"] is not None:
        pv = xt.get("p_value")
        ptxt = f" The chance of doing this well by luck alone is about {pv:.0%} (one-sided binomial test)." \
            if pv is not None and pv >= 0.01 else (" The chance of doing this well by luck alone is under 1%."
                                                    if pv is not None else "")
        st.markdown((f"Our zones were found again **{xt['lift']:.0f}× more often than chance**." + ptxt)
                    if xt["good"] else
                    f"Our zones were found again about as often as chance ({xt['lift']:.1f}×), so single-track "
                    "zones need ground checks before anyone relies on them.")
    if xt.get("small"):
        st.markdown(f"Track {xt['pair']['track']} sees only {xt['coverage']} of the study area, so only "
                    f"{xt['scored']} of our zones could be checked. That is a small sample: treat it as support, "
                    "not proof.")
    sh = (xt.get("scene_shift_db") or {}).get("track106")
    if sh:
        st.markdown(f"Between {pb} and {pa} the whole scene got about {abs(sh['hh_db']):.1f} dB darker in HH and "
                    f"{abs(sh['hv_db']):.1f} dB in HV, on flat and steep ground alike: ground and plants drying "
                    "after the storm, or calibration of these provisional products. A landslide is a local change, "
                    "so on both tracks we measure change against the scene's own median change on dry land.")
    if xt.get("water_reliable") is False:
        st.caption(f"Water areas from track {xt['pair']['track']} are not used: on {pb}, in heavy rain, the radar "
                   "saw less than half of the permanent reservoirs as dark water, because rain roughens the surface.")
    by = xt.get("status_by_confidence") or {}
    if by:
        st.caption("By confidence: " + "; ".join(
            f"{k}: {v.get('confirmed', 0)} of {v.get('confirmed', 0) + v.get('partial', 0) + v.get('not seen', 0)} "
            "found again" for k, v in sorted(by.items(), key=lambda kv: ["high", "medium", "low"].index(kv[0]))))

dc = m.get("dem_check")
if dc:
    st.markdown("## Elevation-map check")
    rs = dc["not_found_reasons"]
    hi = dc["by_confidence"].get("high", {})
    st.markdown(
        f"Slope and slope direction decide where the slide rule looks, so we ran it again on the same radar pair "
        f"with NASA's NASADEM elevation map instead of Copernicus. Overall the two slope maps agree closely "
        f"(median difference {dc['slope']['median_abs_diff_deg']:.0f}°). Near the "
        f"{th.get('slide_min_slope_deg', 15):.0f}° and {th.get('slide_max_slope_deg', 45):.0f}° limits they do not: "
        f"of the ground that either map puts inside that band, the other map puts "
        f"{1 - dc['slope']['band_agreement']:.0%} outside it.")
    st.markdown(
        f"**{dc['found']} of {dc['zones_main']}** zones are found again within {dc['buffer_m']:.0f} m, including "
        f"**{hi.get('found', 0)} of {hi.get('zones', 0)}** high-confidence zones. "
        f"NASADEM also finds {dc['new_in_nasadem']} zones of its own.")
    st.dataframe(pd.DataFrame(
        [{"Not found with NASADEM because": k[0].upper() + k[1:].replace(" in NASADEM", ""), "Zones": v}
         for k, v in rs.items()]), hide_index=True, width="content")
    rh = dc["reported_slide_hits"]
    hits = [s for s in dc["reported_slides"] if s["main"] == "hit"]
    if hits and rh["nasadem"] < rh["main"]:
        dist = " and ".join(f"{s['main_distance_m'] / 1000:.1f} km" for s in hits)
        same = len(rh["main_hit_zones"]) == 1
        st.markdown(
            (f"The {len(hits)} reported landslides we matched ({', '.join(s['id'] for s in hits)}) are "
             f"{'both' if len(hits) == 2 else 'all'} matched to the same zone, {rh['main_hit_zones'][0]}, {dist} away. "
             if same else
             f"The {len(hits)} reported landslides we matched are {dist} from their nearest zone. ")
            + f"With NASADEM, {rh['nasadem']} of {rh['scored']} reports have a zone within range. "
              "So treat the landslide matches as weak support.")
    both = [f["properties"]["id"] for f in (data.geojson("slide_zones.geojson") or {}).get("features", [])
            if f["properties"].get("nasadem") == "found" and f["properties"].get("track106") == "confirmed"]
    if both:
        st.markdown(f"Passing both extra checks (found again by the second NISAR track and with NASADEM): "
                    f"**{', '.join(both)}**.")

st.markdown("## Limits")
st.markdown(f"""
- **Provisional data.** These are NISAR provisional products (released from June 2026); calibration may still change.
- **Two snapshots, twelve days apart.** Anything that flooded and drained between {data.nice_date(before, False)} and {data.nice_date(after)} is invisible.
- **Cities.** Buildings make flooded streets bright, not dark. Our new-water map under-counts urban flooding.
- **Pixel size.** {m['grid']['res_m']:.0f} m pixels. Slides narrower than about two pixels are easily missed.
- **Same-mode rule.** From 27 August to 2 October NISAR imaged this track in a different mode (2005, quad-pol);
  14 October is back in the July mode. Brightness is only compared between passes with the same track, mode and
  polarisation.
- **Water areas may be underestimates.** On {data.nice_date(before)} only {(m.get('water', {}).get('permanent_water_seen_dark') or 0):.0%} of
  the area the JRC record marks as permanent water looked dark enough to pass our water test. Part of that is
  reservoirs drawn down before the monsoon; part is water roughened by wind or rain, which our test misses. So some
  real water may be missed on every date, new water included.
- **Small samples.** Every check is counted, not turned into an "accuracy": floods
  {m.get('validation', {}).get('flood', {}).get('hits', 0)} of {m.get('validation', {}).get('flood', {}).get('observable', 0)},
  landslides {m.get('validation', {}).get('slide', {}).get('hits', 0)} of {m.get('validation', {}).get('slide', {}).get('observable', 0)},
  and the second-track check covers only part of the area.
- **Slope near the limits.** Many zones sit close to the {th.get('slide_min_slope_deg', 15):.0f}° or {th.get('slide_max_slope_deg', 45):.0f}° limits, so a
  different elevation map moves some of them in or out (see the elevation-map check above).
- **Leads, not verdicts.** Slide zones are places to check, not confirmed landslides:
  {m.get('validation', {}).get('unreported_slide_zones', 0)} of {m.get('slides', {}).get('zones', 0)} have no reported event within 2 km.
- **Rainfall.** GPM IMERG Late Run, averaged over the whole study area per UTC day. It is lower than the single-station
  totals quoted in the news, and may shift slightly when the Final Run is released.
""")
st.markdown("## Team")
st.markdown("Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen: Ayush Singh Negi (app and integration), "
            "Rajendra Singh Negi (data and science), Urvashi (validation, story and pitch).")
ui.sources_line()
