import html

import pandas as pd
import streamlit as st

from lib import checks, data, explain, ui

ui.setup("Method and limits")
ui.demo_banner()
if not ui.require_results():
    st.stop()
tr = ui.tr

m = data.metrics()
th = m.get("thresholds", {})
before, after = data.dates()
val_s = m.get("validation", {})
srcs = m.get("sources", [])
fh, fo = val_s.get("flood", {}).get("hits", 0), val_s.get("flood", {}).get("observable", 0)
sh_, so_ = val_s.get("slide", {}).get("hits", 0), val_s.get("slide", {}).get("observable", 0)


def pct(x, d=0):
    return f"{x * 100:.{d}f}%"


ui.page_header(tr("Method and limits", "पद्धत आणि मर्यादा"), tr(
    "Every number in this app comes from the pipeline in our public repository, run on the NISAR files listed below. "
    "Nothing is estimated by hand, and every check is reported, including the ones that came out weak.",
    "या ॲपमधील प्रत्येक आकडा आमच्या सार्वजनिक रिपॉझिटरीतील पाइपलाइनमधून येतो, खाली दिलेल्या निसार फाइल्सवर चालवलेला. "
    "काहीही हाताने अंदाजलेले नाही, आणि प्रत्येक तपासणी नोंदवली आहे, कमकुवत ठरलेल्याही."),
    tr("Researchers and journalists", "संशोधक आणि पत्रकार"))
SECTIONS = [("nisar-in-brief", tr("NISAR in brief", "निसार थोडक्यात")),
            ("how-radar-sees-through-cloud", tr("How radar sees", "रडार कसे पाहते")),
            ("how-it-works", tr("How it works", "हे कसे काम करते")),
            ("how-we-checked-it", tr("How we checked it", "आम्ही कसे तपासले")),
            ("data", tr("Data", "डेटा")), ("limits", tr("Limits", "मर्यादा")),
            ("reproduce-it", tr("Reproduce it", "पुन्हा तयार करा")), ("team", tr("Team", "टीम"))]
st.markdown(f'<nav class="ml-toc" aria-label="{html.escape(tr("On this page", "या पानावर"))}">' + "".join(
    f'<a href="#{a}">{html.escape(t)}</a>' for a, t in SECTIONS) + "</nav>", unsafe_allow_html=True)
H = dict(SECTIONS)


def section(anchor, title=None):
    st.header(title or H[anchor], anchor=anchor)


# ---------------------------------------------------------------- the satellite
section("nisar-in-brief")
tracks = sorted({s["granule_id"].split("_")[5] for s in srcs if s["granule_id"].count("_") > 5})
utc = sorted({s["granule_id"].split("_A_")[-1][9:13] for s in srcs if "_A_" in s["granule_id"]})
utc_txt = tr(" and ", " आणि ").join(f"{u[:2]}:{u[2:]}" for u in utc)
facts = [
    (tr("Launched", "प्रक्षेपण"), tr("30 July 2025 on ISRO's GSLV-F16, from Sriharikota, India",
                                     "३० जुलै २०२५, इस्रोच्या GSLV-F16 वरून, श्रीहरिकोटा, भारत")),
    (tr("Orbit", "कक्षा"), tr("Sun-synchronous, about 747 km up, inclined 98.4°",
                              "सूर्य-समकालिक, सुमारे ७४७ किमी उंचीवर, ९८.४° कलती")),
    (tr("Repeat", "पुनरावृत्ती"), tr("The same ground track every 12 days", "दर १२ दिवसांनी तोच जमिनीवरील मार्ग")),
    (tr("Radars", "रडार"), tr("L-band (NASA/JPL, 24 cm wavelength) and S-band (ISRO), sharing one 12 m mesh reflector",
                              "L-बँड (नासा/JPL, २४ सेमी तरंगलांबी) आणि S-बँड (इस्रो), एकच १२ मीटर जाळीदार परावर्तक")),
    (tr("Swath", "पट्टा"), tr("242 km wide on the ground", "जमिनीवर २४२ किमी रुंद")),
    (tr("What this app uses", "हे ॲप काय वापरते"),
     tr("L-band, tracks {t}, southbound evening passes ({u} UTC), level-2 GCOV and GUNW products",
        "L-बँड, मार्ग {t}, दक्षिणेकडे जाणारी संध्याकाळची निरीक्षणे ({u} UTC), लेव्हल-२ GCOV आणि GUNW उत्पादने",
        t=tr(" and ", " आणि ").join(t.lstrip("0") for t in tracks), u=utc_txt)),
]
st.markdown('<dl class="ml-facts-card">' + "".join(
    f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in facts) + "</dl>",
    unsafe_allow_html=True)
st.caption(tr("Mission facts: [ISRO, NISAR launch page](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) and "
              "[eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar). Tracks and times: the NISAR file "
              "names in the Data table.",
              "मोहिमेची माहिती: [इस्रो, निसार प्रक्षेपण पान](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) आणि "
              "[eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar). मार्ग आणि वेळा: डेटा तक्त्यातील "
              "निसार फाइल्सची नावे."))

section("how-radar-sees-through-cloud", tr("How radar sees through cloud", "रडार ढगांपलीकडे कसे पाहते"))
st.markdown(f'<div style="width:100%;max-width:1000px">{explain.svg()}</div>', unsafe_allow_html=True)
st.caption(tr("NISAR's L-band radar has a wavelength of about 24 cm: it passes through cloud and rain, and partly "
              "through forest canopy. It sends two polarisations: HH (horizontal out, horizontal back) responds to "
              "surfaces and structures, HV (horizontal out, vertical back) mostly to vegetation.",
              "निसारच्या L-बँड रडारची तरंगलांबी सुमारे २४ सेमी आहे: ते ढग आणि पावसातून, आणि काही प्रमाणात जंगलाच्या "
              "छतातूनही जाते. ते दोन ध्रुवीकरणे पाठवते: HH (आडवे जाते, आडवे परत) पृष्ठभाग आणि बांधकामांना प्रतिसाद "
              "देते, HV (आडवे जाते, उभे परत) मुख्यतः वनस्पतींना."))

