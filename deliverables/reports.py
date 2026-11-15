"""The three MonsoonLens reports, typeset as PDFs and exported as HTML for Google Docs.

Every pipeline number is read from data/derived; every outside number comes from deliverables/facts.py, with its
source. Business-plan prices and projections are planning assumptions and are labelled as such.

  python deliverables/reports.py            # -> deliverables/out/reports/*.pdf and *_docs.html
"""
from __future__ import annotations

import asyncio
import html
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "deliverables"))
import facts as F  # noqa: E402

DER = ROOT / "data" / "derived"
OUT = ROOT / "deliverables" / "out" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
FIG = ROOT / "deliverables" / "out" / "fig"
SCR = ROOT / "deliverables" / "out" / "screens"
ASSET_URL = os.environ.get("ASSET_URL", "https://raw.githubusercontent.com/AyushSinghNegi/dancing-with-the-sars/"
                                        "claude/deliverables/deliverables/assets")
APP, REPO = "https://monsoonlens.streamlit.app", "https://github.com/AyushSinghNegi/dancing-with-the-sars"
LOGO = ROOT / "app" / "assets" / "igenfinity_logo.jpg"

M = json.loads((DER / "metrics.json").read_text())
FB = json.loads((DER / "flood_baseline.json").read_text())
W, S, V, XT, DC, SE = M["water"], M["slides"], M["validation"], M["crosstrack"], M["dem_check"], M["sensitivity"]
CLOUD = json.loads((ROOT / "data" / "reference" / "cloud_check.json").read_text())
ZONES = [f["properties"] for f in json.loads((DER / "slide_zones.geojson").read_text())["features"]]
TH = M["thresholds"]

# ---------------------------------------------------------------- citations
_REFS: list[str] = []


def cite(key):
    if key not in _REFS:
        _REFS.append(key)
    n = _REFS.index(key) + 1
    return f'<sup class="ref"><a href="#ref-{n}">[{n}]</a></sup>'


def refs_reset():
    _REFS.clear()


def references():
    rows = []
    for i, k in enumerate(_REFS, 1):
        text, url = F.SOURCES[k]
        rows.append(f'<li id="ref-{i}">{html.escape(text)} <a href="{url}">{html.escape(url)}</a></li>')
    return '<h2 style="break-before: page">References</h2><ol class="refs">' + "".join(rows) + "</ol>"


# ---------------------------------------------------------------- building blocks
def fig(name, caption, width=100, theme="light", screen=False):
    folder = "screens" if screen else "fig"
    fname = f"{name}.png" if screen else f"{name}_{theme}.png"
    return {"t": "fig", "folder": folder, "file": fname, "caption": caption, "width": width}


def kpis(items):
    return {"t": "kpis", "items": items}


def callout(title, body, tone="blue"):
    return {"t": "callout", "title": title, "body": body, "tone": tone}


def table(head, rows, widths=None, small=False):
    return {"t": "table", "head": head, "rows": rows, "widths": widths, "small": small}


def p(x):
    return {"t": "p", "html": x}


def h2(x):
    return {"t": "h2", "text": x}


def h3(x):
    return {"t": "h3", "text": x}


def ul(items):
    return {"t": "ul", "items": items}


def pb():
    return {"t": "pb"}


