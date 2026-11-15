"""Field check list: every likely slide zone, ranked, with its evidence, for district teams."""
import html

import pandas as pd
import streamlit as st

from lib import data, evidence as ev, ui

ui.setup("Field check list")
ui.demo_banner()
if not ui.require_results():
    st.stop()
tr = ui.tr
before, after = data.dates()

ui.page_header(tr('Field check list', 'क्षेत्रीय तपासणी यादी'), tr(
    "Every likely slide zone from {b} to {a}, ranked, with its radar images. Print it or open it on a phone, then go "
    "and check: these are leads, not confirmed landslides.",
    "{b} ते {a} मधील प्रत्येक संभाव्य भूस्खलन क्षेत्र, क्रमवार, रडार प्रतिमांसह. छापा किंवा फोनवर उघडा आणि जाऊन तपासा: "
    "हे संकेत आहेत, निश्चित भूस्खलने नाहीत.", b=ui.day(before), a=ui.date(after)), tr("District disaster teams", "जिल्हा आपत्ती पथके"))

files = data.field_files()
names = {"html": tr("Printable list with radar images", "रडार प्रतिमांसह छापण्याजोगी यादी"),
         "kml": tr("KML for Google Earth and phone maps", "गूगल अर्थ आणि फोन नकाशांसाठी KML"),
         "csv": tr("Spreadsheet (CSV)", "स्प्रेडशीट (CSV)"), "geojson": "GeoJSON (GIS)",
         "nearby": tr("What is nearby (CSV)", "जवळ काय आहे (CSV)")}
save_as = {"nearby": "monsoonlens_nearby.csv"}
if files:
    btns = "".join(
        f'<a class="ml-dl{" primary" if k == "html" else ""}" href="{u}" '
        f'{"target=_blank" if k == "html" else "download=" + save_as.get(k, f"monsoonlens_field_list.{k}")}>'
        f'{html.escape(names[k])}<small>{max(sz // 1000, 1)} KB</small></a>'
        for k, (u, sz) in files.items())
    st.markdown(f'<div class="ml-dlrow">{btns}</div>', unsafe_allow_html=True)

zones = sorted(data.zones(), key=lambda p: (-p["score"], p["id"]))
if not zones:
    st.info(tr("No slide zones in this run.", "या निकालात भूस्खलन क्षेत्रे नाहीत."))
    st.stop()

nb = data.nearby()
nbz = nb.get("zones", {})


def _first(z, key, name):
    """Nearest road or settlement within range, as 'name, distance'; empty when there is none that close."""
    return f"{name(z[key][0])}, {ev.dist(z[key][0]['distance_m'])}" if z and z[key] else ""


rows = []
for rank, p in enumerate(zones, start=1):
    rows.append({"rank": rank, "id": p["id"], "near": p.get("near") or "", "confidence": p["confidence"],
                 "road": _first(nbz.get(p["id"]), "roads", ev._line_name),
                 "place": _first(nbz.get(p["id"]), "places", ev._place_name),
                 "conf_txt": {"high": tr("High", "उच्च"), "medium": tr("Medium", "मध्यम"),
                              "low": tr("Low", "कमी")}.get(p["confidence"], p["confidence"]),
                 "score": p["score"], "orbit": {"confirmed": tr("found again", "पुन्हा सापडले"),
                                                "partial": tr("partly", "अंशतः"),
                                                "not seen": tr("not seen", "दिसले नाही"),
                                                "not covered": tr("outside view", "दृष्टीबाहेर")}.get(p.get("track106"), ""),
                 "dem": tr("kept", "टिकले") if p.get("nasadem") == "found" else tr("not kept", "टिकले नाही"),
                 "report": (f'{p["nearest_event_km"]:.1f} km' if p.get("nearest_event_km") is not None else ""),
                 "slope": p["slope_deg"], "map": ev.maps_link(p["lat"], p["lon"])})
df = pd.DataFrame(rows)

