import html

import pandas as pd
import streamlit as st

from lib import checks, data, explain, ui

ui.setup("Method and limits")
ui.demo_banner()
if not ui.require_results():
    st.stop()

m = data.metrics()
th = m.get("thresholds", {})
before, after = data.dates()
val_s = m.get("validation", {})
srcs = m.get("sources", [])

ui.page_header("Method and limits",
               "Every number in this app comes from the pipeline in our public repository, run on the NISAR files "
               "listed below. Nothing is estimated by hand, and every check is reported, including the ones that "
               "came out weak.", "Researchers and journalists")
ui.english_only_note()
st.markdown('<nav class="ml-toc" aria-label="On this page">' + "".join(
    f'<a href="#{a}">{t}</a>' for a, t in [
        ("nisar-in-brief", "NISAR in brief"), ("how-radar-sees-through-cloud", "How radar sees"),
        ("how-it-works", "How it works"), ("how-we-checked-it", "How we checked it"), ("data", "Data"),
        ("limits", "Limits"), ("reproduce-it", "Reproduce it"), ("team", "Team")]) + "</nav>",
    unsafe_allow_html=True)

# ---------------------------------------------------------------- the satellite
st.markdown("## NISAR in brief")
tracks = sorted({s["granule_id"].split("_")[5] for s in srcs if s["granule_id"].count("_") > 5})
utc = sorted({s["granule_id"].split("_A_")[-1][9:13] for s in srcs if "_A_" in s["granule_id"]})
utc_txt = " and ".join(f"{u[:2]}:{u[2:]}" for u in utc)
facts = [
    ("Launched", "30 July 2025 on ISRO's GSLV-F16, from Sriharikota, India"),
    ("Orbit", "Sun-synchronous, about 747 km up, inclined 98.4°"),
    ("Repeat", "The same ground track every 12 days"),
    ("Radars", "L-band (NASA/JPL, 24 cm wavelength) and S-band (ISRO), sharing one 12 m mesh reflector"),
    ("Swath", "242 km wide on the ground"),
    ("What this app uses", f"L-band, tracks {' and '.join(t.lstrip('0') for t in tracks)}, southbound evening passes "
                           f"({utc_txt} UTC), level-2 GCOV and GUNW products"),
]
st.markdown('<dl class="ml-facts-card">' + "".join(
    f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in facts) + "</dl>",
    unsafe_allow_html=True)
st.caption("Mission facts: [ISRO, NISAR launch page](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) and "
           "[eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar). Tracks and times: the NISAR file "
           "names in the Data table.")

st.markdown("## How radar sees through cloud")
st.markdown(f'<div style="width:100%;max-width:1000px">{explain.svg()}</div>', unsafe_allow_html=True)
st.caption("NISAR's L-band radar has a wavelength of about 24 cm: it passes through cloud and rain, and partly through "
           "forest canopy. It sends two polarisations: HH (horizontal out, horizontal back) responds to surfaces and "
           "structures, HV (horizontal out, vertical back) mostly to vegetation.")