# ---------------------------------------------------------------- the pipeline
section("how-it-works")
wb = th.get("water_db_bounds", ["?", "?"])
n_rep = len(data.events().get("features", [])) if data.events() else 0
STEPS = [
    (tr("Read the radar", "रडार वाचा"), [
        (tr("Cut the radar to Pune", "रडार पुण्यापुरते कापा"),
         tr("NISAR's level-2 GCOV files hold radar brightness (gamma-nought, already corrected for terrain) on a map "
            "grid. A full frame is about 5 GB per layer, so we stream only the study box (lon {w} to {e}, lat {s} to "
            "{n}) and average 2 × 2 or more native pixels into a {r} m grid. Averaging reduces radar speckle; a Lee "
            "filter removes more.",
            "निसारच्या लेव्हल-२ GCOV फाइल्समध्ये नकाशा-ग्रिडवर रडारची चमक (गॅमा-नॉट, भूरचनेसाठी आधीच दुरुस्त) असते. "
            "एक पूर्ण फ्रेम प्रति स्तर सुमारे ५ GB असते, म्हणून आम्ही फक्त अभ्यास क्षेत्र (रेखांश {w} ते {e}, अक्षांश {s} "
            "ते {n}) प्रवाहित करतो आणि २ × २ किंवा अधिक मूळ चौकोनांची सरासरी काढून {r} मीटरचा ग्रिड बनवतो. सरासरीमुळे "
            "रडारचा ठिपकेपणा कमी होतो; ली फिल्टर आणखी कमी करतो.",
            w=m["aoi"]["west"], e=m["aoi"]["east"], s=m["aoi"]["south"], n=m["aoi"]["north"],
            r=f"{m['grid']['res_m']:.0f}"),
         [tr("{r} m grid", "{r} मीटर ग्रिड", r=f"{m['grid']['res_m']:.0f}"), "UTM 43N", tr("Lee filter", "ली फिल्टर")]),
        (tr("Find water on each date", "प्रत्येक तारखेला पाणी शोधा"),
         tr("Smooth water reflects the radar away and looks dark in HH. The cut-off between water and land is set "
            "separately for each date with the minimum-error method of Kittler and Illingworth, trained on reservoir "
            "and river cores that the JRC Global Surface Water record says are water at least {o}% of the time, plus "
            "an equal number of land pixels. In these NISAR products open water sits near −16 dB and dry land near "
            "−5 dB.",
            "गुळगुळीत पाणी रडार दूर परावर्तित करते आणि HH मध्ये गडद दिसते. पाणी आणि जमीन यांतील सीमा प्रत्येक तारखेसाठी "
            "वेगळी ठरवली जाते, किटलर आणि इलिंगवर्थ यांच्या किमान-त्रुटी पद्धतीने, धरणे आणि नद्यांच्या अशा मध्यभागांवर "
            "प्रशिक्षित जे JRC जागतिक पृष्ठजल नोंदीनुसार किमान {o}% वेळ पाणी असतात, तितक्याच जमिनीच्या चौकोनांसह. या "
            "निसार उत्पादनांमध्ये खुले पाणी सुमारे −१६ dB आणि कोरडी जमीन सुमारे −५ dB वर असते.",
            o=th.get("water_train_occurrence", 90)),
         [tr("threshold kept within {a} to {b} dB", "मर्यादा {a} ते {b} dB मध्ये", a=wb[0], b=wb[1]),
          tr("one threshold per date", "प्रत्येक तारखेला एक मर्यादा")]),
    ]),
    (tr("Find the change", "बदल शोधा"), [
        (tr("Keep only new water", "फक्त नवीन पाणी ठेवा"),
         tr("A pixel is new water if it is water on {a} but not on {b}, clearly darker, outside permanent water, on "
            "flat ground, and part of a patch big enough not to be speckle.",
            "एखादा चौकोन नवीन पाणी तेव्हा, जेव्हा तो {a} ला पाणी आहे पण {b} ला नाही, स्पष्टपणे गडद आहे, कायमच्या "
            "पाण्याबाहेर आहे, सपाट जमिनीवर आहे, आणि ठिपक्यापेक्षा मोठ्या पुरेशा भागाचा भाग आहे.",
            a=ui.date(after), b=ui.date(before)),
         [tr("≥ {d} dB darker", "≥ {d} dB गडद", d=th.get("change_db")),
          tr("JRC occurrence < {o}%", "JRC आढळ < {o}%", o=th.get("permanent_water_occurrence")),
          tr("slope < {s}°", "उतार < {s}°", s=th.get("flood_max_slope_deg")),
          tr("≥ {p} pixels", "≥ {p} चौकोन", p=th.get("min_patch_pixels"))]),
        (tr("Flag possible hidden water", "लपलेल्या संभाव्य पाण्याची खूण करा"),
         tr("At L-band, water under trees or between buildings makes the radar bounce twice and come back brighter. "
            "Flat ground that got brighter is shown as possible water, and never added to flood totals.",
            "L-बँडवर, झाडांखालील किंवा इमारतींमधील पाण्यामुळे रडार दोनदा परावर्तित होऊन अधिक उजळ परत येते. उजळ झालेली "
            "सपाट जमीन संभाव्य पाणी म्हणून दाखवली जाते, आणि पुराच्या एकूण आकड्यात कधीही जोडली जात नाही."),
         [tr("≥ {d} dB brighter", "≥ {d} dB उजळ", d=th.get("change_db")),
          tr("shown hatched, never counted", "रेषांनी दाखवले, कधी मोजले नाही")]),
        (tr("Find likely slide zones", "संभाव्य भूस्खलन क्षेत्रे शोधा"),
         tr("Outside the radar's layover and shadow, a zone needs all three: the ground stopped matching itself "
            "between passes (coherence, from the NISAR GUNW product); it lost much more coherence than its own 1 km "
            "neighbourhood, because monsoon vegetation lowers coherence everywhere; and the radar brightness jumped, "
            "from rough debris (HH up) or stripped vegetation (HV down), measured against the scene's own median "
            "change on dry land. Each zone gets a 0 to 1 score from slope, radar change and coherence loss.",
            "रडारच्या ले-ओव्हर आणि सावलीबाहेर, एका क्षेत्राला तिन्ही हवे: दोन निरीक्षणांदरम्यान जमीन स्वतःशी जुळेनाशी झाली "
            "(कोहेरन्स, निसार GUNW उत्पादनातून); तिने आपल्या स्वतःच्या १ किमी परिसरापेक्षा खूप जास्त कोहेरन्स गमावला, "
            "कारण पावसाळ्यातील वनस्पती सगळीकडे कोहेरन्स कमी करतात; आणि रडारची चमक उसळली, खडबडीत ढिगाऱ्यामुळे (HH वर) "
            "किंवा निघून गेलेल्या वनस्पतींमुळे (HV खाली), कोरड्या जमिनीवरील दृश्याच्या स्वतःच्या मध्यम बदलाशी तुलना करून. "
            "प्रत्येक क्षेत्राला उतार, रडार बदल आणि कोहेरन्समधील घट यांवरून ० ते १ गुण मिळतात."),
         [tr("slope {a}° to {b}°", "उतार {a}° ते {b}°", a=th.get("slide_min_slope_deg"), b=th.get("slide_max_slope_deg", 45)),
          tr("coherence < {c}", "कोहेरन्स < {c}", c=th.get("coherence_low")),
          tr("< 0.6 × its 1 km surroundings", "< आपल्या १ किमी परिसराच्या ०.६ पट"),
          f"HH +{th.get('slide_hh_rise_db', 3)} dB / HV −{th.get('slide_hv_drop_db', 2)} dB"]),
    ]),
    (tr("Check it", "तपासा"), [
        (tr("Check against reports", "नोंदींशी तुलना करा"),
         tr("Reported floods and landslides, from the news and official sources, each linked, are matched to "
            "detections nearby, or within the report's own location precision if that is larger.",
            "बातम्या आणि अधिकृत स्रोतांमधून नोंदवलेले पूर आणि भूस्खलने, प्रत्येकाचा दुवा दिलेला, जवळच्या शोधांशी जुळवले "
            "जातात, किंवा नोंदीच्या स्वतःच्या स्थान-अचूकतेच्या आत, जर ती मोठी असेल तर."),
         [tr("floods: 500 m", "पूर: ५०० मी"), tr("slides: 750 m", "भूस्खलने: ७५० मी"),
          tr("{n} reports", "{n} नोंदी", n=n_rep)]),
        (tr("Check with a second track", "दुसऱ्या मार्गाने तपासा"),
         tr("The same slide rule runs on an independent NISAR pair from another orbit, which also spans the rain "
            "peak. A real slope failure changes the ground for good, so it should show in both; speckle or a "
            "geometry artefact of one orbit usually does not. Chance level comes from moving every zone to random "
            "steep, dry places and repeating the test.",
            "तोच भूस्खलन नियम दुसऱ्या कक्षेतील एका स्वतंत्र निसार जोडीवर चालतो, जी पावसाच्या शिखरालाही व्यापते. खरी "
            "उतार-घसरण जमीन कायमची बदलते, म्हणून ती दोन्हींत दिसायला हवी; एका कक्षेतील ठिपकेपणा किंवा भूमितीतील दोष "
            "सहसा दिसत नाही. योगायोगाची पातळी प्रत्येक क्षेत्र यादृच्छिक तीव्र, कोरड्या ठिकाणी हलवून आणि चाचणी पुन्हा "
            "करून मिळते."),
         [tr("track 106", "मार्ग १०६"), tr("3 to 15 July", "३ ते १५ जुलै"),
          tr("random-placement baseline", "यादृच्छिक मांडणीचा आधार")]),
        (tr("Check with a second elevation map", "दुसऱ्या उंची नकाशाने तपासा"),
         tr("Slope and slope direction come from the Copernicus GLO-30 elevation map. We run the same slide rule "
            "again with NASA's NASADEM elevation map and record which zones it keeps.",
            "उतार आणि उताराची दिशा कोपर्निकस GLO-30 उंची नकाशावरून येतात. आम्ही तोच भूस्खलन नियम नासाच्या NASADEM "
            "उंची नकाशासह पुन्हा चालवतो आणि तो कोणती क्षेत्रे ठेवतो ते नोंदवतो."),
         ["Copernicus GLO-30", "NASA NASADEM"]),
        (tr("Test the water threshold", "पाण्याची मर्यादा तपासा"),
         tr("Both dates' water thresholds are moved 1 dB down and up and the water numbers are recomputed, to show "
            "how much they depend on that one choice.",
            "दोन्ही तारखांच्या पाण्याच्या मर्यादा १ dB खाली आणि वर हलवल्या जातात आणि पाण्याचे आकडे पुन्हा मोजले जातात, "
            "ते त्या एका निवडीवर किती अवलंबून आहेत हे दाखवण्यासाठी."),
         ["−1, 0, +1 dB"]),
    ]),
    (tr("Hand it over", "सुपूर्द करा"), [
        (tr("Package the evidence", "पुरावा एकत्र बांधा"),
         tr("For every slide zone and flood patch the pipeline cuts small image chips of that spot from the NISAR "
            "data (radar colour before and after, and coherence), notes the nearest reported event, and writes the "
            "field check list as a printable page, KML, CSV and GeoJSON.",
            "प्रत्येक भूस्खलन क्षेत्र आणि पुराच्या भागासाठी पाइपलाइन निसार डेटामधून त्या जागेच्या लहान प्रतिमा कापते "
            "(आधीचा आणि नंतरचा रडार रंग, आणि कोहेरन्स), सर्वात जवळची नोंदवलेली घटना नोंदवते, आणि क्षेत्रीय तपासणी यादी "
            "छापण्याजोगे पान, KML, CSV आणि GeoJSON म्हणून लिहिते."),
         [tr("1.9 km image chips", "१.९ किमी प्रतिमा"), "HTML", "KML", "CSV", "GeoJSON"]),
    ]),
]
k = 0
for phase, steps in STEPS:
    st.markdown(f'<p class="ml-phase">{html.escape(phase)}</p>', unsafe_allow_html=True)
    items = []
    for title, desc, chips in steps:
        k += 1
        items.append(f'<li><span class="n">{k}</span><p class="t">{html.escape(title)}</p>'
                     f'<p class="d">{html.escape(desc)}</p><div class="ml-chips2">'
                     + "".join(f"<span>{html.escape(str(c))}</span>" for c in chips) + "</div></li>")
    st.markdown(f'<ol class="ml-steps" start="{k - len(steps) + 1}">{"".join(items)}</ol>', unsafe_allow_html=True)