def n(x, d=1):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- report 1: business plan
def business_plan():
    refs_reset()
    cost_world = F.yearly_cost(F.EARTH_LAND_KM2)
    cost_india = F.yearly_cost(F.INDIA_PRONE_KM2)
    cost_tile = F.yearly_cost(F.TILE_KM2)
    tiles_world = F.EARTH_LAND_KM2 / F.TILE_KM2
    total_fc = F.SDRF_CR + F.SDMF_CR + F.NDRMF_CR
    plan_rows = [[p_["year"], p_["districts"], f"{p_['coverage_mkm2']:g}", f"${p_['revenue_k']:,}k", f"${p_['grants_k']:,}k",
                  f"${p_['cost_k']:,}k", f"${p_['revenue_k'] + p_['grants_k'] - p_['cost_k']:,}k"] for p_ in F.PLAN]
    blocks = [
        h2("1. Executive summary"),
        p("<b>Monsoon cloud hides the ground exactly when people need to see it.</b> From 3 to 8 July 2026, while floods "
          f"and landslides hit Pune district in India, all {CLOUD['all_cloud']} of NASA's available daily satellite photos "
          "of the area showed only cloud. The NASA–ISRO NISAR satellite carries an L-band radar that sees through cloud "
          f"and rain, covers nearly all land twice every 12 days, and publishes its data free{cite('nisar_overview')}"
          f"{cite('nisar_open')}."),
        p("<b>MonsoonLens turns those radar passes into maps and field check lists that a district disaster team can "
          "act on.</b> In our working prototype for Pune it found "
          f"{n(W['rise_km2'])} km² of new water as reservoirs and rivers rose, {S['zones']} likely landslide zones "
          f"({S['high']} of them high confidence), and it publishes a ranked list with radar images, KML for phones and a "
          "printable sheet. Every result is checked, and the weak checks are shown too."),
        kpis([(f"{XT['lift_confirmed']:.0f}×", "a second NISAR orbit re-found our slide zones more often than chance "
               f"(p ≈ {XT['p_value']:.2f})"),
              (f"{DC['found']} of {DC['zones_main']}", "slide zones kept when re-run with NASA's NASADEM elevation map"),
              (f"{F.PIPELINE_SECONDS // 60} min {F.PIPELINE_SECONDS % 60} s", "to rebuild every map and list from one "
               "NISAR pair on a 2-core machine"),
              (f"${cost_world:,.0f}", "compute per year to run it on every pass over all land on Earth")]),
        p("<b>The business is open-core.</b> The public layer (the app, the maps and the code) stays free. District, "
          "state and infrastructure teams pay for what makes it operational: their own area, an alert after every pass, "
          "a field app, training and support. Compute is not the cost driver: running the full pipeline on every NISAR "
          f"pass over India's entire landslide-prone area costs about ${cost_india:,.0f} a year in cloud compute. The "
          "cost is people: support, field validation and partnerships."),
        p("<b>What we ask for now:</b> a monsoon-season pilot with three district teams in the Western Ghats in 2027, "
          "and seed funding to make the pipeline run automatically on every new NISAR pass."),
        h2("2. The problem"),
        h3("Cloud blinds the satellites people rely on"),
        p("Optical satellites, the source of most disaster maps, cannot see through cloud. During the July 2026 storm "
          f"over Pune, {CLOUD['all_cloud']} of {CLOUD['images_available']} daily images from four NASA sensors "
          f"({', '.join(CLOUD['sensors'])}) showed only cloud from {CLOUD['from'][8:]} to {CLOUD['to'][8:]} July. That is "
          "the week the floods and landslides happened. Radar does not need sunlight or clear sky."),
        fig("rain", "Daily rain over the study area (NASA GPM IMERG Late Run, area average). The dotted lines are the two "
                    "NISAR passes compared; floods and landslides were reported in the shaded week.", 92),
        h3("Landslides and floods kill, and they repeat"),
        p(f"Between 2004 and 2016, {F.LANDSLIDE_DEATHS_2004_2016:,} people died in {F.LANDSLIDE_EVENTS_2004_2016:,} "
          f"non-seismic landslides worldwide, with Asia the dominant region{cite('froude')}. In India about "
          f"{F.INDIA_PRONE_KM2 / 1e6:.2f} million km², {F.INDIA_PRONE_SHARE}% of the land, is landslide-prone"
          f"{cite('ndma_lrms')}, including about {F.WGHATS_PRONE_KM2 / 1e6:.2f} million km² in the Western Ghats and Konkan "
          f"hills{cite('gsi_wghats')}, where our study area lies."),
        p(f"The Western Ghats keep paying: the Malin landslide in Pune district killed {F.MALIN_DEATHS} people in 2014, and "
          f"Taliye in neighbouring Raigad killed {F.TALIYE_DEATHS} in 2021{cite('malin')}. In Kerala, the 2024 "
          f"Mundakkai–Chooralmala disaster has an official toll of {F.WAYANAD_DEATHS}{cite('wayanad')}. Floods reach "
          f"further still: {F.FLOOD_EXPOSED_BN} billion people are directly exposed to 1-in-100-year floods, "
          f"{F.FLOOD_EXPOSED_INDIA_M} million of them in India{cite('rentschler')}."),
        callout("Why this matters for a district team",
                "After a storm, a district team has to decide where to send engineers and survey crews first. Today that "
                "decision rests on phone calls and news reports, which come from where people are, not from where the "
                "hill moved. A radar map of where the ground changed, with each spot ranked and checked, gives them a "
                "list to start from on the day the data arrives."),
        h2("3. The solution: MonsoonLens"),
        p("MonsoonLens is an open pipeline and a public web app. The pipeline reads NISAR level-2 radar products, maps "
          "water on each date, finds new water, flags likely landslide zones, checks every result four independent ways, "
          "and packages the evidence. The app shows it in six pages, in English, Hindi, Marathi and German, on desktop and "
          "phone, with a guided tour for first-time visitors."),
        table(["Page", "Who it serves", "What it does"], [
            ["Overview", "Everyone", "The findings, how sure we are, and a 3D fly-over of the results on a model of the land"],
            ["Story", "The public, media", "Six short chapters from the rain to what radar could not see"],
            ["Explore the map", "Analysts", "Every layer, the season slider, and the radar evidence for each zone"],
            ["Check a place", "Residents", f"Pick one of 431 villages and towns and see what was found within 2, 5 or 10 km; "
                                           "the result has its own link"],
            ["Field check list", "District teams", "Every likely slide zone ranked, with radar images, nearby roads and "
                                                   "villages, as a printable sheet, KML, CSV and GeoJSON"],
            ["Method and limits", "Researchers", "Every NISAR file, step, threshold, check and limit"],
        ], widths=[18, 18, 64]),
        fig("hero", "The MonsoonLens Overview (dark mode).", 100, screen=True),
        h3("What it found in Pune, and how sure we are"),
        fig("map_findings", "NISAR radar on 10 July 2026 with the changes since 28 June: rising reservoirs and rivers "
                            "(blue), flood water on dry land (white), likely slide zones (orange) and the 18 reported "
                            "events (triangles).", 82),
        table(["Result", "Value", "How sure"], [
            ["New water as reservoirs and rivers rose", f"{n(W['rise_km2'])} km²",
             f"Holds up: {n(SE['range']['rise_km2'][0])} to {n(SE['range']['rise_km2'][1])} km² with the water threshold moved ±1 dB"],
            ["Flood water still standing on dry land on 10 July", f"{W['flood_km2']:.2f} km²",
             f"Order of magnitude only: {SE['range']['flood_km2'][0]:.2f} to {SE['range']['flood_km2'][1]:.1f} km² with ±1 dB"],
            ["Likely landslide zones", f"{S['zones']} ({S['high']} high confidence)",
             f"Second orbit {XT['lift_confirmed']:.0f}× chance; NASADEM keeps {DC['found']} of {DC['zones_main']}"],
            ["Reported floods with a detection nearby", f"{V['flood']['hits']} of {V['flood']['observable']}",
             f"No better than chance ({FB['reference']['flat_ground']['expected_matches']:.1f} at random places): city "
             "flooding hides from radar"],
        ], widths=[38, 20, 42]),
        p("We publish the weak results as plainly as the strong ones. Radar finds landslide scars and rising reservoirs "
          "well; it does not find water between buildings, so city flood reports are mostly missed. That limit shapes "
          "the product: MonsoonLens is a landslide and water-rise lead generator first, and an urban flood map only "
          "once the science supports it (Section 9)."),
        h2("4. Why now: NISAR changes the economics"),
        ul([f"<b>Free, open and global.</b> NISAR's science data is free to everyone, in line with NASA's open-data policy"
            f"{cite('nisar_open')}, and the mission scans nearly all of Earth's land and ice twice every 12 days"
            f"{cite('nisar_overview')}.",
            f"<b>L-band sees through cloud and canopy.</b> Its 24 cm wavelength works day and night, through monsoon "
            f"cloud and partly through forest{cite('nisar_asf')}.",
            f"<b>The data already sits in the cloud.</b> All NISAR data is hosted in NASA's Earthdata Cloud on AWS in "
            f"us-west-2, so processing can run next to the archive without downloading it{cite('nisar_s3')}.",
            "<b>The method is cheap.</b> Our full pipeline needs no GPU and no labelled training data. That is why one "
            "pass over the whole land surface costs about a dollar per 64 tiles of 7,000 km² (Section 7)."]),
        h2("5. Customers and market"),
        table(["Segment", "Their problem", "What they buy", "Examples (targets, not partners)"], [
            ["District and state disaster authorities", "Where to send survey crews after a storm",
             "Their area watched every pass; ranked leads; alerts; training", "District Disaster Management Authorities, "
             "State Disaster Management Authorities in the Western Ghats states"],
            ["Infrastructure operators", "Slopes above rail lines, highways, dams and mines",
             "Corridor watch and change reports after each pass", "Ghat rail sections, expressways, hydropower and mining operators"],
            ["Insurers and reinsurers", "Fast, independent evidence of where damage happened",
             "API access to history and new passes", "Parametric and catastrophe-risk teams"],
            ["Humanitarian and development", "Situational awareness when cloud blocks optical imagery",
             "Data feed and joint products", "Red Cross and Red Crescent societies, UN agencies, development banks"],
            ["Researchers and media", "Trustworthy, citable maps", "Free public layer", "Universities, journalists"],
        ], widths=[20, 24, 26, 30], small=True),
        h3("The money already exists"),
        p(f"India's 15th Finance Commission set aside ₹{F.SDRF_CR:,} crore for State Disaster Response Funds, "
          f"₹{F.SDMF_CR:,} crore for State Disaster Mitigation Funds{cite('sdrf')}{cite('sdmf')}, and ₹{F.NDRMF_CR:,} crore "
          f"for the National Disaster Risk Management Fund for 2021–26{cite('fc15')}: ₹{total_fc:,} crore in all. The "
          "mitigation windows exist precisely for tools that reduce risk before and between disasters."),
        fig("funding", "India's disaster-management funds for 2021–26 (15th Finance Commission).", 88),
        p(f"Globally, the value added by Earth observation data is estimated at ${F.EO_VALUE_2023_BN} billion in 2023, "
          f"rising to over ${F.EO_VALUE_2030_BN} billion by 2030{cite('wef')}. Early warning is among the best-returning "
          f"investments: 24 hours of warning can cut damage by {F.WARNING_24H_DAMAGE_CUT}%, and ${F.EW_SPEND_M} million spent "
          f"on such systems in developing countries would avoid ${F.EW_AVOIDED_BN[0]}–{F.EW_AVOIDED_BN[1]} billion in losses "
          f"a year{cite('gca')}. The UN's Early Warnings for All initiative aims to protect everyone on Earth by 2027"
          f"{cite('ew4all')}, and WMO puts the return at up to ${F.WMO_DOLLAR_SAVES} saved for every dollar"
          f"{cite('wmo_15')}."),
        callout("What we have not yet proven",
                "We have not surveyed willingness to pay. The prices and projections in this plan are planning "
                "assumptions, to be tested in the 2027 pilots. MonsoonLens produces leads for ground checks, not "
                "warnings, and it has not yet been validated in the field.", tone="orange"),
        h2("6. Business model"),
        p("<b>Open core.</b> Everything needed to reproduce our results stays open: the code (MIT licence), the public "
          "app and the maps. Paying customers fund the operational layer around it."),
        table(["Tier", "Price per year (assumption)", "What it includes"],
              [[k, "Free" if v[0] == 0 else f"${v[0]:,}", v[1]] for k, v in F.PRICES.items()], widths=[18, 22, 60]),
        p("<b>Grants and public funding</b> carry the first two years: open-science and disaster-risk programmes fund "
          "exactly this kind of public good. <b>Services</b> (training, custom analysis, integration into state "
          "emergency systems) add revenue without closing the core."),
        h2("7. What it costs to run, from one district to the whole Earth"),
        p(f"We timed the full pipeline (water, slide zones, every check, evidence chips, maps and the field list) on "
          f"15 November 2026: {F.PIPELINE_SECONDS} seconds on a 2-core machine, starting from the cropped NISAR files. On a "
          f"4-core cloud machine priced at ${F.INSTANCE_USD_PER_H}/hour on demand in us-west-2{cite('aws')}, and allowing "
          f"{F.OVERHEAD}× for streaming the radar data, retries and idle time, one run over a {F.TILE_KM2:,} km² tile costs "
          f"about ${F.COST_PER_TILE_RUN_USD:.3f}. NISAR passes each place twice every 12 days, about {F.RUNS_PER_YEAR} runs "
          "a year."),
        fig("cost_to_cover", "Yearly compute cost to run MonsoonLens on every NISAR pass, by area watched. Measured "
                             "runtime, published cloud prices, and a 3× allowance for data access.", 92),
        table(["Area watched", "Area (km²)", "Tiles", "Compute per year"], [
            ["Pune study area", f"{F.TILE_KM2:,}", "1", f"${cost_tile:,.2f}"],
            ["Western Ghats and Konkan, landslide-prone", f"{F.WGHATS_PRONE_KM2:,}", f"{F.WGHATS_PRONE_KM2 / F.TILE_KM2:.0f}",
             f"${F.yearly_cost(F.WGHATS_PRONE_KM2):,.0f}"],
            ["All of India's landslide-prone area", f"{F.INDIA_PRONE_KM2:,}", f"{F.INDIA_PRONE_KM2 / F.TILE_KM2:.0f}",
             f"${cost_india:,.0f}"],
            [f"All land on Earth{cite('cia_land')}", f"{F.EARTH_LAND_KM2:,}", f"{tiles_world:,.0f}", f"${cost_world:,.0f}"],
        ], widths=[44, 20, 14, 22]),
        p("Storage of results is small (a few MB per tile and pass) and NASA does not charge for in-region data access. "
          "The conclusion is the core of the business case: <b>watching the whole planet is affordable; the scarce "
          "resource is people who turn leads into action.</b>"),
        pb(),
        h2("8. Five-year financial plan"),
        callout("Planning assumptions, not forecasts",
                "The figures below show how the business could fund itself if the pilots succeed. They are built from "
                "the price list in Section 6 and the coverage plan in Section 9, with staffing as the main cost.",
                tone="orange"),
        fig("revenue", "Revenue, grants and operating cost by year (planning assumptions).", 92),
        table(["Year", "Customers / reach", "Coverage (M km²)", "Revenue", "Grants", "Cost", "Net"], plan_rows,
              widths=[9, 27, 14, 13, 12, 12, 13], small=True),
        p("Operating cost is mostly people: a small core team in year one (two engineers, one scientist, one field and "
          "partnerships lead), growing with each region for customer support, field validation and localisation. "
          "Cloud compute stays below 1% of cost at every stage."),
        h2("9. Global scale-up plan"),
        fig("coverage", "Coverage plan: from the Pune pilot to all land on Earth.", 88),
        h3("From one district to every NISAR pass on Earth"),
        ul(["<b>Event-driven.</b> A watcher on NASA's catalogue starts a job the moment a new NISAR pass over a watched "
            "tile is published. No one has to press a button.",
            f"<b>Tiled.</b> The world's land splits into about {tiles_world:,.0f} tiles the size of our study box; each runs "
            "on its own worker next to the data in us-west-2, so cost grows linearly and time does not.",
            "<b>Self-calibrating.</b> Water thresholds are already trained per date from the JRC water record, which is "
            "global. Slope comes from the global Copernicus GLO-30 elevation model, checked against NASADEM.",
            "<b>Standard outputs.</b> Cloud-optimised GeoTIFFs, a STAC catalogue for analysts, and Common Alerting "
            "Protocol messages that state emergency systems can ingest.",
            "<b>Local by design.</b> The app already runs in four languages; each new region adds its languages, place "
            "names from OpenStreetMap and its own reported events."]),
        h3("Science roadmap"),
        ul(["Use both orbit directions (ascending and descending) so slopes facing away from one pass face the other.",
            "Add InSAR motion time series to find slopes that creep before they fail.",
            "Fuse ISRO's S-band channel and ESA's Sentinel-1 C-band for more looks per week and continuity beyond NISAR's "
            "three-year prime mission.",
            "Attack our weakest result, urban floods, with double-bounce brightening and coherence loss between buildings.",
            "Learn a ranking from field-verified outcomes once district teams report back."]),
        fig("roadmap", "Roadmap from the hackathon prototype to global coverage.", 100),
        h2("10. Go-to-market"),
        table(["Phase", "When", "Goal", "How we get there"], [
            ["0. Open prototype", "Now", "Credibility", "Public app, open code, published checks, this plan"],
            ["1. Pilots", "2027 monsoon", "Prove field value", "Three district teams in the Western Ghats; weekly leads; "
                                                               "a shared field form; joint review after the season"],
            ["2. Western Ghats", "2028", "First paying customers", "District subscriptions; one infrastructure corridor"],
            ["3. India", "2029", "National scale", "State contracts; work with national agencies on landslide early warning"],
            ["4. Global", "2030 on", "Every NISAR pass", "Partners in other monsoon and mountain regions; open global layer"],
        ], widths=[17, 14, 19, 50], small=True),
        h2("11. Impact we will measure"),
        table(["Metric", "Target for the 2027 pilot"], [
            ["Time from a NISAR pass being published to the field list", "Under 1 hour"],
            ["Leads checked on the ground within 72 hours", "At least half of high-confidence leads"],
            ["Share of checked leads that show fresh ground failure", "Reported every season, whatever it is"],
            ["People living within 2 km of a lead who can look it up", "Every village in the pilot districts"],
            ["Languages available", "At least the official language of every pilot state"],
        ], widths=[60, 40]),
        h2("12. Risks and how we handle them"),
        table(["Risk", "What we do about it"], [
            ["False leads waste crews' time", "Rank by evidence and independent checks; show every check; publish the "
                                             "field-verified hit rate each season"],
            ["Urban floods are missed", "Say so on every page; treat urban flooding as research until it validates"],
            ["NISAR products are provisional", "Track calibration updates; re-run history when products are reprocessed"],
            ["Mission lifetime (3-year prime mission)", "Add Sentinel-1 and S-band so the service outlives one satellite"],
            ["Leads read as warnings and cause alarm", "Call them leads, not landslides; send them to officials first; the "
                                                       "public page explains limits in plain words"],
            ["Slow institutional adoption", "Start with pilots that cost districts nothing; fit their existing workflow"],
        ], widths=[35, 65]),
        h2("13. Team"),
        p("<b>Team iGenfinity</b>, NASA Space Apps Challenge 2026 (GDG Ahlen): <b>Ayush Singh Negi</b> (app and "
          "integration, team lead), <b>Rajendra Singh Negi</b> (data and science), <b>Urvashi</b> (validation, story and "
          "pitch)."),
        p("<i>Use of AI:</i> parts of the code, text and translations were drafted with an AI assistant and checked by "
          "the team. Every number comes from the pipeline output or a cited source. No NASA logos are used."),
    ]
    return dict(title="Business Plan and Global Scale-Up",
                subtitle="Turning free NASA–ISRO radar into cloud-proof landslide and flood leads, from one district to "
                         "every NISAR pass on Earth", blocks=blocks, refs=references())