# ---------------------------------------------------------------- the pipeline
st.markdown("## How it works")
wb = th.get("water_db_bounds", ["?", "?"])
STEPS = [
    ("Read the radar", [
        ("Cut the radar to Pune",
         f"NISAR's level-2 GCOV files hold radar brightness (gamma-nought, already corrected for terrain) on a map grid. "
         f"A full frame is about 5 GB per layer, so we stream only the study box (lon {m['aoi']['west']} to "
         f"{m['aoi']['east']}, lat {m['aoi']['south']} to {m['aoi']['north']}) and average 2 × 2 or more native pixels "
         f"into a {m['grid']['res_m']:.0f} m grid. Averaging reduces radar speckle; a Lee filter removes more.",
         [f"{m['grid']['res_m']:.0f} m grid", "UTM zone 43N", "Lee filter"]),
        ("Find water on each date",
         "Smooth water reflects the radar away and looks dark in HH. The cut-off between water and land is set "
         "separately for each date with the minimum-error method of Kittler and Illingworth, trained on reservoir and "
         f"river cores that the JRC Global Surface Water record says are water at least "
         f"{th.get('water_train_occurrence', 90)}% of the time, plus an equal number of land pixels. In these NISAR "
         "products open water sits near −16 dB and dry land near −5 dB.",
         [f"threshold kept within {wb[0]} to {wb[1]} dB", "one threshold per date"]),
    ]),
    ("Find the change", [
        ("Keep only new water",
         f"A pixel is new water if it is water on {after} but not on {before}, clearly darker, outside permanent "
         "water, on flat ground, and part of a patch big enough not to be speckle.",
         [f"≥ {th.get('change_db')} dB darker", f"JRC occurrence < {th.get('permanent_water_occurrence')}%",
          f"slope < {th.get('flood_max_slope_deg')}°", f"≥ {th.get('min_patch_pixels')} pixels"]),
        ("Flag possible hidden water",
         "At L-band, water under trees or between buildings makes the radar bounce twice and come back brighter. Flat "
         "ground that got brighter is shown as possible water, and never added to flood totals.",
         [f"≥ {th.get('change_db')} dB brighter", "shown hatched, never counted"]),
        ("Find likely slide zones",
         "Outside the radar's layover and shadow, a zone needs all three: the ground stopped matching itself between "
         "passes (coherence, from the NISAR GUNW product); it lost much more coherence than its own 1 km "
         "neighbourhood, because monsoon vegetation lowers coherence everywhere; and the radar brightness jumped, "
         "from rough debris (HH up) or stripped vegetation (HV down), measured against the scene's own median change "
         "on dry land. Each zone gets a 0 to 1 score from slope, radar change and coherence loss.",
         [f"slope {th.get('slide_min_slope_deg')}° to {th.get('slide_max_slope_deg', 45)}°",
          f"coherence < {th.get('coherence_low')}", "< 0.6 × its 1 km surroundings",
          f"HH +{th.get('slide_hh_rise_db', 3)} dB or HV −{th.get('slide_hv_drop_db', 2)} dB"]),
    ]),
    ("Check it", [
        ("Check against reports",
         "Reported floods and landslides, from the news and official sources, each linked, are matched to detections "
         "nearby, or within the report's own location precision if that is larger.",
         ["floods: 500 m", "slides: 750 m", f"{len(data.events().get('features', [])) if data.events() else 0} reports"]),
        ("Check with a second track",
         "The same slide rule runs on an independent NISAR pair from another orbit, which also spans the rain peak. "
         "A real slope failure changes the ground for good, so it should show in both; speckle or a geometry artefact "
         "of one orbit usually does not. Chance level comes from moving every zone to random steep, dry places and "
         "repeating the test.",
         ["track 106", "3 to 15 July", "random-placement baseline"]),
        ("Check with a second elevation map",
         "Slope and slope direction come from the Copernicus GLO-30 elevation map. We run the same slide rule again "
         "with NASA's NASADEM elevation map and record which zones it keeps.",
         ["Copernicus GLO-30", "NASA NASADEM"]),
        ("Test the water threshold",
         "Both dates' water thresholds are moved 1 dB down and up and the water numbers are recomputed, to show how "
         "much they depend on that one choice.", ["−1, 0, +1 dB"]),
    ]),
    ("Hand it over", [
        ("Package the evidence",
         "For every slide zone and flood patch the pipeline cuts small image chips of that spot from the NISAR data "
         "(radar colour before and after, and coherence), notes the nearest reported event, and writes the field "
         "check list as a printable page, KML, CSV and GeoJSON.",
         ["1.9 km image chips", "HTML", "KML", "CSV", "GeoJSON"]),
    ]),
]
st.markdown('<div class="ml-flow">' + "".join(
    f"<div><b>{html.escape(ph)}</b>{html.escape(', '.join(t.lower() if j else t for j, (t, _, _) in enumerate(st_)))}</div>"
    for ph, st_ in STEPS) + "</div>", unsafe_allow_html=True)
k = 0
for phase, steps in STEPS:
    st.markdown(f'<p class="ml-phase">{html.escape(phase)}</p>', unsafe_allow_html=True)
    items = []
    for title, desc, chips in steps:
        k += 1
        items.append(f'<li><span class="n">{k}</span><p class="t">{html.escape(title)}</p>'
                     f'<p class="d">{html.escape(desc)}</p><div class="ml-chips2">'
                     + "".join(f"<span>{html.escape(c)}</span>" for c in chips) + "</div></li>")
    st.markdown(f'<ol class="ml-steps" start="{k - len(steps) + 1}">{"".join(items)}</ol>', unsafe_allow_html=True)