# ---------------------------------------------------------------- the checks
section("how-we-checked-it")
checks.render()
xt, dc, sens = data.crosstrack(), m.get("dem_check"), m.get("sensitivity")
tabs = st.tabs([tr("Reported events", "नोंदवलेल्या घटना"), tr("Second NISAR orbit", "दुसरी निसार कक्षा"),
                tr("Second elevation map", "दुसरा उंची नकाशा"), tr("Water threshold", "पाण्याची मर्यादा"),
                tr("Results table", "निकाल तक्ता")])


def short(text):
    st.markdown(f'<p class="ml-short"><b>{html.escape(tr("In short:", "थोडक्यात:"))}</b> {text}</p>',
                unsafe_allow_html=True)


YESNO = {True: tr("yes", "हो"), False: tr("no", "नाही")}
with tabs[0]:
    _fb = data.flood_baseline()
    short(tr("radar found something near {h} of {o} reported floods it could see", "रडारला दिसू शकणाऱ्या {o} पैकी {h} "
             "नोंदवलेल्या पुरांजवळ काहीतरी सापडले", h=fh, o=fo)
          + (tr(", but places nobody reported score {e}: no better than chance",
                ", पण कोणीही न नोंदवलेली ठिकाणे {e} गुण मिळवतात: योगायोगापेक्षा चांगले नाही",
                e=f"{_fb['flat']['expected_matches']:.1f}") if _fb else "")
          + tr(". Landslides: {h} of {o}.", ". भूस्खलने: {o} पैकी {h}.", h=sh_, o=so_))
    val = data.table("validation.csv")
    if val is not None and len(val):
        st.markdown(tr("Floods: **{fh} of {fo}** reports that radar could observe had a detection nearby. Landslides: "
                       "**{sh} of {so}**. Counts, not an accuracy: the samples are small.",
                       "पूर: रडारला दिसू शकणाऱ्या **{fo} पैकी {fh}** नोंदींजवळ शोध लागला. भूस्खलने: **{so} पैकी {sh}**. "
                       "ही गणना आहे, अचूकता नव्हे: नमुने लहान आहेत.", fh=fh, fo=fo, sh=sh_, so=so_))
        fb = data.flood_baseline()
        if fb:
            n, k = fb["of"], fb["matched"]
            lo, hi = fb["new_water_km"]
            better = fb["flat"]["prob_at_least_observed"] < 0.05 and fb["settlements"]["prob_at_least_observed"] < 0.05
            st.markdown("#### " + tr("Are the flood matches better than chance?", "पुराच्या जुळण्या योगायोगापेक्षा चांगल्या आहेत का?"))
            st.markdown(
                (tr("**Yes.**", "**हो.**") if better else tr("**No.**", "**नाही.**")) + " "
                + tr("With the reports as they stand now, **{k} of {n}** reported floods have a detection within their "
                     "tolerance. The same rule applied to places nobody reported gives **{a} of {n}** on random flat "
                     "ground and **{b} of {n}** at a random village, town or suburb.",
                     "सध्याच्या नोंदींनुसार **{n} पैकी {k}** नोंदवलेल्या पुरांच्या सहनसीमेत शोध आहे. कोणीही न नोंदवलेल्या "
                     "ठिकाणी तोच नियम लावल्यास यादृच्छिक सपाट जमिनीवर **{n} पैकी {a}** आणि यादृच्छिक गाव, शहर किंवा "
                     "उपनगरात **{n} पैकी {b}** मिळते.",
                     k=k, n=n, a=f"{fb['flat']['expected_matches']:.1f}", b=f"{fb['settlements']['expected_matches']:.1f}")
                + ("" if better else " " + tr(
                    "So the flood count is what chance alone would give: it is not evidence that the map finds reported "
                    "floods.", "म्हणून पुराची गणना केवळ योगायोगाने मिळेल इतकीच आहे: नकाशा नोंदवलेले पूर शोधतो याचा तो पुरावा नाही."))
                + (" " + tr("All {k} matches are to \"possible water under cover\" patches, which we show but never count "
                            "as flood;", "सर्व {k} जुळण्या \"झाकलेले संभाव्य पाणी\" भागांशी आहेत, जे आम्ही दाखवतो पण पूर "
                            "म्हणून कधी मोजत नाही;", k=k)
                   if k and not fb["observed"]["matched_to_new_water"] else "")
                + " " + tr("the nearest mapped new open water is {lo} to {hi} km from every reported flood.",
                           "प्रत्येक नोंदवलेल्या पुरापासून सर्वात जवळचे नकाशातील नवीन खुले पाणी {lo} ते {hi} किमी दूर आहे.",
                           lo=f"{lo:.0f}", hi=f"{hi:.0f}"))
            if not fb["in_step"]:
                v = fb["validation_csv"]
                st.markdown(tr("The count above differs from the {h} of {o} in the headline and the table below: a "
                               "report's location was corrected after the last full pipeline run. The two will agree "
                               "after the next run.",
                               "वरील गणना शीर्षकातील आणि खालील तक्त्यातील {o} पैकी {h} पेक्षा वेगळी आहे: शेवटच्या पूर्ण "
                               "पाइपलाइन रननंतर एका नोंदीचे स्थान दुरुस्त केले गेले. पुढच्या रननंतर दोन्ही जुळतील.",
                               h=v["hits"], o=v["of"]))
            from lib import charts
            st.plotly_chart(charts.flood_chance(fb), width="stretch", config={"displayModeBar": False})
            st.markdown(tr(
                "How the chance level is worked out: a report counts as matched when new water or a possible-water "
                "patch lies within its tolerance (the larger of the report's location precision and 500 m). For each "
                "report we take the share of a reference set that has a detection within that same tolerance, and add "
                "the shares up. Flat ground: every 40 m pixel with radar data on both dates, outside permanent water, "
                "slope ≤ 5° ({km} km²). Settlements: {p} OpenStreetMap villages, towns and suburbs with radar data. "
                "Getting {k} or more by chance has a probability of {pf} on flat ground and {ps} at settlements (exact, "
                "no random draws).",
                "योगायोगाची पातळी कशी काढली: नवीन पाणी किंवा संभाव्य-पाण्याचा भाग नोंदीच्या सहनसीमेत (नोंदीची स्थान-अचूकता "
                "आणि ५०० मी यांपैकी मोठे) असल्यास ती नोंद जुळली असे मानले. प्रत्येक नोंदीसाठी आम्ही संदर्भ संचातील त्याच "
                "सहनसीमेत शोध असलेल्या भागाचा वाटा घेतो, आणि वाटे बेरीज करतो. सपाट जमीन: दोन्ही तारखांना रडार डेटा असलेला "
                "प्रत्येक ४० मी चौकोन, कायमच्या पाण्याबाहेर, उतार ≤ ५° ({km} चौ. किमी). वस्त्या: रडार डेटा असलेली {p} "
                "OpenStreetMap गावे, शहरे आणि उपनगरे. योगायोगाने {k} किंवा अधिक मिळण्याची शक्यता सपाट जमिनीवर {pf} आणि "
                "वस्त्यांवर {ps} आहे (अचूक, यादृच्छिक काढणी नाही).",
                km=f"{fb['flat']['km2']:,.0f}", p=fb["settlements"]["places"], k=k,
                pf=f"{fb['flat']['prob_at_least_observed']:.2f}", ps=f"{fb['settlements']['prob_at_least_observed']:.2f}"))
            st.dataframe(pd.DataFrame([{
                tr("Report", "नोंद"): e["id"], tr("Place", "ठिकाण"): e["place"],
                tr("Tolerance (m)", "सहनसीमा (मी)"): e["tolerance_m"],
                tr("Nearest detection (m)", "सर्वात जवळचा शोध (मी)"): e["distance_m"],
                tr("Matched", "जुळले"): YESNO[bool(e["matched"])],
                tr("Nearest new open water (km)", "सर्वात जवळचे नवीन खुले पाणी (किमी)"): round(e["nearest_new_water_m"] / 1000, 1),
                tr("Flat ground within tolerance of a detection", "शोधाच्या सहनसीमेतील सपाट जमीन"): pct(e["chance"]["flat_ground"]),
                tr("Settlements within tolerance of a detection", "शोधाच्या सहनसीमेतील वस्त्या"): pct(e["chance"]["settlements"])}
                for e in fb["events"]]), hide_index=True, width="stretch")
            st.markdown("#### " + tr("Every reported event", "प्रत्येक नोंदवलेली घटना"))
        from lib import evidence as _ev
        _df, _cc = _ev.events_table(val)
        st.dataframe(_df, hide_index=True, width="stretch", column_config=_cc)
    else:
        st.info(tr("Runs once reported events are added.", "नोंदवलेल्या घटना जोडल्यावर चालते."))
