"""The independent checks behind the numbers, as one summary band (Overview and Method pages)."""
from __future__ import annotations

import html

import streamlit as st

from . import data, ui


def items() -> list[tuple[str, str, str]]:
    """(headline number, check name, one-line result) for each check that has run, strongest first."""
    tr, v, m = ui.tr, data.value, data.metrics()
    dc = m.get("dem_check") or {}
    sens = (m.get("sensitivity") or {}).get("range", {})
    checks = []
    if dc:
        hi = (dc.get("by_confidence") or {}).get("high") or {}
        checks.append((ui.t("x_of_y", x=dc["found"], y=dc["zones_main"]), tr("Second elevation map", "दुसरा उंची नकाशा"),
                       tr("slide zones kept when the rule is re-run on NASA's NASADEM{h}.",
                          "नासाच्या NASADEM वर नियम पुन्हा चालवल्यावर टिकलेली भूस्खलन क्षेत्रे{h}.",
                          h=tr(", including {a} of {b} high-confidence ones", ", त्यात {b} पैकी {a} उच्च खात्रीची",
                               a=hi["found"], b=hi["zones"]) if hi.get("zones") else "")))
    xt = data.crosstrack()
    if xt:
        pv = xt.get("p_value")
        exp = (xt.get("chance") or {}).get("confirmed")
        checks.append((f"{ui.fmt_num(xt['lift'] or 0, 0)}×", tr("Second NISAR orbit", "दुसरी निसार कक्षा"),
                       tr("better than chance: {c} of the {n} zones it covers were found again{e}{p}.",
                          "योगायोगापेक्षा चांगले: तिच्या दृष्टीतील {n} पैकी {c} क्षेत्रे पुन्हा सापडली{e}{p}.",
                          c=xt["confirmed"], n=xt["scored"],
                          e=tr(", chance gives {x}", ", योगायोगाने {x}", x=ui.fmt_num(exp * xt["scored"], 2))
                          if exp is not None else "",
                          p=f" (p ≈ {pv:.2f})" if pv is not None else "")))
    sh, so = v("validation.slide.hits"), v("validation.slide.observable")
    if so:
        rh = dc.get("reported_slide_hits") or {}
        zs = rh.get("main_hit_zones") or []
        note = []
        if len(zs) == 1 and sh and sh > 1:
            note.append(tr("both near one zone, {z}", "दोन्ही एकाच क्षेत्राजवळ, {z}", z=zs[0]))
        if rh and rh.get("nasadem", 0) < rh.get("main", 0):
            note.append(tr("none with NASADEM", "NASADEM सह एकही नाही") if not rh.get("nasadem") else
                        tr("{n} with NASADEM", "NASADEM सह {n}", n=rh["nasadem"]))
        checks.append((ui.t("x_of_y", x=sh, y=so), tr("Reported landslides", "नोंदवलेली भूस्खलने"),
                       tr("radar could see had a slide zone nearby", "जी रडारला दिसू शकत होती त्यांच्याजवळ भूस्खलन क्षेत्र होते")
                       + (": " + "; ".join(note) + "." if note else ".")))
    fh, fo = v("validation.flood.hits"), v("validation.flood.observable")
    if fo:
        fb = data.flood_baseline()
        luck = fb and min(fb["flat"]["prob_at_least_observed"], fb["settlements"]["prob_at_least_observed"]) >= 0.05
        checks.append((ui.t("x_of_y", x=fh, y=fo), tr("Reported floods", "नोंदवलेले पूर"),
                       tr("No better than chance ({e} of {n}): flooding between buildings hides from radar.",
                          "योगायोगापेक्षा जास्त नाही ({n} पैकी {e}): इमारतींमधील पूर रडारपासून लपतो.",
                          e=ui.fmt_num(fb["flat"]["expected_matches"], 1), n=fb["of"]) if luck else
                       tr("that radar could see had a detection nearby.", "जे रडारला दिसू शकत होते त्यांच्याजवळ शोध लागला.")))
    if sens:
        checks.append(("±1 dB", tr("Water threshold moved", "पाण्याची मर्यादा बदलली"),
                       tr("Reservoir rise: {a} to {b} km². Flooding: {c} to {d} km².",
                          "धरणांची वाढ: {a} ते {b} चौ. किमी. पूर: {c} ते {d} चौ. किमी.",
                          a=ui.fmt_num(sens["rise_km2"][0]), b=ui.fmt_num(sens["rise_km2"][1]),
                          c=ui.fmt_num(sens["flood_km2"][0], 2), d=ui.fmt_num(sens["flood_km2"][1], 1))))
    return checks


def render(rows=None):
    rows = items() if rows is None else rows
    st.markdown('<div class="ml-checkrow">' + "".join(
        f'<div class="ml-check"><div class="k">{html.escape(k)}</div><p class="t">{html.escape(t_)}</p>'
        f'<p>{html.escape(p)}</p></div>' for k, t_, p in rows) + "</div>", unsafe_allow_html=True)