# ---------------------------------------------------------------- the checks
st.markdown("## How we checked it")
checks.render()
xt, dc, sens = data.crosstrack(), m.get("dem_check"), m.get("sensitivity")
tabs = st.tabs(["Reported events", "Second NISAR orbit", "Second elevation map", "Water threshold", "Results table"])


def short(text):
    st.markdown(f'<p class="ml-short"><b>In short:</b> {text}</p>', unsafe_allow_html=True)


with tabs[0]:
    short(f"radar found something near {val_s.get('flood', {}).get('hits', 0)} of "
          f"{val_s.get('flood', {}).get('observable', 0)} reported floods and {val_s.get('slide', {}).get('hits', 0)} of "
          f"{val_s.get('slide', {}).get('observable', 0)} landslides that it could see.")
    val = data.table("validation.csv")
    if val is not None and len(val):
        st.markdown(
            f"Floods: **{val_s.get('flood', {}).get('hits', 0)} of {val_s.get('flood', {}).get('observable', 0)}** "
            f"reports that radar could observe had a detection nearby. Landslides: "
            f"**{val_s.get('slide', {}).get('hits', 0)} of {val_s.get('slide', {}).get('observable', 0)}**. "
            "Counts, not an accuracy: the samples are small.")
        st.dataframe(val, hide_index=True, width="stretch",
                     column_config={"source_url": st.column_config.LinkColumn("source")})
    else:
        st.info("Runs once `data/reference/events.geojson` exists.")
with tabs[1]:
    if xt:
        short(f"an independent NISAR orbit re-found {xt['confirmed']} of the {xt['scored']} zones it could see, "
              f"{ui.fmt_num(xt['lift'] or 0, 0)}× more often than chance. A small sample, so support, not proof.")
        c, ch = xt["status_counts"], xt.get("chance", {})
        pb, pa = (data.nice_date(xt["pair"][k_], False) for k_ in ("before", "after"))
        st.markdown(
            f"Same slide rule, run on NISAR track {xt['pair']['track']} ({pb} to {pa}). A track-034 zone counts as "
            f"**found again** when a track-{xt['pair']['track']} zone lies within {xt['buffer_m']:.0f} m (allowing for "
            "small position differences between orbits). **Partial** means only one piece of the evidence is there "
            "(coherence loss or the backscatter jump): that alone is common in the monsoon, so we do not count it.")
        st.dataframe(pd.DataFrame([
            {"": "Our zones", "Found again": str(c.get("confirmed", 0)), "Partial": str(c.get("partial", 0)),
             "Not seen": str(c.get("not seen", 0)), "Not covered by track 106": str(c.get("not covered", 0)),
             "Found-again rate": f"{xt['real']['confirmed']:.0%}"},
            {"": f"Same zones moved to random steep places ({ch.get('trials', 0)} trials)", "Found again": "",
             "Partial": "", "Not seen": "", "Not covered by track 106": "",
             "Found-again rate": f"{(ch.get('confirmed') or 0):.1%}"},
        ]), hide_index=True, width="stretch")
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
                f"{k_}: {v_.get('confirmed', 0)} of "
                f"{v_.get('confirmed', 0) + v_.get('partial', 0) + v_.get('not seen', 0)} found again"
                for k_, v_ in sorted(by.items(), key=lambda kv: ["high", "medium", "low"].index(kv[0]))))
    else:
        st.info("Runs once the track-106 files are cropped.")
with tabs[2]:
    if dc:
        short(f"{dc['found']} of {dc['zones_main']} zones survive when slope comes from NASA's NASADEM, including "
              f"{dc['by_confidence'].get('high', {}).get('found', 0)} of {dc['by_confidence'].get('high', {}).get('zones', 0)} "
              "high-confidence ones.")
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
            [{"Not found with NASADEM because": k_[0].upper() + k_[1:].replace(" in NASADEM", ""), "Zones": v_}
             for k_, v_ in rs.items()]), hide_index=True, width="content")
        rh = dc["reported_slide_hits"]
        hits = [s for s in dc["reported_slides"] if s["main"] == "hit"]
        if hits and rh["nasadem"] < rh["main"]:
            dist = " and ".join(f"{s['main_distance_m'] / 1000:.1f} km" for s in hits)
            same = len(rh["main_hit_zones"]) == 1
            st.markdown(
                (f"The {len(hits)} reported landslides we matched ({', '.join(s['id'] for s in hits)}) are "
                 f"{'both' if len(hits) == 2 else 'all'} matched to the same zone, {rh['main_hit_zones'][0]}, {dist} "
                 "away. " if same else
                 f"The {len(hits)} reported landslides we matched are {dist} from their nearest zone. ")
                + f"With NASADEM, {rh['nasadem']} of {rh['scored']} reports have a zone within range. "
                  "So treat the landslide matches as weak support.")
        both = [f["properties"]["id"] for f in (data.geojson("slide_zones.geojson") or {}).get("features", [])
                if f["properties"].get("nasadem") == "found" and f["properties"].get("track106") == "confirmed"]
        if both:
            st.markdown(f"Passing both extra checks (found again by the second NISAR track and with NASADEM): "
                        f"**{', '.join(both)}**.")