with tabs[1]:
    if xt:
        short(tr("an independent NISAR orbit re-found {c} of the {n} zones it could see, {l}× more often than chance. "
                 "A small sample, so support, not proof.",
                 "एका स्वतंत्र निसार कक्षेने तिला दिसू शकलेल्या {n} पैकी {c} क्षेत्रे पुन्हा शोधली, योगायोगापेक्षा {l}× जास्त "
                 "वेळा. नमुना लहान आहे, म्हणून आधार, पुरावा नव्हे.",
                 c=xt["confirmed"], n=xt["scored"], l=ui.fmt_num(xt["lift"] or 0, 0)))
        c, ch = xt["status_counts"], xt.get("chance", {})
        pb, pa = ui.date(xt["pair"]["before"]), ui.date(xt["pair"]["after"])
        st.markdown(tr(
            "Same slide rule, run on NISAR track {t} ({b} to {a}). A track-034 zone counts as **found again** when a "
            "track-{t} zone lies within {m} m (allowing for small position differences between orbits). **Partial** "
            "means only one piece of the evidence is there (coherence loss or the backscatter jump): that alone is "
            "common in the monsoon, so we do not count it.",
            "तोच भूस्खलन नियम, निसार मार्ग {t} वर चालवला ({b} ते {a}). मार्ग-०३४ चे क्षेत्र तेव्हा **पुन्हा सापडले** मानले "
            "जाते जेव्हा मार्ग-{t} चे क्षेत्र {m} मीटरच्या आत असते (कक्षांमधील लहान स्थान-फरकांसाठी सवलत). **अंशतः** म्हणजे "
            "पुराव्याचा फक्त एक भाग आहे (कोहेरन्समधील घट किंवा परावर्तनातील उसळी): पावसाळ्यात हे एकटे सामान्य आहे, म्हणून "
            "आम्ही ते मोजत नाही.", t=xt["pair"]["track"], b=pb, a=pa, m=f"{xt['buffer_m']:.0f}"))
        st.dataframe(pd.DataFrame([
            {"": tr("Our zones", "आमची क्षेत्रे"), tr("Found again", "पुन्हा सापडले"): str(c.get("confirmed", 0)),
             tr("Partial", "अंशतः"): str(c.get("partial", 0)), tr("Not seen", "दिसले नाही"): str(c.get("not seen", 0)),
             tr("Not covered by track 106", "मार्ग १०६ च्या कक्षेबाहेर"): str(c.get("not covered", 0)),
             tr("Found-again rate", "पुन्हा सापडण्याचा दर"): pct(xt["real"]["confirmed"])},
            {"": tr("Same zones moved to random steep places ({n} trials)",
                    "तीच क्षेत्रे यादृच्छिक तीव्र ठिकाणी हलवली ({n} चाचण्या)", n=ch.get("trials", 0)),
             tr("Found again", "पुन्हा सापडले"): "", tr("Partial", "अंशतः"): "", tr("Not seen", "दिसले नाही"): "",
             tr("Not covered by track 106", "मार्ग १०६ च्या कक्षेबाहेर"): "",
             tr("Found-again rate", "पुन्हा सापडण्याचा दर"): pct(ch.get("confirmed") or 0, 1)},
        ]), hide_index=True, width="stretch")
        if xt["lift"] is not None:
            pv = xt.get("p_value")
            ptxt = (" " + tr("The chance of doing this well by luck alone is about {p} (one-sided binomial test).",
                             "केवळ नशिबाने इतके चांगले होण्याची शक्यता सुमारे {p} आहे (एकतर्फी द्विपद चाचणी).", p=pct(pv))
                    if pv is not None and pv >= 0.01 else
                    (" " + tr("The chance of doing this well by luck alone is under 1%.",
                              "केवळ नशिबाने इतके चांगले होण्याची शक्यता १% पेक्षा कमी आहे.") if pv is not None else ""))
            st.markdown((tr("Our zones were found again **{l}× more often than chance**.",
                            "आमची क्षेत्रे **योगायोगापेक्षा {l}× जास्त वेळा** पुन्हा सापडली.", l=f"{xt['lift']:.0f}") + ptxt)
                        if xt["good"] else
                        tr("Our zones were found again about as often as chance ({l}×), so single-track zones need "
                           "ground checks before anyone relies on them.",
                           "आमची क्षेत्रे साधारण योगायोगाइतकीच पुन्हा सापडली ({l}×), म्हणून एका मार्गावरील क्षेत्रांवर कोणी "
                           "अवलंबून राहण्याआधी जमिनीवर तपासणी हवी.", l=f"{xt['lift']:.1f}"))
        if xt.get("small"):
            st.markdown(tr("Track {t} sees only {c} of the study area, so only {n} of our zones could be checked. That is "
                           "a small sample: treat it as support, not proof.",
                           "मार्ग {t} अभ्यास क्षेत्राचा फक्त {c} भाग पाहतो, म्हणून आमच्या फक्त {n} क्षेत्रांची तपासणी झाली. "
                           "हा लहान नमुना आहे: त्याला आधार माना, पुरावा नव्हे.",
                           t=xt["pair"]["track"], c=xt["coverage"], n=xt["scored"]))
        shf = (xt.get("scene_shift_db") or {}).get("track106")
        if shf:
            st.markdown(tr(
                "Between {b} and {a} the whole scene got about {h} dB darker in HH and {v} dB in HV, on flat and steep "
                "ground alike: ground and plants drying after the storm, or calibration of these provisional products. "
                "A landslide is a local change, so on both tracks we measure change against the scene's own median "
                "change on dry land.",
                "{b} ते {a} दरम्यान संपूर्ण दृश्य HH मध्ये सुमारे {h} dB आणि HV मध्ये {v} dB गडद झाले, सपाट आणि तीव्र "
                "जमिनीवर सारखेच: वादळानंतर जमीन आणि वनस्पती सुकणे, किंवा या तात्पुरत्या उत्पादनांचे कॅलिब्रेशन. भूस्खलन हा "
                "स्थानिक बदल आहे, म्हणून दोन्ही मार्गांवर आम्ही कोरड्या जमिनीवरील दृश्याच्या स्वतःच्या मध्यम बदलाशी तुलना "
                "करून बदल मोजतो.", b=pb, a=pa, h=f"{abs(shf['hh_db']):.1f}", v=f"{abs(shf['hv_db']):.1f}"))
        if xt.get("water_reliable") is False:
            st.caption(tr("Water areas from track {t} are not used: on {b}, in heavy rain, the radar saw less than half of "
                          "the permanent reservoirs as dark water, because rain roughens the surface.",
                          "मार्ग {t} वरील पाण्याचे क्षेत्रफळ वापरले नाही: {b} ला, मुसळधार पावसात, रडारने कायमच्या धरणांपैकी "
                          "अर्ध्याहून कमी भाग गडद पाणी म्हणून पाहिला, कारण पाऊस पृष्ठभाग खडबडीत करतो.",
                          t=xt["pair"]["track"], b=pb))
        by = xt.get("status_by_confidence") or {}
        if by:
            CONF = {"high": tr("High", "उच्च"), "medium": tr("Medium", "मध्यम"), "low": tr("Low", "कमी")}
            st.caption(tr("By confidence:", "खात्रीनुसार:") + " " + "; ".join(
                tr("{c}: {f} of {n} found again", "{c}: {n} पैकी {f} पुन्हा सापडली", c=CONF[k_], f=v_.get("confirmed", 0),
                   n=v_.get("confirmed", 0) + v_.get("partial", 0) + v_.get("not seen", 0))
                for k_, v_ in sorted(by.items(), key=lambda kv: ["high", "medium", "low"].index(kv[0]))))
    else:
        st.info(tr("Runs once the track-106 files are cropped.", "मार्ग-१०६ च्या फाइल्स कापल्यावर चालते."))
