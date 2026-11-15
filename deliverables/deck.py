"""The MonsoonLens deck (7 slides) and its appendix, from one layout spec, as PowerPoint files (python-pptx) and PDFs.
The .pptx files are uploaded to Google Drive, which converts them to Google Slides.

Numbers come from data/derived (pipeline) and deliverables/facts.py (sources). Positions are in points on a
960 x 540 pt (16:9) page.

  python deliverables/deck.py                 # -> deliverables/out/deck/*.pptx, *.pdf
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "deliverables"))
import facts as F  # noqa: E402

OUT = ROOT / "deliverables" / "out" / "deck"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS = ROOT / "deliverables" / "assets"
ASSET_URL = os.environ.get("ASSET_URL", "https://raw.githubusercontent.com/AyushSinghNegi/dancing-with-the-sars/"
                                        "claude/deliverables/deliverables/assets")
LINKS = json.loads((ROOT / "deliverables" / "links.json").read_text()) if (ROOT / "deliverables" / "links.json").exists() else {}
APP = "https://monsoonlens.streamlit.app"
REPO = "https://github.com/AyushSinghNegi/dancing-with-the-sars"

M = json.loads((ROOT / "data" / "derived" / "metrics.json").read_text())
FB = json.loads((ROOT / "data" / "derived" / "flood_baseline.json").read_text())
W, S, V, XT, DC, SE = M["water"], M["slides"], M["validation"], M["crosstrack"], M["dem_check"], M["sensitivity"]
CLOUD = json.loads((ROOT / "data" / "reference" / "cloud_check.json").read_text())
TL = [r for r in __import__("csv").DictReader(open(ROOT / "data" / "derived" / "timeline.csv")) if r["same_mode_as_primary"] == "True"]

NAVY, NAVY2, PANEL, LINE = "#070c17", "#0b1630", "#101d3a", "#22314d"
INK, MUTED, CYAN, BLUE, DEEP, ORANGE, WHITE = "#e8eef7", "#9fb0c6", "#6fe3ff", "#3d8ef0", "#1f6fd1", "#f0743a", "#ffffff"
HEAD, BODY = "IBM Plex Sans Condensed", "IBM Plex Sans"


# ---------------------------------------------------------------- spec helpers
def text(x, y, w, h, runs, size=14, color=INK, font=BODY, bold=False, align="LEFT", valign="TOP", link=None,
         bullets=False, line=1.15):
    """runs: str, or list of paragraphs; a paragraph is str or list of (text, {style}) runs."""
    return dict(k="text", x=x, y=y, w=w, h=h, runs=runs, size=size, color=color, font=font, bold=bold, align=align,
                valign=valign, link=link, bullets=bullets, line=line)


def rect(x, y, w, h, fill=PANEL, line=None, round_=True, alpha=1.0, link=None):
    return dict(k="rect", x=x, y=y, w=w, h=h, fill=fill, line=line, round=round_, alpha=alpha, link=link)


def img(x, y, w, h, name, link=None, fit="contain"):
    """fit="contain" keeps the whole picture inside the box; "cover" fills the box and crops the overflow."""
    return dict(k="img", x=x, y=y, w=w, h=h, name=name, link=link, fit=fit)


def button(x, y, w, h, label, url, fill=BLUE, color=WHITE, size=11.5, line=None, align="CENTER", bold=True, sub=None):
    """A clickable shape with its label inside, so the whole shape is the link and the label keeps its colour.
    sub: a quieter second part of the label."""
    return dict(k="button", x=x, y=y, w=w, h=h, label=label, link=url, fill=fill, color=color, size=size, line=line,
                align=align, bold=bold, sub=sub)


def pill(x, y, w, label, url, fill=BLUE, color=WHITE, line=None):
    return [button(x, y, w, 28, label, url, fill=fill, color=color, line=line)]


MINOR = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "as", "at", "by", "in", "of", "off", "on",
         "per", "to", "up", "via", "vs"}


def title_case(s):
    """Title case, APA style: major words and words of four letters or more capitalized; short articles, conjunctions
    and prepositions lower case unless first, last or after a colon or full stop. Names like NISAR, MonsoonLens and
    iGenfinity are kept as written."""
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        core = w.strip("()\"'“”,.:;!?")
        lead = w[:len(w) - len(w.lstrip("(\"'“”"))]
        rest = w[len(lead):]
        first = i == 0 or words[i - 1].endswith((":", ".", "?", "!"))
        last = i == len(words) - 1
        if any(ch.isupper() for ch in core[1:]) or any(ch.isdigit() for ch in core) or not core:
            out.append(w)
        elif core.lower() in MINOR and not first and not last:
            out.append(lead + rest.lower())
        else:
            out.append(lead + "-".join(p[:1].upper() + p[1:] for p in rest.split("-")))
    return " ".join(out)


def frame(title, kicker, n, total=7, appendix=False):
    title, kicker = title_case(title), title_case(kicker)
    els = [rect(0, 0, 960, 540, fill=NAVY, round_=False),
           text(48, 30, 700, 20, kicker, size=12, color=CYAN, font=BODY, bold=True),
           text(48, 50, 864, 48, title, size=28, color=WHITE, font=HEAD, bold=True),
           img(44, 504, 22, 22, "igenfinity_logo_420.jpg"),
           text(72, 506, 500, 18, "MonsoonLens, Team iGenfinity, NASA Space Apps Challenge 2026", size=9, color=MUTED),
           text(780, 506, 132, 18, (f"Appendix {n}" if appendix else f"{n} / {total}"), size=9, color=MUTED, align="END")]
    return els


def kpi(x, y, w, h, big, label, accent=CYAN):
    return [rect(x, y, w, h, fill=PANEL, line=LINE), rect(x, y, 4, h, fill=accent, round_=False),
            text(x + 16, y + 10, w - 26, 34, big, size=26, color=WHITE, font=HEAD, bold=True),
            text(x + 16, y + 44, w - 26, h - 50, label, size=10.5, color=MUTED, line=1.2)]


def L(key, default=None):
    return LINKS.get(key) or default


# ---------------------------------------------------------------- the 7 slides
def main_deck():
    xt_l, p = XT["lift_confirmed"], XT["p_value"]
    rise_lo, rise_hi = SE["range"]["rise_km2"]
    s = []
    # 1. title
    els = [rect(0, 0, 960, 540, fill=NAVY, round_=False), img(456, 0, 504, 540, "title_3d.jpg", fit="cover", link=APP),
           img(48, 40, 74, 74, "igenfinity_logo_420.jpg"),
           text(134, 52, 320, 52, [[("Team iGenfinity", {"bold": True, "color": WHITE})],
                                   "NASA Space Apps Challenge 2026: Dancing with the SARs"], size=11, color=MUTED),
           text(48, 150, 400, 70, "MonsoonLens", size=54, color=WHITE, font=HEAD, bold=True),
           text(48, 222, 390, 110, "What NASA–ISRO's NISAR radar saw through the 2026 Pune monsoon, turned into field "
                                   "check lists for the people who respond.", size=17, color=INK, line=1.25),
           text(48, 336, 400, 54, [[("Ayush Singh Negi", {"bold": True, "color": WHITE}), (": team lead, app and integration", {})],
                                   [("Rajendra Singh Negi", {"bold": True, "color": WHITE}), (": data and science", {})],
                                   [("Urvashi Negi", {"bold": True, "color": WHITE}), (": validation, story and pitch", {})]],
                size=10.5, color=MUTED)]
    els += pill(48, 404, 150, "Open the live app", APP)
    els += pill(206, 404, 128, "Watch the demo", L("video", APP), fill=ORANGE)
    els += pill(342, 404, 106, "Code and data", REPO, fill=PANEL, line=LINE)
    els += [text(48, 448, 400, 40, "Every number in this deck comes from our open pipeline or a cited source: see the "
                                   "appendix and the linked reports.", size=9, color=MUTED),
            text(470, 514, 476, 18, "3D view from the app: NISAR results over Copernicus GLO-30 elevation, heights ×2",
                 size=8, color=MUTED, align="END")]
    s.append(dict(id="s1", els=els))
    # 2. problem
    els = frame("Cloud hides the ground exactly when it matters", "The problem", 2)
    stats = [(f"{CLOUD['all_cloud']} of {CLOUD['images_available']}", "NASA daily satellite photos of the area, 3–8 July "
              "2026: only cloud"),
             (f"{F.LANDSLIDE_DEATHS_2004_2016:,}", "people killed by non-seismic landslides worldwide, 2004–2016 [1]"),
             (f"{F.INDIA_PRONE_SHARE}%", "of India's land is landslide-prone, 0.42 million km² [2]"),
             (f"{F.MALIN_DEATHS}", "killed by the Malin landslide in Pune district, 2014 [3]")]
    for i, (b, l) in enumerate(stats):
        els += kpi(48 + (i % 2) * 212, 118 + (i // 2) * 128, 200, 114, b, l, accent=[CYAN, ORANGE, BLUE, ORANGE][i])
    els += [img(490, 112, 422, 168, "rain_dark.png"),
            img(490, 290, 422, 150, "cloud_check_contact_sheet.jpg"),
            text(490, 444, 422, 40, "Top: daily rain from NASA GPM IMERG; dotted lines are the two NISAR passes. Bottom: "
                                    "NASA Worldview daily images, 28 June to 10 July: cloud on every storm day.",
                 size=9, color=MUTED),
            text(48, 384, 410, 100, "When the hills fail, district teams decide where to send survey crews from phone "
                                    "calls and news reports, which come from where people are, not from where the "
                                    "ground moved.", size=13, color=INK, line=1.25)]
    s.append(dict(id="s2", els=els))
    # 3. solution
    els = frame("NISAR's radar sees through cloud. MonsoonLens turns it into action.", "The solution", 3)
    steps = [("A satellite passes", "NISAR images nearly all land twice every 12 days, day or night [4]."),
             ("Radar sees through cloud", "L-band (24 cm) passes cloud and rain. Calm water looks dark."),
             ("We map the change", "Compare passes before and after the storm; map new water and likely slides.")]
    for i, (t, d) in enumerate(steps):
        y = 116 + i * 82
        els += [rect(48, y, 380, 72, fill=PANEL, line=LINE), rect(48, y, 36, 72, fill=[CYAN, BLUE, ORANGE][i]),
                text(48, y + 18, 36, 36, str(i + 1), size=20, color=NAVY, font=HEAD, bold=True, align="CENTER"),
                text(96, y + 8, 320, 22, t, size=14, color=WHITE, bold=True),
                text(96, y + 30, 326, 40, d, size=10.5, color=MUTED)]
    els += [text(48, 368, 380, 60, [[("One open pipeline, ", {"bold": True, "color": WHITE}),
                                     ("from NISAR files to maps, checks and a field list in "
                                      f"{F.PIPELINE_SECONDS // 60} min {F.PIPELINE_SECONDS % 60} s on a 2-core machine.", {})]],
                 size=12.5, color=INK, line=1.25)]
    chips = ["6 pages", "4 languages", "Guided tour", "Phone-ready", "Open source"]
    x = 48
    for c in chips:
        w = 16 + len(c) * 5.9
        els += [rect(x, 438, w, 24, fill=NAVY2, line=CYAN), text(x, 439, w, 22, c, size=9.5, color=CYAN, align="CENTER",
                                                                   valign="MIDDLE", bold=True)]
        x += w + 7
    els += [img(450, 112, 462, 260, "hero.jpg", link=APP), img(450, 382, 226, 110, "tour.jpg", link=APP),
            img(686, 382, 226, 110, "hindi.jpg", link=APP + "/?lang=hi")]
    s.append(dict(id="s3", els=els))
    # 4. results
    els = frame("What the radar found around Pune, 28 June to 10 July 2026", "Results", 4)
    els += [img(48, 104, 390, 390, "map_findings_dark.png")]
    k = [(f"{W['rise_km2']:.1f} km²", f"new water as reservoirs and rivers rose; {rise_lo:.1f}–{rise_hi:.1f} km² with "
          "the water threshold moved ±1 dB", BLUE),
         (f"{S['zones']}", f"likely landslide zones on 15–45° slopes, {S['high']} of them high confidence, each with "
          "radar evidence", ORANGE),
         (f"{float(TL[-1]['water_in_jrc_extent_km2']):.0f} km²", f"open water in rivers and reservoirs by 14 October, up "
          f"from {float(TL[0]['water_in_jrc_extent_km2']):.0f} km² on 28 June (5 same-mode passes)", CYAN),
         (f"{W['flood_km2']:.2f} km²", "flood water still standing on dry land on 10 July: an order of magnitude, "
          "very threshold-sensitive", DEEP)]
    for i, (b, l, a) in enumerate(k):
        els += kpi(462 + (i % 2) * 228, 104 + (i // 2) * 106, 216, 98, b, l, accent=a)
    els += [img(462, 318, 450, 176, "before_after_dark.png")]
    s.append(dict(id="s4", els=els))
    # 5. validity
    els = frame("Every result is checked, and the weak ones are shown too", "Validity", 5)
    els += [img(48, 102, 864, 296, "checks_dark.png")]
    cards = [(f"{xt_l:.0f}× chance", f"An independent NISAR orbit re-found {XT['status_counts']['confirmed']} of "
              f"{XT['real']['zones_scored']} zones it could see (p ≈ {p:.2f}).", BLUE),
             (f"{DC['found']} of {DC['zones_main']}", f"zones kept with NASA's NASADEM elevation map, "
              f"{DC['by_confidence']['high']['found']} of {DC['by_confidence']['high']['zones']} high-confidence.", ORANGE),
             (f"{V['slide']['hits']} of {V['slide']['observable']}", "reported landslides had a zone nearby, both near "
              "one zone: weak support.", CYAN),
             (f"{V['flood']['hits']} of {V['flood']['observable']}", "reported floods matched: no better than chance. The "
              "misses were in or near towns, where buildings can hide flooded streets.", DEEP)]
    for i, (b, l, a) in enumerate(cards):
        els += [rect(48 + i * 218, 404, 206, 90, fill=PANEL, line=LINE), rect(48 + i * 218, 404, 206, 4, fill=a, round_=False),
                text(60 + i * 218, 412, 186, 26, b, size=18, color=WHITE, font=HEAD, bold=True),
                text(60 + i * 218, 438, 186, 54, l, size=9.5, color=MUTED, line=1.15)]
    s.append(dict(id="s5", els=els))
    # 6. impact / demo
    els = frame("From a radar pass to a field crew, in minutes", "Impact", 6)
    els += [img(48, 104, 470, 300, "field.jpg", link=APP + "/field"),
            img(530, 104, 120, 260, "phone_place.jpg", link=APP + "/place?lang=mr"),
            img(660, 104, 120, 260, "phone_field.jpg", link=APP + "/field?lang=hi"),
            img(790, 104, 120, 260, "phone_home.jpg", link=APP)]
    who = [("District disaster teams", "Ranked list of likely slide zones with radar images, nearest roads, rail and "
            "villages; printable, KML for phones, CSV and GeoJSON."),
           ("People who live there", "Check a place: 431 villages and towns, 2, 5 or 10 km, in English, Hindi, Marathi "
            "or German, with a link to share."),
           ("Researchers and journalists", "Every number traced to its NISAR file, every check and limit, all code open.")]
    for i, (t, d) in enumerate(who):
        els += [text(48 + i * 290, 414, 278, 20, t, size=12.5, color=CYAN, bold=True),
                text(48 + i * 290, 434, 278, 60, d, size=10, color=INK, line=1.2)]
    els += [text(530, 372, 382, 30, "Phones: Check a place in Marathi, Field list in Hindi, Overview.", size=9, color=MUTED)]
    s.append(dict(id="s6", els=els))
    # 7. scale and business
    els = frame("From one district to every NISAR pass on Earth", "Scale and business", 7)
    els += [img(48, 104, 440, 196, "cost_to_cover_dark.png"),
            text(48, 308, 440, 60, [[(f"${F.yearly_cost(F.EARTH_LAND_KM2):,.0f} a year ", {"bold": True, "color": WHITE}),
                                     ("of cloud compute would run MonsoonLens on every NISAR pass over all land: measured "
                                      "runtime, published prices, 3× allowance for data access [5][6].", {})]],
                 size=11, color=INK, line=1.2),
            text(48, 372, 440, 124, [[("Open core. ", {"bold": True, "color": WHITE}),
                                      ("The app, maps and code stay free for everyone. District, state and infrastructure "
                                       "teams pay for their own area, alerts after every pass, a field app and support.", {})],
                                     [("The ask. ", {"bold": True, "color": ORANGE}),
                                      ("A 2027 monsoon pilot with three Western Ghats district teams, and seed funding to "
                                       "run on every new pass.", {})]], size=11, color=INK, line=1.2),
            img(508, 104, 404, 196, "revenue_dark.png")]
    docs = [("Business plan and global scale-up", "13 pages: market, model, costs, five-year plan", L("business_plan")),
            ("Technical and validation report", "data, method, every check, all 50 zones", L("technical")),
            ("Field operations guide", "how a district team uses the leads", L("field_guide")),
            ("Appendix slides", "data, method, checks, business, risks, sources", L("appendix")),
            ("Full demo video", "2 minutes, every feature, with captions", L("video_long", L("video")))]
    els += [text(508, 306, 404, 20, "Read more", size=12, color=CYAN, bold=True)]
    y = 328
    for label, sub, url in docs:
        els += [button(508, y, 404, 26, label, url or APP, fill=PANEL, color=WHITE, size=10.5, line=LINE, align="LEFT",
                       sub=sub)]
        y += 31
    els += [text(508, y + 2, 404, 30, "AI use: code, text and translations were drafted with an AI assistant and checked "
                                      "by the team. No NASA logos are used.", size=8.5, color=MUTED)]
    s.append(dict(id="s7", els=els))
    return s


REFS_MAIN = ["froude", "ndma_lrms", "malin", "nisar_overview", "aws", "cia_land"]


# ---------------------------------------------------------------- appendix
def appendix_deck():
    s = []
    els = [rect(0, 0, 960, 540, fill=NAVY, round_=False), img(48, 48, 64, 64, "igenfinity_logo_420.jpg"),
           text(48, 170, 860, 60, title_case("MonsoonLens: appendix"), size=44, color=WHITE, font=HEAD, bold=True),
           text(48, 236, 760, 60, "Data, method, every check, the business model and all sources behind the 7-slide deck.",
                size=17, color=INK),
           text(48, 330, 860, 120, [f"Live app: {APP}", f"Code and data: {REPO}",
                                    "Team iGenfinity, NASA Space Apps Challenge 2026 (GDG Ahlen)"], size=12, color=MUTED)]
    s.append(dict(id="a0", els=els))
    # A1 data
    els = frame("Data: six NISAR files and five open datasets", "Data", "A1", appendix=True)
    rows = [["NISAR L2 GCOV, track 34", "28 Jun and 10 Jul 2026 (mode 4005, DHDH)", "Backscatter, water, change"],
            ["NISAR L2 GUNW, track 34", "28 Jun – 10 Jul pair", "Coherence for slide zones"],
            ["NISAR L2 GCOV + GUNW, track 106", "3 – 15 Jul 2026", "Independent second-orbit check"],
            ["NISAR L2 GCOV, track 34", "5 same-mode passes, 28 Jun – 14 Oct", "Reservoirs through the season"],
            ["JRC Global Surface Water v1.4", "1984–2021 occurrence", "Water training, permanent water"],
            ["Copernicus GLO-30 DEM; NASADEM", "30 m", "Slope, layover, shadow; second check"],
            ["GPM IMERG Late Run", "Daily", "Rain context"],
            ["OpenStreetMap", "Places, roads, railways", "Names, nearby infrastructure"],
            ["Reported events", f"{V['events']} floods and landslides", "Validation, each with a source link"]]
    els += [dict(k="table", x=48, y=104, w=864, h=360, head=["Data", "Product", "Use"], rows=rows, widths=[34, 33, 33])]
    els += [text(48, 470, 864, 30, f"Every NISAR file is listed with its link on the app's Method page. Study box "
                                    f"{M['aoi']['west']}–{M['aoi']['east']}° E, {M['aoi']['south']}–{M['aoi']['north']}° N, "
                                    f"{F.TILE_KM2:,} km², 40 m grid.", size=10, color=MUTED)]
    s.append(dict(id="a1", els=els))
    # A2 method
    th = M["thresholds"]
    els = frame("Method: from radar brightness to ranked leads", "Method", "A2", appendix=True)
    rows = [["1. Cut", "Stream the study box; average to a 40 m grid; Lee filter"],
            ["2. Water", f"Per-date Kittler–Illingworth threshold trained on JRC water ({W['threshold_before_db']:.1f} / "
                         f"{W['threshold_after_db']:.1f} dB)"],
            ["3. New water", f"Water after, not before; ≥ {th['change_db']} dB darker; outside permanent water; flat"],
            ["4. Hidden water", "Flat ground that got brighter (double bounce): shown, never counted"],
            ["5. Slide zones", f"Coherence < {th['coherence_low']} and < 0.6× its 1 km area; HH +{th['slide_hh_rise_db']} dB or "
                               f"HV −{th['slide_hv_drop_db']} dB vs scene median; slope {th['slide_min_slope_deg']:.0f}–"
                               f"{th['slide_max_slope_deg']:.0f}°; no layover or shadow"],
            ["6. Score", "0–1 from slope, radar change and coherence loss"],
            ["7–10. Checks", "Reported events, second orbit, second DEM, threshold ±1 dB"],
            ["11. Package", f"{M['evidence']['chips']} image chips; field list as HTML, KML, CSV, GeoJSON"]]
    els += [dict(k="table", x=48, y=104, w=864, h=380, head=["Step", "What happens"], rows=rows, widths=[18, 82])]
    s.append(dict(id="a2", els=els))
    # A3 the app, page by page
    els = frame("The app, page by page", "The app", "A3", appendix=True)
    shots = [("hero.jpg", "Overview", "What happened, the key numbers, the 3D view and a guided tour", ""),
             ("story.jpg", "Story", "Five steps from cloud to radar to field list, with a before/after slider", "/story"),
             ("explore_flat.jpg", "Explore the map", "Every layer, every zone and flood patch, downloads", "/explore"),
             ("place.jpg", "Check a place", "431 villages and towns; what was found within 2, 5 or 10 km", "/place"),
             ("field.jpg", "Field check list", "Ranked leads, radar evidence, printable list and KML", "/field"),
             ("method.jpg", "Method and limits", "Every step, check, limit and NISAR file, in four languages", "/method")]
    for i, (f, t, d, u) in enumerate(shots):
        x, y = 48 + (i % 3) * 292, 104 + (i // 3) * 200
        els += [img(x, y, 280, 140, f, fit="cover", link=APP + u),
                rect(x, y, 280, 140, fill=NAVY, alpha=0.0, line=LINE, round_=False, link=APP + u),
                text(x, y + 146, 280, 18, t, size=11.5, color=WHITE, bold=True, link=None),
                text(x, y + 164, 280, 30, d, size=9, color=MUTED)]
    s.append(dict(id="a3", els=els))
    # A3 checks detail
    els = frame("Checks in detail", "Validity", "A4", appendix=True)
    rows = [["Second NISAR orbit", f"{XT['status_counts']['confirmed']} of {XT['real']['zones_scored']} re-found "
             f"({XT['real']['confirmed'] * 100:.1f}%) vs {XT['chance']['confirmed'] * 100:.1f}% at random steep places "
             f"({XT['chance']['trials']} trials); {XT['lift_confirmed']:.0f}×, p ≈ {XT['p_value']:.3f}; covers "
             f"{XT['valid_fraction'] * 100:.0f}% of the box"],
            ["NASADEM", f"{DC['found']} of {DC['zones_main']} kept (high {DC['by_confidence']['high']['found']}/"
                        f"{DC['by_confidence']['high']['zones']}, medium {DC['by_confidence']['medium']['found']}/"
                        f"{DC['by_confidence']['medium']['zones']}, low {DC['by_confidence']['low']['found']}/"
                        f"{DC['by_confidence']['low']['zones']}); slope correlation {DC['slope']['correlation']:.2f}"],
            ["Reported landslides", f"{V['slide']['hits']} of {V['slide']['observable']} with a zone nearby; both near "
                                    "one zone; none with NASADEM"],
            ["Reported floods", f"{V['flood']['hits']} of {V['flood']['observable']}; chance gives "
                                f"{FB['reference']['flat_ground']['expected_matches']:.1f} (flat land) and "
                                f"{FB['reference']['settlements']['expected_matches']:.1f} (settlements): no better than chance"],
            ["Water threshold ±1 dB", f"Reservoir rise {SE['range']['rise_km2'][0]:.1f}–{SE['range']['rise_km2'][1]:.1f} km²; "
                                      f"flood {SE['range']['flood_km2'][0]:.2f}–{SE['range']['flood_km2'][1]:.1f} km²"]]
    els += [dict(k="table", x=48, y=104, w=864, h=250, head=["Check", "Result"], rows=rows, widths=[22, 78])]
    els += [img(48, 362, 430, 136, "season_dark.png"), img(490, 362, 422, 136, "chips_dark.png")]
    s.append(dict(id="a3", els=els))
    # A4 business model
    els = frame("Business model and five-year plan (planning assumptions)", "Business", "A5", appendix=True)
    rows = [[k, "Free" if v[0] == 0 else f"${v[0]:,}", v[1]] for k, v in F.PRICES.items()]
    els += [dict(k="table", x=48, y=104, w=430, h=230, head=["Tier", "Per year", "Includes"], rows=rows, widths=[22, 18, 60],
                 size=8.5)]
    els += [img(490, 104, 422, 190, "revenue_dark.png"), img(48, 344, 430, 150, "funding_dark.png"),
            img(490, 304, 422, 190, "coverage_dark.png")]
    s.append(dict(id="a4", els=els))
    # A5 global architecture
    els = frame("How it scales to every NISAR pass on Earth", "Global scale-up", "A6", appendix=True)
    boxes = [("New NISAR pass published", "NASA catalogue watcher"), ("Tile job starts", f"{F.EARTH_LAND_KM2 / F.TILE_KM2:,.0f} "
             "land tiles of 7,116 km²"), ("Runs next to the data", "AWS us-west-2, Earthdata Cloud [7]"),
             ("Checks and evidence", "second orbit, DEM, thresholds"), ("Outputs", "COG, STAC, CAP alerts, field lists")]
    for i, (t, d) in enumerate(boxes):
        x = 48 + i * 176
        els += [rect(x, 120, 160, 96, fill=PANEL, line=CYAN if i in (0, 4) else LINE),
                text(x + 10, 130, 140, 40, t, size=12.5, color=WHITE, bold=True),
                text(x + 10, 172, 140, 40, d, size=9.5, color=MUTED)]
        if i < 4:
            els += [text(x + 160, 150, 16, 30, "→", size=16, color=CYAN, align="CENTER")]
    els += [text(48, 240, 416, 250, ["Self-calibrating: water thresholds trained per date from the global JRC record.",
                                     "Global inputs: Copernicus GLO-30 and NASADEM, OpenStreetMap places and roads.",
                                     "Local by design: four languages today, more per region.",
                                     "Science next: both orbit directions, InSAR motion, S-band and Sentinel-1, urban "
                                     "floods from double bounce."], size=12, color=INK, bullets=True, line=1.3),
            img(480, 232, 432, 262, "roadmap_dark.png")]
    s.append(dict(id="a5", els=els))
    # A6 risks
    els = frame("Limits and risks, and what we do about them", "Honesty", "A7", appendix=True)
    rows = [["Floods between buildings are likely missed (radar bounces off walls)", "Say so everywhere; research double bounce before claiming it"],
            ["Water between passes is invisible", "Both orbit directions: a look about every 6 days"],
            ["40 m pixels miss narrow slides", "Leads, not verdicts; field checks; finer products later"],
            ["Provisional NISAR products", "Re-run history when products are reprocessed"],
            ["False leads waste crews' time", "Rank by evidence; publish the field-verified hit rate"],
            ["Leads read as warnings", "Officials first; plain-language limits on every page"],
            ["Mission lifetime", "Add Sentinel-1 and S-band so the service outlives one satellite"]]
    els += [dict(k="table", x=48, y=104, w=864, h=360, head=["Limit or risk", "What we do"], rows=rows, widths=[45, 55])]
    s.append(dict(id="a6", els=els))
    # A8 team and use of AI
    els = frame("Team iGenfinity, and how we used AI", "Team", "A8", appendix=True)
    els += [img(48, 110, 150, 150, "igenfinity_logo_420.jpg")]
    people = [("Ayush Singh Negi", "Team lead: app and integration"),
              ("Rajendra Singh Negi", "Data and science"),
              ("Urvashi Negi", "Validation, story and pitch")]
    for i, (n, r) in enumerate(people):
        els += [rect(222, 110 + i * 54, 690, 46, fill=PANEL, line=LINE),
                text(238, 116 + i * 54, 220, 34, n, size=13, color=WHITE, bold=True, valign="MIDDLE"),
                text(452, 116 + i * 54, 450, 34, r, size=10.5, color=INK, valign="MIDDLE")]
    els += [text(48, 290, 864, 20, "Use of AI", size=13, color=CYAN, bold=True),
            text(48, 312, 864, 120, ["An AI coding assistant (Claude) helped write code, text, figures and the Hindi, "
                                     "Marathi and German translations. The team reviewed every result, and every number "
                                     "comes from our open pipeline or a cited source.",
                                     "No AI-generated images or video are used as evidence: radar images are NISAR data, maps "
                                     "are drawn from data, and screenshots and the demo video show the real app.",
                                     "No NASA logos or mission identifiers are used. NISAR data courtesy of NASA/JPL-Caltech "
                                     "and ISRO, via ASF DAAC."], size=11, color=INK, bullets=True, line=1.25)]
    els += pill(48, 448, 150, "Open the live app", APP) + pill(206, 448, 120, "Code and data", REPO, fill=PANEL, line=LINE)
    s.append(dict(id="a8", els=els))
    # A7 references
    els = frame("References and sources", "Sources", "A9", appendix=True)
    keys = REFS_MAIN + ["nisar_s3", "nisar_asf", "nisar_open", "rentschler", "gsi_wghats", "wayanad", "fc15", "sdmf",
                        "sdrf", "wef", "gca", "ew4all", "wmo_15", "pekel", "copdem", "nasadem", "imerg", "osm", "worldview"]
    lines = []
    for i, k_ in enumerate(keys, 1):
        t, u = F.SOURCES[k_]
        lines.append([(f"[{i}]  ", {"bold": True, "color": CYAN}), (t + "  ", {"color": INK}),
                      ("open", {"link": u, "color": CYAN, "bold": True})])
    els += [text(48, 104, 420, 380, lines[:13], size=8.6, color=INK, line=1.12),
            text(492, 104, 420, 380, lines[13:], size=8.6, color=INK, line=1.12),
            text(48, 486, 864, 16, "Each “open” links to the source.", size=8.5, color=MUTED)]
    s.append(dict(id="a9", els=els))
    return s


# ---------------------------------------------------------------- backend 1: python-pptx
EMBED_KB = 90   # in the Google Slides upload, bigger pictures are placeholders that Slides fills from the public URL


def cover_crop(name, w, h):
    """Crop an asset to the box's aspect ratio (centre), saved as its own file; returns the new name."""
    from PIL import Image
    src = ASSETS / name
    out = ASSETS / f"{Path(name).stem}_crop{int(w)}x{int(h)}.jpg"
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src).convert("RGB")
        ar, br = im.width / im.height, w / h
        if ar > br:
            nw = int(im.height * br)
            im = im.crop(((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height))
        else:
            nh = int(im.width / br)
            im = im.crop((0, (im.height - nh) // 2, im.width, (im.height - nh) // 2 + nh))
        im.save(out, quality=88)
    return out.name


def to_pptx(slides, path, placeholders=None):
    """placeholders: a list to collect (token, file) for pictures left out of the file (Google Slides upload)."""
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Pt
    from PIL import Image

    prs = Presentation()
    prs.slide_width, prs.slide_height = Pt(960), Pt(540)
    rgb = lambda h: RGBColor.from_string(h.lstrip("#"))
    for sd in slides:
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        for e in sd["els"]:
            if e["k"] == "rect":
                shp = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if e["round"] else MSO_SHAPE.RECTANGLE,
                                          Pt(e["x"]), Pt(e["y"]), Pt(e["w"]), Pt(e["h"]))
                if e["round"]:
                    shp.adjustments[0] = min(0.12, 6 / max(min(e["w"], e["h"]), 1))
                shp.fill.solid()
                shp.fill.fore_color.rgb = rgb(e["fill"])
                if e["alpha"] < 1:
                    from pptx.oxml.ns import qn
                    sf = shp.fill._xPr.find(qn("a:solidFill"))
                    clr = sf[0]
                    a = clr.makeelement(qn("a:alpha"), {"val": str(int(e["alpha"] * 100000))})
                    clr.append(a)
                if e["line"]:
                    shp.line.color.rgb = rgb(e["line"])
                    shp.line.width = Pt(0.75)
                else:
                    shp.line.fill.background()
                shp.shadow.inherit = False
                if e.get("link"):
                    shp.click_action.hyperlink.address = e["link"]
            elif e["k"] == "img":
                name = cover_crop(e["name"], e["w"], e["h"]) if e.get("fit") == "cover" else e["name"]
                f = ASSETS / name
                if not f.exists():
                    raise FileNotFoundError(f)
                if placeholders is not None and f.stat().st_size > EMBED_KB * 1024:
                    token = f"{{{{IMG:{len(placeholders):02d}}}}}"
                    placeholders.append((token, name))
                    shp = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(e["x"]), Pt(e["y"]), Pt(e["w"]), Pt(e["h"]))
                    shp.fill.background()
                    shp.line.fill.background()
                    shp.text_frame.text = token
                    shp.text_frame.paragraphs[0].runs[0].font.size = Pt(6)
                    continue
                iw, ih = Image.open(f).size
                bw, bh = e["w"], e["h"]
                r = min(bw / iw, bh / ih)
                w_, h_ = iw * r, ih * r
                pic = sl.shapes.add_picture(str(f), Pt(e["x"] + (bw - w_) / 2), Pt(e["y"] + (bh - h_) / 2), Pt(w_), Pt(h_))
                if e.get("link"):
                    pic.click_action.hyperlink.address = e["link"]
            elif e["k"] == "button":
                shp = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(e["x"]), Pt(e["y"]), Pt(e["w"]), Pt(e["h"]))
                shp.adjustments[0] = min(0.3, 6 / e["h"])
                shp.fill.solid()
                shp.fill.fore_color.rgb = rgb(e["fill"])
                if e["line"]:
                    shp.line.color.rgb = rgb(e["line"])
                    shp.line.width = Pt(0.75)
                else:
                    shp.line.fill.background()
                shp.shadow.inherit = False
                tf = shp.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = Pt(10)
                tf.margin_top = tf.margin_bottom = Pt(2)
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                pp = tf.paragraphs[0]
                pp.alignment = {"LEFT": PP_ALIGN.LEFT, "CENTER": PP_ALIGN.CENTER}[e["align"]]
                rr = pp.add_run()
                rr.text = e["label"]
                rr.font.size = Pt(e["size"])
                rr.font.name = BODY
                rr.font.bold = e["bold"]
                rr.font.color.rgb = rgb(e["color"])
                if e.get("sub"):
                    r2 = pp.add_run()
                    r2.text = "    " + e["sub"]
                    r2.font.size = Pt(e["size"] - 2)
                    r2.font.name = BODY
                    r2.font.color.rgb = rgb(MUTED)
                shp.click_action.hyperlink.address = e["link"]
            elif e["k"] == "text":
                tb = sl.shapes.add_textbox(Pt(e["x"]), Pt(e["y"]), Pt(e["w"]), Pt(e["h"]))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = Pt(2)
                tf.margin_top = tf.margin_bottom = Pt(1)
                tf.vertical_anchor = {"TOP": MSO_ANCHOR.TOP, "MIDDLE": MSO_ANCHOR.MIDDLE}[e["valign"]]
                paras = e["runs"] if isinstance(e["runs"], list) else [e["runs"]]
                for i, para in enumerate(paras):
                    pp = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    pp.alignment = {"LEFT": PP_ALIGN.LEFT, "CENTER": PP_ALIGN.CENTER, "END": PP_ALIGN.RIGHT}[e["align"]]
                    pp.line_spacing = e["line"]
                    if e["bullets"]:
                        pp.text = ""
                    runs = para if isinstance(para, list) else [(("• " if e["bullets"] else "") + para, {})]
                    for t, st in runs:
                        rr = pp.add_run()
                        rr.text = t
                        rr.font.size = Pt(e["size"])
                        rr.font.name = e["font"]
                        rr.font.bold = st.get("bold", e["bold"])
                        rr.font.color.rgb = rgb(st.get("color", e["color"]))
                        if st.get("link") or e.get("link"):
                            rr.hyperlink.address = st.get("link") or e["link"]
            elif e["k"] == "table":
                rows, cols = len(e["rows"]) + 1, len(e["head"])
                tbl = sl.shapes.add_table(rows, cols, Pt(e["x"]), Pt(e["y"]), Pt(e["w"]), Pt(e["h"])).table
                for j, wpc in enumerate(e["widths"]):
                    tbl.columns[j].width = Pt(e["w"] * wpc / 100)
                for i in range(rows):
                    for j in range(cols):
                        c = tbl.cell(i, j)
                        c.text = e["head"][j] if i == 0 else str(e["rows"][i - 1][j])
                        c.fill.solid()
                        c.fill.fore_color.rgb = rgb(DEEP if i == 0 else (PANEL if i % 2 else NAVY2))
                        c.vertical_anchor = MSO_ANCHOR.MIDDLE
                        c.margin_top = c.margin_bottom = Pt(3)
                        for pp in c.text_frame.paragraphs:
                            for rr in pp.runs:
                                rr.font.size = Pt(e.get("size", 10))
                                rr.font.name = BODY
                                rr.font.bold = i == 0
                                rr.font.color.rgb = rgb(WHITE if i == 0 else INK)
    # links in text use the theme's link colour: make it readable on the navy background
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    theme = prs.slide_masters[0].part.part_related_by(RT.THEME)
    xml = theme.blob.decode("utf-8")
    import re as _re
    for tag in ("hlink", "folHlink"):
        xml = _re.sub(rf"<a:{tag}>.*?</a:{tag}>", f'<a:{tag}><a:srgbClr val="{CYAN[1:].upper()}"/></a:{tag}>', xml, flags=_re.S)
    theme._blob = xml.encode("utf-8")
    prs.save(str(path))
    print(path)


if __name__ == "__main__":
    which = sys.argv[1:] or ["MonsoonLens_Appendix", "MonsoonLens_Deck"]
    sha = os.environ.get("ASSET_SHA", "claude/deliverables")
    base = f"https://raw.githubusercontent.com/AyushSinghNegi/dancing-with-the-sars/{sha}/deliverables/assets"
    for name, fn in (("MonsoonLens_Deck", main_deck), ("MonsoonLens_Appendix", appendix_deck)):
        if name not in which:
            continue
        slides = fn()
        p = OUT / f"{name}.pptx"
        to_pptx(slides, p)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(p)],
                       check=False, capture_output=True, timeout=300)
        ph = []
        to_pptx(slides, OUT / f"{name}_gslides.pptx", placeholders=ph)
        reqs = [{"replaceAllShapesWithImage": {"imageUrl": f"{base}/{f}", "imageReplaceMethod": "CENTER_INSIDE",
                                               "containsText": {"text": tok, "matchCase": True}}} for tok, f in ph]
        (OUT / f"{name}_gslides_images.json").write_text(json.dumps(reqs, separators=(",", ":")))
        print(name, len(slides), "slides,", len(ph), "pictures by URL")