with tabs[3]:
    if sens and sens.get("rows"):
        r0 = sens["range"]
        short(f"the reservoir rise holds up ({r0['rise_km2'][0]:.1f} to {r0['rise_km2'][1]:.1f} km²); the flood area "
              f"does not ({r0['flood_km2'][0]:.2f} to {r0['flood_km2'][1]:.1f} km²), so read it as an order of magnitude.")
        st.markdown(
            "The water threshold is set from the radar itself on each date. Moving both dates' thresholds 1 dB down or "
            f"up, and changing nothing else, keeps reservoir and river rise between **{r0['rise_km2'][0]:.1f} and "
            f"{r0['rise_km2'][1]:.1f} km²** (we report {sens['base']['rise_km2']:.1f}). Flooding on ground that was "
            f"never wet swings from **{r0['flood_km2'][0]:.2f} to {r0['flood_km2'][1]:.1f} km²** (we report "
            f"{sens['base']['flood_km2']:.2f}): that figure depends heavily on the threshold, so read it as the order "
            "of magnitude, not a precise area.")
        st.dataframe(pd.DataFrame([{
            "Threshold shift": f"{r['shift_db']:+.0f} dB" if r["shift_db"] else "as chosen",
            "Threshold 28 Jun (dB)": round(r["threshold_before_db"], 1),
            "Threshold 10 Jul (dB)": round(r["threshold_after_db"], 1),
            "New water (km²)": r["new_water_km2"], "Reservoir and river rise (km²)": r["rise_km2"],
            "Flooding (km²)": r["flood_km2"], "Flood patches": r["flood_patches"],
            "Permanent water seen dark": f"{r['permanent_water_seen_dark']:.0%}"} for r in sens["rows"]]),
            hide_index=True, width="stretch")
with tabs[4]:
    ws = data.table("water_stats.csv")
    if ws is not None:
        st.dataframe(ws, hide_index=True, width="stretch")
    st.markdown(
        f"Sanity check: on {before} the radar saw **{(m.get('water', {}).get('permanent_water_seen_dark') or 0):.0%}** "
        "of the JRC permanent-water pixels as water. A low value would mean the threshold or the data is off.")

# ---------------------------------------------------------------- data
st.markdown("## Data")
ROLE = {"before": "before, track 034", "after": "after, track 034", "pair": "coherence, track 034",
        "check_before": "second-track check, before, track 106", "check_after": "second-track check, after, track 106",
        "check_pair": "second-track check, coherence, track 106"}
rows = [{"Data": f"NISAR L2 {'GUNW' if s['role'].endswith('pair') else 'GCOV'} ({ROLE.get(s['role'], s['role'])})",
         "File": s["granule_id"], "Valid share of box": f"{s['valid_fraction']:.0%}", "Link": s["url"]}
        for s in srcs]
rows += [
    {"Data": "Permanent water", "File": "JRC Global Surface Water v1.4 occurrence (Pekel et al., 2016)",
     "Valid share of box": "", "Link": "https://global-surface-water.appspot.com/"},
    {"Data": "Elevation and slope", "File": "Copernicus GLO-30 DEM (ESA)", "Valid share of box": "",
     "Link": "https://registry.opendata.aws/copernicus-dem/"},
    {"Data": "Place names", "File": "OpenStreetMap villages, towns and suburbs (ODbL), via Overpass and Nominatim",
     "Valid share of box": "", "Link": "https://www.openstreetmap.org/copyright"},
]
if dc:
    rows.append({"Data": "Elevation, second-map check", "File": "NASADEM_HGT v001 (NASA / USGS)",
                 "Valid share of box": "", "Link": dc["check_dem_url"]})