with tabs[2]:
    if dc:
        hi = dc["by_confidence"].get("high", {})
        short(tr("{f} of {z} zones survive when slope comes from NASA's NASADEM, including {hf} of {hz} high-confidence "
                 "ones.", "उतार नासाच्या NASADEM वरून घेतल्यावर {z} पैकी {f} क्षेत्रे टिकतात, त्यात {hz} पैकी {hf} उच्च "
                 "खात्रीची.", f=dc["found"], z=dc["zones_main"], hf=hi.get("found", 0), hz=hi.get("zones", 0)))
        rs = dc["not_found_reasons"]
        st.markdown(tr(
            "Slope and slope direction decide where the slide rule looks, so we ran it again on the same radar pair "
            "with NASA's NASADEM elevation map instead of Copernicus. Overall the two slope maps agree closely (median "
            "difference {d}°). Near the {a}° and {b}° limits they do not: of the ground that either map puts inside "
            "that band, the other map puts {p} outside it.",
            "उतार आणि उताराची दिशा भूस्खलन नियम कुठे पाहतो ते ठरवतात, म्हणून आम्ही तो त्याच रडार जोडीवर कोपर्निकसऐवजी "
            "नासाच्या NASADEM उंची नकाशासह पुन्हा चालवला. एकूण दोन्ही उतार-नकाशे जवळून जुळतात (मध्यम फरक {d}°). {a}° आणि "
            "{b}° मर्यादांजवळ ते जुळत नाहीत: कोणताही एक नकाशा जी जमीन त्या पट्ट्यात ठेवतो, तिच्यापैकी {p} भाग दुसरा नकाशा "
            "बाहेर ठेवतो.", d=f"{dc['slope']['median_abs_diff_deg']:.0f}",
            a=f"{th.get('slide_min_slope_deg', 15):.0f}", b=f"{th.get('slide_max_slope_deg', 45):.0f}",
            p=pct(1 - dc["slope"]["band_agreement"])))
        st.markdown(tr("**{f} of {z}** zones are found again within {m} m, including **{hf} of {hz}** high-confidence "
                       "zones. NASADEM also finds {nw} zones of its own.",
                       "**{z} पैकी {f}** क्षेत्रे {m} मीटरच्या आत पुन्हा सापडतात, त्यात **{hz} पैकी {hf}** उच्च खात्रीची "
                       "क्षेत्रे. NASADEM स्वतःची {nw} क्षेत्रेही शोधतो.", f=dc["found"], z=dc["zones_main"],
                       m=f"{dc['buffer_m']:.0f}", hf=hi.get("found", 0), hz=hi.get("zones", 0), nw=dc["new_in_nasadem"]))
        RS = {"steeper than 45° in NASADEM": tr("Steeper than 45°", "४५° पेक्षा तीव्र"),
              "gentler than 15° in NASADEM": tr("Gentler than 15°", "१५° पेक्षा सौम्य"),
              "radar layover or shadow in NASADEM": tr("Radar layover or shadow", "रडार ले-ओव्हर किंवा सावली"),
              "near the edge of the slope band in NASADEM": tr("Near the edge of the slope band", "उतार-पट्ट्याच्या कडेजवळ")}
        st.dataframe(pd.DataFrame(
            [{tr("Not found with NASADEM because", "NASADEM सह न सापडण्याचे कारण"): RS.get(k_, k_), tr("Zones", "क्षेत्रे"): v_}
             for k_, v_ in rs.items()]), hide_index=True, width="content")
        rh = dc["reported_slide_hits"]
        hits = [s for s in dc["reported_slides"] if s["main"] == "hit"]
        if hits and rh["nasadem"] < rh["main"]:
            dist = tr(" and ", " आणि ").join(f"{s['main_distance_m'] / 1000:.1f} km" for s in hits)
            same = len(rh["main_hit_zones"]) == 1
            st.markdown(
                (tr("The {n} reported landslides we matched ({ids}) are all matched to the same zone, {z}, {d} away.",
                    "आम्ही जुळवलेली {n} नोंदवलेली भूस्खलने ({ids}) सर्व एकाच क्षेत्राशी, {z}, {d} अंतरावर जुळतात.",
                    n=len(hits), ids=", ".join(s["id"] for s in hits), z=rh["main_hit_zones"][0], d=dist) if same else
                 tr("The {n} reported landslides we matched are {d} from their nearest zone.",
                    "आम्ही जुळवलेली {n} नोंदवलेली भूस्खलने त्यांच्या सर्वात जवळच्या क्षेत्रापासून {d} दूर आहेत.",
                    n=len(hits), d=dist))
                + " " + tr("With NASADEM, {k} of {n} reports have a zone within range. So treat the landslide matches as "
                           "weak support.", "NASADEM सह, {n} पैकी {k} नोंदींच्या टप्प्यात क्षेत्र आहे. म्हणून भूस्खलनाच्या "
                           "जुळण्यांना कमकुवत आधार माना.", k=rh["nasadem"], n=rh["scored"]))
        both = [f["properties"]["id"] for f in (data.geojson("slide_zones.geojson") or {}).get("features", [])
                if f["properties"].get("nasadem") == "found" and f["properties"].get("track106") == "confirmed"]
        if both:
            st.markdown(tr("Passing both extra checks (found again by the second NISAR track and with NASADEM): **{z}**.",
                           "दोन्ही अतिरिक्त तपासण्या पार करणारी (दुसऱ्या निसार मार्गावर आणि NASADEM सह पुन्हा सापडलेली): "
                           "**{z}**.", z=", ".join(both)))