# ---------------------------------------------------------------- report 2: technical and validation
def technical():
    refs_reset()
    srcs = M["sources"]
    top = sorted(ZONES, key=lambda z: (-z["score"], z["id"]))
    T106 = {"confirmed": "found again", "partial": "partly", "not seen": "not seen", "not covered": "outside view"}
    zone_rows = [[z["id"], z.get("near") or "", z["confidence"], f"{z['score']:.2f}", f"{z['slope_deg']:.0f}°",
                  T106.get(z.get("track106"), ""), "kept" if z.get("nasadem") == "found" else "not kept",
                  f"{z['nearest_event_km']:.1f} km" if z.get("nearest_event_km") is not None else ""] for z in top]
    blocks = [
        h2("1. Summary"),
        p(f"We compared two NISAR L-band radar passes over Pune district, India, from 28 June and 10 July 2026, on either "
          f"side of the 3–8 July floods and landslides. The pipeline mapped {n(W['new_water_km2'])} km² of new open water, "
          f"of which {n(W['rise_km2'])} km² was reservoirs and rivers rising and {W['flood_km2']:.2f} km² was flood water on "
          f"ground with no water on record since 1984. It flagged {S['zones']} likely landslide zones on slopes of "
          f"{TH['slide_min_slope_deg']:.0f}° to {TH['slide_max_slope_deg']:.0f}°, {S['high']} of them high confidence."),
        kpis([(f"{XT['lift_confirmed']:.0f}×", f"second-orbit re-finds vs chance (p ≈ {XT['p_value']:.3f})"),
              (f"{DC['found']}/{DC['zones_main']}", "zones kept with NASADEM"),
              (f"{V['slide']['hits']}/{V['slide']['observable']}", "reported landslides with a zone nearby"),
              (f"{V['flood']['hits']}/{V['flood']['observable']}", "reported floods matched: no better than chance")]),
        p("The landslide and reservoir results hold up under independent checks. The flood matches do not beat chance: "
          "the reported floods were mostly in built-up areas, where radar sees flooded streets as bright, not dark."),
        h2("2. Event and study area"),
        p(f"The study box spans longitude {M['aoi']['west']}–{M['aoi']['east']}° E and latitude {M['aoi']['south']}–"
          f"{M['aoi']['north']}° N ({F.TILE_KM2:,} km²): the Western Ghats hills in the west, Pune city in the east. Rain "
          f"peaked in early July; from {CLOUD['from'][8:]} to {CLOUD['to'][8:]} July all {CLOUD['all_cloud']} available "
          f"daily optical images from four NASA sensors showed only cloud{cite('worldview')}."),
        fig("rain", "Daily rain, area average, NASA GPM IMERG Late Run; the dotted lines are the two NISAR passes.", 92),
        p(f"NISAR's L-band radar (24 cm wavelength) images nearly all land twice every 12 days{cite('nisar_overview')}; "
          f"its products are free and hosted in NASA's Earthdata Cloud{cite('nisar_asf')}{cite('nisar_s3')}. Rain comes "
          f"from GPM IMERG{cite('imerg')}."),
        h2("3. Data"),
        table(["Data", "Product", "Use"], [
            [f"NISAR L2 GCOV, track 34", "28 Jun and 10 Jul 2026, DHDH, mode 4005", "Backscatter HH and HV, water, change"],
            ["NISAR L2 GUNW, track 34", "28 Jun – 10 Jul pair", "Coherence for slide zones"],
            ["NISAR L2 GCOV/GUNW, track 106", "3 – 15 Jul 2026 pair", "Independent second-orbit check"],
            ["NISAR L2 GCOV, track 34 timeline", "5 same-mode passes, 28 Jun – 14 Oct", "Reservoirs through the season"],
            [f"JRC Global Surface Water v1.4{cite('pekel')}", "Occurrence 1984–2021", "Training water thresholds; permanent water"],
            [f"Copernicus GLO-30 DEM{cite('copdem')}", "30 m", "Slope, aspect, radar layover and shadow"],
            [f"NASADEM{cite('nasadem')}", "30 m", "Second elevation check"],
            ["GPM IMERG Late Run", "Daily, area average", "Rain context"],
            [f"OpenStreetMap{cite('osm')}", "Places, roads, railways", "Names, nearby infrastructure, Check a place"],
            ["Reported events", f"{V['events']} floods and landslides with sources", "Validation"],
        ], widths=[30, 32, 38], small=True),
        p(f"All {len(srcs)} NISAR files are listed with links on the app's Method page."),
        h2("4. Method"),
        table(["Step", "What happens", "Key settings"], [
            ["1. Cut", "Stream only the study box from each GCOV file; average native pixels to a 40 m grid; Lee filter",
             f"{M['grid']['res_m']:.0f} m, UTM 43N"],
            ["2. Water", f"Per-date threshold by Kittler–Illingworth minimum error{cite('kittler')}, trained on JRC water "
                         "cores and land",
             f"kept within {TH['water_db_bounds'][0]} to {TH['water_db_bounds'][1]} dB; "
             f"thresholds {W['threshold_before_db']:.1f} / {W['threshold_after_db']:.1f} dB"],
            ["3. New water", "Water after, not before; clearly darker; outside permanent water; flat; big enough",
             f"≥ {TH['change_db']} dB; JRC < {TH['permanent_water_occurrence']}%; slope < {TH['flood_max_slope_deg']}°; "
             f"≥ {TH['min_patch_pixels']} px"],
            ["4. Hidden water", "Flat ground that got brighter (double bounce): shown, never counted", f"≥ {TH['change_db']} dB brighter"],
            ["5. Slide zones", "Low coherence, much lower than its 1 km neighbourhood, and a backscatter jump relative to "
                               "the scene's median change; outside layover and shadow",
             f"slope {TH['slide_min_slope_deg']:.0f}–{TH['slide_max_slope_deg']:.0f}°; coherence < {TH['coherence_low']}; "
             f"< 0.6× local; HH +{TH['slide_hh_rise_db']} dB or HV −{TH['slide_hv_drop_db']} dB"],
            ["6. Score", "0–1 from slope, radar change and coherence loss, each up to a third", "high / medium / low"],
            ["7–10. Checks", "Reported events, second orbit, second DEM, threshold ±1 dB", "Section 6"],
            ["11. Package", "Image chips per zone and patch; field list as HTML, KML, CSV, GeoJSON", f"{M['evidence']['chips']} chips"],
        ], widths=[13, 55, 32], small=True),
        h2("5. Results"),
        fig("map_findings", "Findings on the 10 July radar image.", 80),
        fig("before_after", "The area of most change, before and after, with the change image.", 100),
        fig("season", "Open water inside the JRC water extent on every same-mode pass of track 34.", 86),
        fig("chips", "Evidence for the highest-scoring zone that NASADEM keeps: radar colour before and after, and coherence.", 86),
        h2("6. Validation and checks"),
        fig("checks", "The four checks. From left: NASADEM agreement by confidence, second-orbit re-finds vs random "
                      "placement, reported-flood matches vs chance, and sensitivity to the water threshold.", 100),
        h3("Reported events"),
        p(f"{V['events']} reported floods and landslides, each with a source, were matched to detections within the larger "
          f"of 500 m (floods) or 750 m (landslides) and the report's own location precision. Floods: {V['flood']['hits']} "
          f"of {V['flood']['observable']} that radar could observe had a detection nearby. The same rule at places nobody "
          f"reported gives {FB['reference']['flat_ground']['expected_matches']:.1f} on random flat ground and "
          f"{FB['reference']['settlements']['expected_matches']:.1f} at random settlements: the flood matches are no better "
          f"than chance. Landslides: {V['slide']['hits']} of {V['slide']['observable']}, both near one zone that NASADEM "
          "does not keep, so weak support."),
        h3("Second NISAR orbit"),
        p(f"The same slide rule on the independent track-106 pair (3–15 July) re-found {XT['status_counts']['confirmed']} of "
          f"{XT['real']['zones_scored']} zones it could see ({XT['real']['confirmed'] * 100:.1f}%), against "
          f"{XT['chance']['confirmed'] * 100:.1f}% for the same zones moved to random steep places in "
          f"{XT['chance']['trials']} trials: {XT['lift_confirmed']:.0f}× chance, p ≈ {XT['p_value']:.3f}. Track 106 covers "
          f"only {XT['valid_fraction'] * 100:.0f}% of the box, so the sample is small: support, not proof."),
        h3("Second elevation map"),
        p(f"Re-running the slide rule with NASADEM keeps {DC['found']} of {DC['zones_main']} zones, including "
          f"{DC['by_confidence']['high']['found']} of {DC['by_confidence']['high']['zones']} high-confidence ones. The two "
          f"slope maps agree closely overall (median difference {DC['slope']['median_abs_diff_deg']:.0f}°, correlation "
          f"{DC['slope']['correlation']:.2f}); zones lost sit near the 15° and 45° limits."),
        h3("Water threshold"),
        p(f"Moving both dates' thresholds ±1 dB keeps the reservoir rise between {SE['range']['rise_km2'][0]:.1f} and "
          f"{SE['range']['rise_km2'][1]:.1f} km²; flood water on dry land swings from {SE['range']['flood_km2'][0]:.2f} to "
          f"{SE['range']['flood_km2'][1]:.1f} km², so we report it only as an order of magnitude."),
        h2("7. Limits"),
        ul(["Radar sees flooded streets between buildings as bright, so urban flooding is under-counted.",
            "Water that came and went between the two passes is invisible.",
            f"{M['grid']['res_m']:.0f} m pixels: slides narrower than about two pixels can be missed.",
            f"{S['layover_shadow_share_of_steep'] * 100:.1f}% of steep ground faces away from the radar and is left out.",
            "NISAR products are provisional; numbers may shift with recalibration.",
            "Every check is a count from a small sample, not an accuracy."]),
        h2("8. Reproducibility"),
        p(f"The code is public under the MIT licence at {REPO}. The Pune crops of every NISAR file are in the repository, "
          f"and <code>python -m pipeline.run_all</code> rebuilds every number, map and list in {F.PIPELINE_SECONDS} seconds "
          "on a 2-core machine (measured 15 November 2026). <code>python -m pytest -q</code> runs the tests."),
        pb(),
        h2("Appendix A. All likely slide zones"),
        table(["Zone", "Nearest place", "Conf.", "Score", "Slope", "2nd orbit", "NASADEM", "Nearest report"], zone_rows,
              widths=[8, 28, 9, 8, 8, 13, 12, 14], small=True),
    ]
    return dict(title="Technical and Validation Report",
                subtitle="What NISAR's L-band radar saw through the July 2026 Pune monsoon, and how we checked it",
                blocks=blocks, refs=references())