c1, c2, c3 = st.columns([1.3, 1.2, 1.5])
conf = c1.segmented_control(tr("Confidence", "खात्री"), ["high", "medium", "low"], selection_mode="multi",
                            default=["high", "medium", "low"],
                            format_func=lambda c: {"high": tr("High", "उच्च"), "medium": tr("Medium", "मध्यम"),
                                                   "low": tr("Low", "कमी")}[c], key="field_conf")
extra = c2.toggle(tr("Only zones an extra check backs", "फक्त अतिरिक्त तपासणीने पुष्टी झालेली"), value=False,
                  help=tr("Found again by the second NISAR orbit, kept with NASADEM, or a reported event within 2 km.",
                          "दुसऱ्या निसार कक्षेत पुन्हा सापडलेली, NASADEM सह टिकलेली, किंवा २ किमीच्या आत नोंदवलेली घटना."))
q = c3.text_input(tr("Near a place", "ठिकाणाजवळ"), placeholder=tr("e.g. Mulshi", "उदा. मुळशी"))
sel = df[df["confidence"].isin(conf or [])]
if extra:
    keep = {p["id"] for p in zones if p.get("checks_passed", 0) > 0}
    sel = sel[sel["id"].isin(keep)]
if q.strip():
    sel = sel[sel["near"].str.contains(q.strip(), case=False, regex=False)]

if nbz:
    s = nb["summary"]
    st.markdown(tr(
        "**What is nearby.** Of the {t} zones, {r} have a mapped road within {rk} km, {w} a railway line within "
        "{rk} km and {p} a village, town or suburb within {pk} km; {x} have none of these that close. Distances are "
        "straight lines from the edge of the zone. Near does not mean at risk: it tells whoever looks after that "
        "road, line or village which leads concern them.",
        "**जवळ काय आहे.** {t} क्षेत्रांपैकी {r} क्षेत्रांच्या {rk} किमीच्या आत नकाशातील रस्ता आहे, {w} च्या {rk} किमीच्या "
        "आत रेल्वे मार्ग आणि {p} च्या {pk} किमीच्या आत गाव, शहर किंवा उपनगर आहे; {x} क्षेत्रांजवळ यांपैकी काहीही इतक्या "
        "जवळ नाही. अंतरे क्षेत्राच्या कडेपासून सरळ रेषेत मोजली आहेत. जवळ असणे म्हणजे धोका असणे नव्हे: तो रस्ता, मार्ग "
        "किंवा गाव सांभाळणाऱ्यांना कोणते संकेत त्यांच्याशी संबंधित आहेत हे यावरून कळते.",
        t=s["zones"], r=s["road_within"], w=s["railway_within"], p=s["place_within"], x=s["nothing_within"],
        rk=f"{nb['road_m'] / 1000:g}", pk=f"{nb['place_m'] / 1000:g}"))
st.markdown(tr("{n} of {t} zones. Select a row to see its radar evidence.",
               "{t} पैकी {n} क्षेत्रे. रडार पुरावा पाहण्यासाठी एक ओळ निवडा.", n=len(sel), t=len(df)))