with tabs[3]:
    if sens and sens.get("rows"):
        r0 = sens["range"]
        short(tr("the reservoir rise holds up ({a} to {b} km²); the flood area does not ({c} to {d} km²), so read it as "
                 "an order of magnitude.", "धरणांची वाढ टिकते ({a} ते {b} चौ. किमी); पुराचे क्षेत्रफळ टिकत नाही ({c} ते "
                 "{d} चौ. किमी), म्हणून त्याला केवळ परिमाणाचा अंदाज म्हणून वाचा.",
                 a=f"{r0['rise_km2'][0]:.1f}", b=f"{r0['rise_km2'][1]:.1f}", c=f"{r0['flood_km2'][0]:.2f}",
                 d=f"{r0['flood_km2'][1]:.1f}"))
        st.markdown(tr(
            "The water threshold is set from the radar itself on each date. Moving both dates' thresholds 1 dB down or "
            "up, and changing nothing else, keeps reservoir and river rise between **{a} and {b} km²** (we report "
            "{r}). Flooding on ground that was never wet swings from **{c} to {d} km²** (we report {f}): that figure "
            "depends heavily on the threshold, so read it as the order of magnitude, not a precise area.",
            "पाण्याची मर्यादा प्रत्येक तारखेला रडारवरूनच ठरते. दोन्ही तारखांच्या मर्यादा १ dB खाली किंवा वर हलवल्या आणि "
            "बाकी काही बदलले नाही, तरी धरणे आणि नद्यांची वाढ **{a} ते {b} चौ. किमी** दरम्यान राहते (आम्ही {r} नोंदवतो). "
            "कधीही ओल्या न झालेल्या जमिनीवरील पूर **{c} ते {d} चौ. किमी** पर्यंत बदलतो (आम्ही {f} नोंदवतो): तो आकडा "
            "मर्यादेवर खूप अवलंबून आहे, म्हणून त्याला अचूक क्षेत्रफळ नव्हे, परिमाणाचा अंदाज म्हणून वाचा.",
            a=f"{r0['rise_km2'][0]:.1f}", b=f"{r0['rise_km2'][1]:.1f}", r=f"{sens['base']['rise_km2']:.1f}",
            c=f"{r0['flood_km2'][0]:.2f}", d=f"{r0['flood_km2'][1]:.1f}", f=f"{sens['base']['flood_km2']:.2f}"))
        st.dataframe(pd.DataFrame([{
            tr("Threshold shift", "मर्यादेतील बदल"): f"{r['shift_db']:+.0f} dB" if r["shift_db"] else tr("as chosen", "निवडल्याप्रमाणे"),
            tr("Threshold {d} (dB)", "मर्यादा {d} (dB)", d=ui.day_short(before)): round(r["threshold_before_db"], 1),
            tr("Threshold {d} (dB)", "मर्यादा {d} (dB)", d=ui.day_short(after)): round(r["threshold_after_db"], 1),
            tr("New water (km²)", "नवीन पाणी (चौ. किमी)"): r["new_water_km2"],
            tr("Reservoir and river rise (km²)", "धरणे आणि नद्यांची वाढ (चौ. किमी)"): r["rise_km2"],
            tr("Flooding (km²)", "पूर (चौ. किमी)"): r["flood_km2"], tr("Flood patches", "पुराचे भाग"): r["flood_patches"],
            tr("Permanent water seen dark", "गडद दिसलेले कायमचे पाणी"): pct(r["permanent_water_seen_dark"])}
            for r in sens["rows"]]), hide_index=True, width="stretch")
