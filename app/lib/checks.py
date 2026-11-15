"""The four independent checks behind the numbers, as one summary band (Overview and Method pages)."""
from __future__ import annotations

import html

import streamlit as st

from . import data, ui


def items() -> list[tuple[str, str, str]]:
    """(headline number, check name, one-line result) for each check that has run."""
    tr, v, m = ui.tr, data.value, data.metrics()
    dc = m.get("dem_check") or {}
    sens = (m.get("sensitivity") or {}).get("range", {})
    checks = []
    fh, fo = v("validation.flood.hits"), v("validation.flood.observable")
    sh, so = v("validation.slide.hits"), v("validation.slide.observable")
    if fo:
        rh = dc.get("reported_slide_hits") or {}
        weak = rh and rh.get("nasadem", 0) < rh.get("main", 0)
        fb = data.flood_baseline()
        luck = fb and min(fb["flat"]["prob_at_least_observed"], fb["settlements"]["prob_at_least_observed"]) >= 0.05
        checks.append((ui.t("x_of_y", x=fh, y=fo), tr("Reported floods", "नोंदवलेले पूर"),
                       tr("that radar could see had a detection nearby. Landslides: {h} of {o}",
                          "जे रडारला दिसू शकत होते त्यांच्याजवळ शोध लागला. भूस्खलने: {o} पैकी {h}",
                          h=sh, o=so)
                       + (tr(", weak support.", ", कमकुवत आधार.") if weak else ".")
                       + (" " + tr("No better than chance: places nobody reported match {e} of {n}.",
                                   "योगायोगापेक्षा जास्त नाही: कोणीही न नोंदवलेली ठिकाणे {n} पैकी {e} वेळा जुळतात.",
                                   e=ui.fmt_num(fb["flat"]["expected_matches"], 1), n=fb["of"])
                          if luck else "")))
    xt = data.crosstrack()
    if xt:
        pv = xt.get("p_value")
        checks.append((ui.t("x_of_y", x=xt["confirmed"], y=xt["scored"]), tr("Second NISAR orbit", "दुसरी निसार कक्षा"),
                       tr("slide zones found again, {l}× more than chance{p}.",
                          "भूस्खलन क्षेत्रे पुन्हा सापडली, योगायोगापेक्षा {l}× जास्त{p}.",
                          l=ui.fmt_num(xt["lift"] or 0, 0), p=f" (p ≈ {pv:.2f})" if pv is not None else "")))
    if dc:
        checks.append((ui.t("x_of_y", x=dc["found"], y=dc["zones_main"]), tr("Second elevation map", "दुसरा उंची नकाशा"),
                       tr("slide zones kept with NASA's NASADEM elevation map.",
                          "नासाच्या NASADEM उंची नकाशासह टिकलेली भूस्खलन क्षेत्रे.")))
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