cc = st.column_config
evt = st.dataframe(
    sel, hide_index=True, width="stretch", height=min(420, 38 + 35 * max(len(sel), 1)), on_select="rerun",
    selection_mode="single-row", key="field_table",
    column_order=["rank", "id", "near", "conf_txt", "score", "orbit", "dem", "report"]
    + (["road", "place"] if nbz else []) + ["slope", "map"],
    column_config={"rank": cc.NumberColumn("#", width="small"), "id": tr("Zone", "क्षेत्र"),
                   "near": tr("Nearest place", "जवळचे ठिकाण"), "conf_txt": tr("Confidence", "खात्री"),
                   "score": cc.ProgressColumn(tr("Score", "गुण"), min_value=0, max_value=1, format="%.2f"),
                   "orbit": cc.TextColumn(tr("2nd orbit", "दुसरी कक्षा"),
                                          help=tr("NISAR track 106, 3 to 15 July", "निसार मार्ग १०६, ३ ते १५ जुलै")),
                   "dem": cc.TextColumn("NASADEM", help=tr("Slide rule re-run with NASA's NASADEM elevation map",
                                                           "नासाच्या NASADEM उंची नकाशासह पुन्हा तपासणी")),
                   "report": cc.TextColumn(tr("Nearest report", "जवळची नोंद"),
                                           help=tr("Distance to the nearest reported flood or landslide",
                                                   "सर्वात जवळच्या नोंदवलेल्या पूर किंवा भूस्खलनाचे अंतर")),
                   "road": cc.TextColumn(tr("Road nearby", "जवळचा रस्ता"),
                                         help=tr("Nearest mapped road within {km} km of the zone's edge (OpenStreetMap)",
                                                 "क्षेत्राच्या कडेपासून {km} किमीच्या आत सर्वात जवळचा नकाशातील रस्ता "
                                                 "(OpenStreetMap)", km=f"{nb.get('road_m', 0) / 1000:g}")),
                   "place": cc.TextColumn(tr("Settlement nearby", "जवळची वस्ती"),
                                          help=tr("Nearest village, town or suburb within {km} km of the zone's edge "
                                                  "(OpenStreetMap)",
                                                  "क्षेत्राच्या कडेपासून {km} किमीच्या आत सर्वात जवळचे गाव, शहर किंवा "
                                                  "उपनगर (OpenStreetMap)", km=f"{nb.get('place_m', 0) / 1000:g}")),
                   "slope": cc.NumberColumn(tr("Slope (°)", "उतार (°)"), format="%.0f"),
                   "map": cc.LinkColumn(tr("Map", "नकाशा"), display_text=tr("Open", "उघडा"))})
rows_sel = (evt.selection.rows if evt and hasattr(evt, "selection") else []) or []
pick = sel.iloc[rows_sel[0]]["id"] if rows_sel and len(sel) else (sel.iloc[0]["id"] if len(sel) else None)
if pick:
    p = next(z for z in zones if z["id"] == pick)
    st.markdown(f"### {tr('Evidence for', 'पुरावा:')} {pick}")
    ev.show_zone(p)

np_ = data.next_pass()
if np_:
    st.markdown(f'<div class="ml-pass"><span>🛰️</span><span>' + tr(
        "This list comes from one pair of NISAR passes. NISAR returns every 12 days: the last pass in our data is "
        "<b>{l}</b>, and if it keeps its repeat the next is <b>{n}</b>. The same code rebuilds the list from each "
        "new pass.",
        "ही यादी निसारच्या एका जोडी निरीक्षणांवरून बनली आहे. निसार दर १२ दिवसांनी परत येतो: आमच्या डेटातील शेवटचे "
        "निरीक्षण <b>{l}</b>, आणि चक्र कायम राहिल्यास पुढचे <b>{n}</b>. तोच कोड प्रत्येक नव्या निरीक्षणावरून यादी "
        "पुन्हा तयार करतो.", l=ui.date(np_[0]), n=ui.date(np_[1])) + "</span></div>", unsafe_allow_html=True)
st.markdown('<p class="ml-source">' + tr(
    "Nearest place names © OpenStreetMap contributors (Nominatim). Score: steepness, radar change and coherence loss, "
    "each up to a third.", "जवळच्या ठिकाणांची नावे © OpenStreetMap योगदानकर्ते. गुण: उतार, रडार बदल आणि कोहेरन्समधील घट, "
    "प्रत्येकी एक तृतीयांशपर्यंत.") + (" " + tr(
        "Roads, railway lines and settlements © OpenStreetMap contributors (expressways down to tertiary roads; "
        "smaller roads, tracks and hamlets are not counted).",
        "रस्ते, रेल्वे मार्ग आणि वस्त्या © OpenStreetMap योगदानकर्ते (द्रुतगती मार्गांपासून तृतीय श्रेणीच्या रस्त्यांपर्यंत; "
        "लहान रस्ते, पायवाटा आणि वाड्या मोजलेल्या नाहीत).") if nbz else "") + "</p>", unsafe_allow_html=True)
ui.sources_line()