with tabs[4]:
    ws = data.table("water_stats.csv")
    if ws is not None:
        st.dataframe(ws, hide_index=True, width="stretch")
    st.markdown(tr("Sanity check: on {d} the radar saw **{p}** of the JRC permanent-water pixels as water. A low value "
                   "would mean the threshold or the data is off.",
                   "सुसंगतता तपासणी: {d} ला रडारने JRC कायमच्या पाण्याच्या चौकोनांपैकी **{p}** पाणी म्हणून पाहिले. कमी "
                   "मूल्य म्हणजे मर्यादा किंवा डेटा चुकीचा असता.", d=ui.date(before),
                   p=pct(m.get("water", {}).get("permanent_water_seen_dark") or 0)))

# ---------------------------------------------------------------- data
section("data")
ROLE = {"before": tr("before, track 034", "आधी, मार्ग ०३४"), "after": tr("after, track 034", "नंतर, मार्ग ०३४"),
        "pair": tr("coherence, track 034", "कोहेरन्स, मार्ग ०३४"),
        "check_before": tr("second-track check, before, track 106", "दुसऱ्या मार्गाची तपासणी, आधी, मार्ग १०६"),
        "check_after": tr("second-track check, after, track 106", "दुसऱ्या मार्गाची तपासणी, नंतर, मार्ग १०६"),
        "check_pair": tr("second-track check, coherence, track 106", "दुसऱ्या मार्गाची तपासणी, कोहेरन्स, मार्ग १०६")}
C_DATA, C_FILE, C_VALID, C_LINK = (tr("Data", "डेटा"), tr("File", "फाइल"), tr("Valid share of box", "क्षेत्राचा वैध भाग"),
                                   tr("Link", "दुवा"))
rows = [{C_DATA: f"NISAR L2 {'GUNW' if s['role'].endswith('pair') else 'GCOV'} ({ROLE.get(s['role'], s['role'])})",
         C_FILE: s["granule_id"], C_VALID: pct(s["valid_fraction"]), C_LINK: s["url"]} for s in srcs]
rows += [
    {C_DATA: tr("Permanent water", "कायमचे पाणी"), C_FILE: "JRC Global Surface Water v1.4 occurrence (Pekel et al., 2016)",
     C_VALID: "", C_LINK: "https://global-surface-water.appspot.com/"},
    {C_DATA: tr("Elevation and slope", "उंची आणि उतार"), C_FILE: "Copernicus GLO-30 DEM (ESA)", C_VALID: "",
     C_LINK: "https://registry.opendata.aws/copernicus-dem/"},
    {C_DATA: tr("Place names", "ठिकाणांची नावे"),
     C_FILE: "OpenStreetMap villages, towns and suburbs (ODbL), via Overpass and Nominatim",
     C_VALID: "", C_LINK: "https://www.openstreetmap.org/copyright"},
]
if data.nearby():
    rows.append({C_DATA: tr("Roads and railways near each zone", "प्रत्येक क्षेत्राजवळचे रस्ते आणि रेल्वे"),
                 C_FILE: "OpenStreetMap ways: motorway to tertiary roads, and railway lines (ODbL), via Overpass",
                 C_VALID: "", C_LINK: "https://www.openstreetmap.org/copyright"})
if dc:
    rows.append({C_DATA: tr("Elevation, second-map check", "उंची, दुसऱ्या नकाशाची तपासणी"),
                 C_FILE: "NASADEM_HGT v001 (NASA / USGS)", C_VALID: "", C_LINK: dc["check_dem_url"]})
rain = data.rainfall()
if rain is not None:
    src = str(rain["source"].iloc[0]) if "source" in rain else "daily rainfall"
    link = "https://power.larc.nasa.gov/" if "POWER" in src else "https://giovanni.gsfc.nasa.gov/"
    rows.append({C_DATA: tr("Daily rainfall", "रोजचा पाऊस"), C_FILE: src, C_VALID: "", C_LINK: link})
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={C_LINK: st.column_config.LinkColumn(C_LINK)})
st.caption(tr("File names and data sources are kept as published, in English.",
              "फाइल्सची नावे आणि डेटा स्रोत प्रकाशित केल्याप्रमाणे, इंग्रजीत ठेवले आहेत."))