# ---------------------------------------------------------------- report 3: field operations guide
def field_guide():
    refs_reset()
    hi = [z for z in ZONES if z["confidence"] == "high"]
    blocks = [
        h2("1. What you get after every NISAR pass"),
        p("NISAR passes over each place twice every 12 days, cloud or not. After each pass MonsoonLens produces a "
          "<b>field check list</b>: every place on steep ground where the radar saw the surface change in a way that "
          "fits a landslide, ranked by evidence, with radar images of the spot and what is nearby."),
        fig("field", "The Field check list page: two main downloads, filters, and the ranked table.", 100, screen=True),
        table(["Download", "Use it for"], [
            ["Printable list with radar images", "A paper briefing pack for the control room and for crews"],
            ["KML for Google Earth and phone maps", "Navigation to each lead on a phone, offline once loaded"],
            ["CSV, GeoJSON, nearby CSV (Other formats)", "GIS, spreadsheets and your own systems"],
        ], widths=[40, 60]),
        callout("A lead is not a landslide",
                "Each zone is a place where the ground changed between two radar passes in a way that fits a slide. It "
                f"may be a fresh scar, a field ploughed, or a forest cut. In this pilot, {V['unreported_slide_zones']} of "
                f"{S['zones']} zones had no reported event within 2 km. Check before you act, and never present a lead to "
                "the public as a confirmed landslide.", tone="orange"),
        h2("2. How to prioritise"),
        ul(["<b>Confidence first.</b> Start with high-confidence zones (in this run, "
                   f"{len(hi)} of {S['zones']}).",
                   "<b>Independent checks next.</b> Zones found again by the second NISAR orbit, kept with NASADEM, or "
                   "near a reported event deserve an earlier visit (use the <i>Backed by an extra check</i> filter).",
                   "<b>Exposure.</b> Leads near a road, railway line or village matter more. The table shows the nearest "
                   "road and settlement for each zone.",
                   "<b>Access and safety.</b> Plan the route; do not send crews onto unstable ground in heavy rain."]),
        h2("3. Reading the evidence card"),
        fig("field_evidence", "An evidence card: radar images before and after, coherence, why it was flagged, extra "
                              "checks and what is nearby.", 100, screen=True),
        table(["On the card", "What it means"], [
            ["Steep ground", "Mean slope of the zone; slides are searched only between 15° and 45°"],
            ["Coherence", "How much the ground's fine radar pattern stayed the same; a slide scrambles it (dark = changed)"],
            ["HH rose / HV fell", "Rougher debris (HH up) or vegetation stripped away (HV down)"],
            ["Second NISAR orbit", "Whether an independent pass from another orbit also saw it"],
            ["NASADEM", "Whether the zone survives when slope comes from a second elevation map"],
            ["Reported event within 2 km", "Whether a news or official report exists nearby"],
        ], widths=[30, 70]),
        h2("4. On the ground: what to record"),
        table(["Record", "How"], [
            ["Location", "GPS point at the observation spot; note how far from the zone centre"],
            ["What you see", "Fresh scar, cracks, bulging, debris on road, tilted trees or poles, muddy water, nothing"],
            ["Photos", "Four directions plus a close-up; include a person or vehicle for scale"],
            ["Risk to people", "Houses, roads, rail or water lines below; people living within 500 m"],
            ["Verdict", "Confirmed slide / possible / no sign / could not reach"],
        ], widths=[25, 75]),
        p("Send each record back to the MonsoonLens team (in the pilot, through a shared form). Your verdicts are how the "
          "ranking improves and how we publish an honest hit rate."),
        h2("5. Talking to the public"),
        ul(["Use the <b>Check a place</b> page: residents pick their village and see what was found within 2, 5 or 10 km. "
            "Each result has its own link to share.",
            "Say <i>a place to check</i>, not <i>a landslide</i>, until a crew confirms it.",
            "Radar misses water between buildings: a quiet map of a town does not mean the town is safe.",
            "The app works in English, Hindi, Marathi and German; the tour button explains every page in a minute."]),
        h2("6. One-page checklist"),
        table(["Before", "During", "After"], [
            ["Download the new list and KML", "Visit high-confidence leads first", "Upload records and photos"],
            ["Filter: high confidence, extra checks", "Record GPS, photos, verdict", "Mark confirmed slides for engineers"],
            ["Check roads and villages near each lead", "Stay off unstable slopes in rain", "Brief the public with care"],
        ], widths=[33, 34, 33]),
    ]
    return dict(title="Field Operations Guide", subtitle="Using MonsoonLens leads after a monsoon storm: for district "
                "disaster management teams", blocks=blocks, refs=references() if _REFS else "")