rain = data.rainfall()
if rain is not None:
    src = str(rain["source"].iloc[0]) if "source" in rain else "daily rainfall"
    link = "https://power.larc.nasa.gov/" if "POWER" in src else "https://giovanni.gsfc.nasa.gov/"
    rows.append({"Data": "Daily rainfall", "File": src, "Valid share of box": "", "Link": link})
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
             column_config={"Link": st.column_config.LinkColumn("Link")})

# ---------------------------------------------------------------- limits
st.markdown("## Limits")
seen = (m.get("water", {}).get("permanent_water_seen_dark") or 0)
LIMITS = [
    ("Provisional data", "These are NISAR provisional products (released from June 2026); calibration may still change."),
    ("Two snapshots, twelve days apart", f"Anything that flooded and drained between {data.nice_date(before, False)} "
                                         f"and {data.nice_date(after)} is invisible."),
    ("Cities", "Buildings make flooded streets bright, not dark. Our new-water map under-counts urban flooding."),
    ("Pixel size", f"{m['grid']['res_m']:.0f} m pixels. Slides narrower than about two pixels are easily missed."),
    ("Same-mode rule", "From 27 August to 2 October NISAR imaged this track in a different mode (2005, quad-pol); "
                       "14 October is back in the July mode. Brightness is only compared between passes with the same "
                       "track, mode and polarisation."),
    ("Water areas may be underestimates", f"On {data.nice_date(before)} only {seen:.0%} of the area the JRC record marks "
                                          "as permanent water looked dark enough to pass our water test. Part of that "
                                          "is reservoirs drawn down before the monsoon; part is water roughened by wind "
                                          "or rain, which our test misses."),
    ("Small samples", f"Every check is counted, not turned into an accuracy: floods "
                      f"{val_s.get('flood', {}).get('hits', 0)} of {val_s.get('flood', {}).get('observable', 0)}, "
                      f"landslides {val_s.get('slide', {}).get('hits', 0)} of "
                      f"{val_s.get('slide', {}).get('observable', 0)}, and the second-track check covers only part of "
                      "the area."),
    ("Flood area is threshold-sensitive", "The flood figure can move several-fold with a 1 dB change in the water "
                                          "threshold; the reservoir rise much less (see the water-threshold check)."),
    ("Slope near the limits", f"Many zones sit close to the {th.get('slide_min_slope_deg', 15):.0f}° or "
                              f"{th.get('slide_max_slope_deg', 45):.0f}° limits, so a different elevation map moves "
                              "some of them in or out (see the elevation-map check)."),
    ("Leads, not verdicts", f"Slide zones are places to check, not confirmed landslides: "
                            f"{val_s.get('unreported_slide_zones', 0)} of {m.get('slides', {}).get('zones', 0)} have no "
                            "reported event within 2 km."),
    ("Rainfall", "GPM IMERG Late Run, averaged over the whole study area per UTC day. It is lower than the "
                 "single-station totals quoted in the news, and may shift slightly when the Final Run is released."),
]
st.markdown('<div class="ml-cardgrid">' + "".join(
    f'<div class="lim"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>' for t, d in LIMITS) + "</div>",
    unsafe_allow_html=True)

# ---------------------------------------------------------------- reproduce
st.markdown("## Reproduce it")
st.markdown("The code is public, and the Pune crops of every NISAR file above are in the repository (a few MB each), "
            "so one command rebuilds every number, map and list in this app from them. Fetching the crops again from "
            "NASA's archive needs a free Earthdata login.")
st.code("pip install -r requirements-pipeline.txt\n"
        "python -m pipeline.run_all        # water, slide zones, checks, evidence, maps, metrics.json\n"
        "python -m pytest -q               # the pipeline's tests\n\n"
        "# optional: fetch the crops again from NASA's archive (Earthdata login)\n"
        "python -m pipeline.crop --primary --timeline\n"
        "python -m pipeline.crop --granule <a track-106 file from the Data table>", language="bash")
st.markdown("To point it at another place, change the study box and the NISAR files in `pipeline/config.py`.")

st.markdown("## Team")
st.markdown('<div class="ml-cardgrid">'
            '<div><b>Ayush Singh Negi</b><p>App and integration</p></div>'
            '<div><b>Rajendra Singh Negi</b><p>Data and science</p></div>'
            '<div><b>Urvashi</b><p>Validation, story and pitch</p></div></div>', unsafe_allow_html=True)
st.caption("Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen.")
ui.sources_line()