# ---------------------------------------------------------------- limits
section("limits")
seen = (m.get("water", {}).get("permanent_water_seen_dark") or 0)
LIMITS = [
    (tr("Provisional data", "तात्पुरता डेटा"),
     tr("These are NISAR provisional products (released from June 2026); calibration may still change.",
        "ही निसारची तात्पुरती उत्पादने आहेत (जून २०२६ पासून प्रकाशित); कॅलिब्रेशन अजून बदलू शकते.")),
    (tr("Two snapshots, twelve days apart", "बारा दिवसांच्या अंतराने दोन छायाचित्रे"),
     tr("Anything that flooded and drained between {b} and {a} is invisible.",
        "{b} ते {a} दरम्यान पूर येऊन ओसरलेले काहीही दिसत नाही.", b=ui.day(before), a=ui.date(after))),
    (tr("Cities", "शहरे"), tr("Buildings make flooded streets bright, not dark. Our new-water map under-counts urban "
                              "flooding.", "इमारतींमुळे पाण्याखालचे रस्ते गडद नव्हे, उजळ दिसतात. आमचा नवीन-पाण्याचा नकाशा "
                              "शहरी पूर कमी मोजतो.")),
    (tr("Pixel size", "चौकोनाचा आकार"), tr("{r} m pixels. Slides narrower than about two pixels are easily missed.",
                                          "{r} मीटर चौकोन. सुमारे दोन चौकोनांपेक्षा अरुंद भूस्खलने सहज सुटतात.",
                                          r=f"{m['grid']['res_m']:.0f}")),
    (tr("Same-mode rule", "एकाच पद्धतीचा नियम"),
     tr("From 27 August to 2 October NISAR imaged this track in a different mode (2005, quad-pol); 14 October is back "
        "in the July mode. Brightness is only compared between passes with the same track, mode and polarisation.",
        "२७ ऑगस्ट ते २ ऑक्टोबर निसारने हा मार्ग वेगळ्या पद्धतीत (2005, क्वाड-पोल) टिपला; १४ ऑक्टोबरला पुन्हा जुलैची पद्धत. "
        "चमकेची तुलना फक्त एकाच मार्ग, पद्धत आणि ध्रुवीकरणाच्या निरीक्षणांमध्ये होते.")),
    (tr("Water areas may be underestimates", "पाण्याचे क्षेत्रफळ कमी अंदाजले असू शकते"),
     tr("On {d} only {p} of the area the JRC record marks as permanent water looked dark enough to pass our water test. "
        "Part of that is reservoirs drawn down before the monsoon; part is water roughened by wind or rain, which our "
        "test misses.", "{d} ला JRC नोंद कायमचे पाणी म्हणून दाखवत असलेल्या भागापैकी फक्त {p} भाग आमची पाण्याची चाचणी "
        "पार करण्याइतका गडद दिसला. त्याचा काही भाग पावसाळ्याआधी खाली गेलेली धरणे; काही भाग वारा किंवा पावसाने खडबडीत "
        "झालेले पाणी, जे आमची चाचणी चुकवते.", d=ui.date(before), p=pct(seen))),
    (tr("Small samples", "लहान नमुने"),
     tr("Every check is counted, not turned into an accuracy: floods {fh} of {fo}, landslides {sh} of {so}, and the "
        "second-track check covers only part of the area.",
        "प्रत्येक तपासणी मोजली आहे, अचूकतेत बदलली नाही: पूर {fo} पैकी {fh}, भूस्खलने {so} पैकी {sh}, आणि दुसऱ्या "
        "मार्गाची तपासणी क्षेत्राचा फक्त काही भाग व्यापते.", fh=fh, fo=fo, sh=sh_, so=so_)),
    (tr("Flood area is threshold-sensitive", "पुराचे क्षेत्रफळ मर्यादेवर अवलंबून"),
     tr("The flood figure can move several-fold with a 1 dB change in the water threshold; the reservoir rise much less "
        "(see the water-threshold check).", "पाण्याच्या मर्यादेत १ dB बदलाने पुराचा आकडा अनेक पटींनी बदलू शकतो; धरणांची "
        "वाढ खूपच कमी (पाण्याच्या मर्यादेची तपासणी पाहा).")),
    (tr("Slope near the limits", "मर्यादांजवळचा उतार"),
     tr("Many zones sit close to the {a}° or {b}° limits, so a different elevation map moves some of them in or out "
        "(see the elevation-map check).", "अनेक क्षेत्रे {a}° किंवा {b}° मर्यादांजवळ आहेत, म्हणून वेगळा उंची नकाशा "
        "त्यांपैकी काहींना आत किंवा बाहेर हलवतो (उंची नकाशाची तपासणी पाहा).",
        a=f"{th.get('slide_min_slope_deg', 15):.0f}", b=f"{th.get('slide_max_slope_deg', 45):.0f}")),
    (tr("Leads, not verdicts", "संकेत, निर्णय नव्हे"),
     tr("Slide zones are places to check, not confirmed landslides: {u} of {z} have no reported event within 2 km.",
        "भूस्खलन क्षेत्रे तपासण्याची ठिकाणे आहेत, निश्चित भूस्खलने नव्हेत: {z} पैकी {u} क्षेत्रांच्या २ किमीच्या आत "
        "नोंदवलेली घटना नाही.", u=val_s.get("unreported_slide_zones", 0), z=m.get("slides", {}).get("zones", 0))),
    (tr("Rainfall", "पाऊस"),
     tr("GPM IMERG Late Run, averaged over the whole study area per UTC day. It is lower than the single-station "
        "totals quoted in the news, and may shift slightly when the Final Run is released.",
        "GPM IMERG Late Run, प्रत्येक UTC दिवसासाठी संपूर्ण अभ्यास क्षेत्राची सरासरी. ती बातम्यांमधील एका केंद्राच्या "
        "आकड्यांपेक्षा कमी आहे, आणि Final Run प्रकाशित झाल्यावर थोडी बदलू शकते.")),
]
st.markdown('<div class="ml-cardgrid">' + "".join(
    f'<div class="lim"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>' for t, d in LIMITS) + "</div>",
    unsafe_allow_html=True)

# ---------------------------------------------------------------- reproduce
section("reproduce-it")
st.markdown(tr("The code is public, and the Pune crops of every NISAR file above are in the repository (a few MB "
               "each), so one command rebuilds every number, map and list in this app from them. Fetching the crops "
               "again from NASA's archive needs a free Earthdata login. The whole pipeline runs in about two minutes on "
               "a two-core computer.",
               "कोड सार्वजनिक आहे, आणि वरील प्रत्येक निसार फाइलचे पुण्याचे तुकडे रिपॉझिटरीत आहेत (प्रत्येकी काही MB), म्हणून "
               "एकाच आदेशाने या ॲपमधील प्रत्येक आकडा, नकाशा आणि यादी पुन्हा तयार होते. नासाच्या संग्रहातून तुकडे पुन्हा "
               "मिळवण्यासाठी मोफत Earthdata लॉगिन लागते. संपूर्ण पाइपलाइन दोन-कोर संगणकावर सुमारे दोन मिनिटांत चालते."))
st.code("pip install -r requirements-pipeline.txt\n"
        "python -m pipeline.run_all        # water, slide zones, checks, evidence, maps, metrics.json\n"
        "python -m pytest -q               # the pipeline's tests\n\n"
        "# optional: fetch the crops again from NASA's archive (Earthdata login)\n"
        "python -m pipeline.crop --primary --timeline\n"
        "python -m pipeline.crop --granule <a track-106 file from the Data table>", language="bash")
st.markdown(tr("To point it at another place, change the study box and the NISAR files in `pipeline/config.py`.",
               "दुसऱ्या ठिकाणासाठी, `pipeline/config.py` मधील अभ्यास क्षेत्र आणि निसार फाइल्स बदला."))

section("team")
ui.team_cards()
ui.sources_line()