# ---------------------------------------------------------------- render: print (PDF)
CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'IBM Plex Serif', Georgia, serif; font-size: 10.4pt; line-height: 1.55; color: #10213a; margin: 0; }
h1, h2, h3, .kpi .k, .cover, th, .cap, .callout b.t, .meta { font-family: 'IBM Plex Sans', system-ui, sans-serif; }
h2 { font-family: 'IBM Plex Sans Condensed', 'IBM Plex Sans', sans-serif; font-size: 17pt; font-weight: 700;
     color: #0b1630; margin: 18pt 0 6pt; break-after: avoid; letter-spacing: -0.01em; }
h3 { font-size: 11.5pt; font-weight: 600; color: #1f6fd1; margin: 12pt 0 3pt; break-after: avoid; }
p { margin: 0 0 7pt; } ul { margin: 0 0 8pt 0; padding-left: 15pt; } li { margin: 0 0 3pt; }
a { color: #1f6fd1; text-decoration: none; } code { font-family: 'IBM Plex Mono', monospace; font-size: 9pt; }
sup.ref { font-size: 7pt; line-height: 0; } sup.ref a { color: #1f6fd1; }
figure { margin: 8pt auto 12pt; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; border-radius: 4px; }
figure img.scr { border: 1px solid #dde4ec; }
.cap { font-size: 8.4pt; color: #5d6b75; text-align: left; margin-top: 4pt; line-height: 1.4; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0 12pt; font-family: 'IBM Plex Sans', sans-serif;
        font-size: 8.8pt; line-height: 1.4; break-inside: auto; }
table.small { font-size: 7.9pt; }
th { text-align: left; background: #0b1630; color: #fff; font-weight: 600; padding: 5pt 6pt; }
td { padding: 4.5pt 6pt; border-bottom: 1px solid #e3e9f0; vertical-align: top; }
tr:nth-child(even) td { background: #f6f9fc; }
tr { break-inside: avoid; }
table.keep { break-inside: avoid; }
h2 + table, h3 + table { break-before: avoid; }
.kpis { display: flex; gap: 8pt; margin: 8pt 0 12pt; break-inside: avoid; }
.kpi { flex: 1; background: #0b1630; color: #e8eef7; border-radius: 8px; padding: 10pt 10pt 9pt;
       border-top: 3px solid #6fe3ff; }
.kpi .k { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 19pt; color: #fff; line-height: 1.05; }
.kpi .l { font-family: 'IBM Plex Sans', sans-serif; font-size: 7.8pt; color: #b9c8dc; margin-top: 4pt; line-height: 1.35; }
.callout { border-left: 4px solid #3d8ef0; background: #eef5fe; padding: 8pt 11pt; margin: 8pt 0 12pt; border-radius: 0 6px 6px 0;
           break-inside: avoid; }
.callout.orange { border-color: #f0743a; background: #fff3ec; }
.callout b.t { display: block; font-size: 9.6pt; margin-bottom: 2pt; color: #0b1630; }
.callout p { margin: 0; font-size: 9.6pt; }
.pb { break-after: page; }
ol.refs { font-size: 8.2pt; line-height: 1.45; padding-left: 16pt; font-family: 'IBM Plex Sans', sans-serif; }
ol.refs li { margin-bottom: 4pt; } ol.refs a { word-break: break-all; }
.cover { height: 257mm; display: flex; flex-direction: column; justify-content: space-between; color: #e8eef7;
         background: radial-gradient(120% 70% at 70% 110%, #1d63b3 0%, #0b1630 45%, #070c17 100%);
         margin: -20mm -18mm 0; padding: 26mm 20mm 20mm; break-after: page; position: relative; overflow: hidden; }
.cover .brand { display: flex; align-items: center; gap: 12pt; }
.cover .brand img { width: 64pt; height: 64pt; border-radius: 12pt; object-fit: cover; }
.cover .brand span { font-size: 11pt; color: #9fe9ff; font-weight: 600; letter-spacing: .02em; }
.cover .kicker { font-family: 'IBM Plex Sans Condensed'; color: #6fe3ff; font-size: 13pt; font-weight: 600; margin-bottom: 8pt; }
.cover h1 { font-family: 'IBM Plex Sans Condensed'; font-size: 34pt; line-height: 1.02; margin: 0 0 12pt; color: #fff;
            letter-spacing: -0.02em; }
.cover .sub { font-size: 13.5pt; line-height: 1.45; color: #c9d6e8; max-width: 140mm; }
.cover .meta { font-size: 9.4pt; color: #b9c8dc; line-height: 1.6; }
.cover .meta a { color: #9fe9ff; }
.cover .arc { position: absolute; left: -10%; right: -10%; bottom: -160mm; height: 220mm; border-radius: 50%;
              box-shadow: 0 -2px 0 #6fe3ff, 0 -30px 80px rgba(111,227,255,.25); }
"""


def _img_src(b, mode):
    if mode == "docs":
        return f"{ASSET_URL}/{b['file'].replace('.png', '.jpg') if b['folder'] == 'screens' else b['file']}"
    return str((FIG if b["folder"] == "fig" else SCR) / b["file"])


def render(rep, mode="print"):
    out = []
    for b in rep["blocks"]:
        t = b["t"]
        if t == "h2":
            out.append(f"<h2>{html.escape(b['text'])}</h2>")
        elif t == "h3":
            out.append(f"<h3>{html.escape(b['text'])}</h3>")
        elif t == "p":
            out.append(f"<p>{b['html']}</p>")
        elif t == "ul":
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in b["items"]) + "</ul>")
        elif t == "pb":
            out.append('<div class="pb"></div>' if mode == "print" else "")
        elif t == "fig":
            src = _img_src(b, mode)
            if mode == "print":
                cls = ' class="scr"' if b["folder"] == "screens" else ""
                out.append(f'<figure style="width:{b["width"]}%"><img{cls} src="file://{src}"><div class="cap">'
                           f'{html.escape(b["caption"])}</div></figure>')
            else:
                w = int(6.3 * 96 * b["width"] / 100)
                out.append(f'<p style="text-align:center"><img src="{src}" width="{w}"></p>'
                           f'<p style="font-size:9pt;color:#5d6b75"><i>{html.escape(b["caption"])}</i></p>')
        elif t == "kpis":
            if mode == "print":
                out.append('<div class="kpis">' + "".join(
                    f'<div class="kpi"><div class="k">{html.escape(k)}</div><div class="l">{html.escape(l)}</div></div>'
                    for k, l in b["items"]) + "</div>")
            else:
                cells = "".join(f'<td style="background-color:#0b1630;padding:8pt;width:25%;vertical-align:top">'
                                f'<span style="color:#ffffff;font-size:18pt;font-weight:bold">{html.escape(k)}</span><br>'
                                f'<span style="color:#b9c8dc;font-size:8.5pt">{html.escape(l)}</span></td>'
                                for k, l in b["items"])
                out.append(f'<table style="border-collapse:collapse;width:100%"><tr>{cells}</tr></table><p></p>')
        elif t == "callout":
            if mode == "print":
                out.append(f'<div class="callout {b["tone"]}"><b class="t">{html.escape(b["title"])}</b><p>{b["body"]}</p></div>')
            else:
                bg = "#fff3ec" if b["tone"] == "orange" else "#eef5fe"
                out.append(f'<table style="border-collapse:collapse;width:100%"><tr><td style="background-color:{bg};'
                           f'padding:9pt;border-left:4pt solid {"#f0743a" if b["tone"] == "orange" else "#3d8ef0"}">'
                           f'<b>{html.escape(b["title"])}</b><br>{b["body"]}</td></tr></table><p></p>')
        elif t == "table":
            cls = ' class="small"' if b["small"] else ""
            cols = "".join(f'<col style="width:{w}%">' for w in b["widths"]) if b["widths"] else ""
            if mode == "print":
                if len(b["rows"]) <= 9:
                    cls = cls[:-1] + ' keep"' if cls else ' class="keep"'
                head = "".join(f"<th>{html.escape(h)}</th>" for h in b["head"])
                rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b["rows"])
                out.append(f"<table{cls}><colgroup>{cols}</colgroup><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>")
            else:
                head = "".join(f'<td style="background-color:#0b1630;color:#ffffff;padding:4pt;font-weight:bold">'
                               f'{html.escape(h)}</td>' for h in b["head"])
                rows = "".join("<tr>" + "".join(f'<td style="padding:4pt;border-bottom:1px solid #dde4ec">{c}</td>'
                                                for c in r) + "</tr>" for r in b["rows"])
                out.append(f'<table style="border-collapse:collapse;width:100%;font-size:9pt"><tr>{head}</tr>{rows}'
                           f'</table><p></p>')
    body = "\n".join(out) + (rep["refs"] or "")
    meta = (f'Team iGenfinity · NASA Space Apps Challenge 2026 · GDG Ahlen<br>15 November 2026<br>'
            f'App: <a href="{APP}">{APP}</a><br>Code and data: <a href="{REPO}">{REPO}</a>')
    if mode == "print":
        logo = f'<img src="file://{LOGO}">' if LOGO.exists() else ""
        cover = (f'<section class="cover"><div class="brand">{logo}<span>MonsoonLens · Team iGenfinity</span></div>'
                 f'<div><div class="kicker">MonsoonLens</div><h1>{html.escape(rep["title"])}</h1>'
                 f'<div class="sub">{html.escape(rep["subtitle"])}</div></div><div class="meta">{meta}</div>'
                 f'<div class="arc"></div></section>')
        return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MonsoonLens · {html.escape(rep["title"])}'
                f'</title><style>{CSS}</style></head><body>{cover}{body}</body></html>')
    logo = f'<p><img src="{ASSET_URL}/igenfinity_logo.jpg" width="120"></p>'
    return (f'<html><head><meta charset="utf-8"></head><body style="font-family:Arial">{logo}'
            f'<p style="color:#1f6fd1;font-size:12pt"><b>MonsoonLens</b></p>'
            f'<h1 style="font-size:26pt;color:#0b1630">{html.escape(rep["title"])}</h1>'
            f'<p style="font-size:13pt;color:#3c4b5c">{html.escape(rep["subtitle"])}</p><p style="font-size:9.5pt;color:#5d6b75">'
            f'{meta}</p><p style="font-size:9pt;color:#5d6b75"><i>A typeset PDF of this document is in the code repository.'
            f'</i></p><hr>{body}</body></html>')


async def to_pdf(html_text, path):
    from playwright.async_api import async_playwright
    tmp = OUT / (path.stem + ".html")
    tmp.write_text(html_text, encoding="utf-8")
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        await pg.goto(f"file://{tmp}", wait_until="networkidle")
        await pg.wait_for_timeout(800)
        foot = ('<div style="font-family:IBM Plex Sans,sans-serif;font-size:7.5pt;color:#8a9bb0;width:100%;'
                'padding:0 18mm;display:flex;justify-content:space-between"><span>MonsoonLens · Team iGenfinity · '
                f'{html.escape(path.stem.split("_", 1)[1].replace("_", " ").title())}</span>'
                '<span class="pageNumber"></span></div>')
        await pg.pdf(path=str(path), format="A4", print_background=True, display_header_footer=True,
                     header_template="<div></div>", footer_template=foot,
                     margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"})
        await b.close()
    print(path)


REPORTS = {"MonsoonLens_Business_Plan": business_plan, "MonsoonLens_Technical_Report": technical,
           "MonsoonLens_Field_Guide": field_guide}

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in REPORTS.items():
        if only and name not in only:
            continue
        rep = fn()
        asyncio.run(to_pdf(render(rep, "print"), OUT / f"{name}.pdf"))
        rep = fn()
        (OUT / f"{name}_docs.html").write_text(render(rep, "docs"), encoding="utf-8")
