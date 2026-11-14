"""Evidence cards: what NISAR saw at one finding, why it was flagged, and which checks it passed."""
from __future__ import annotations

import html

import streamlit as st

from . import data, ui

E = {
    "why_h": {"en": "Why the radar flagged it", "mr": "रडारने हे का निवडले"},
    "slope": {"en": "Steep ground: {s}° on average.", "mr": "तीव्र उतार: सरासरी {s}°."},
    "coh": {"en": "The ground stopped matching itself between passes: coherence {c}, {r}× its surrounding kilometre.",
            "mr": "दोन निरीक्षणांदरम्यान जमीन स्वतःशी जुळेनाशी झाली: कोहेरन्स {c}, आजूबाजूच्या एका किलोमीटरच्या {r} पट."},
    "hv": {"en": "HV fell {v} dB (vegetation stripped)", "mr": "HV {v} dB ने घटले (वनस्पती निघून गेली)"},
    "hh": {"en": "HH rose {v} dB (rough debris)", "mr": "HH {v} dB ने वाढले (खडबडीत ढिगारा)"},
    "bs": {"en": "Radar brightness changed: {x}.", "mr": "रडारची चमक बदलली: {x}."},
    "bs_rel": {"en": "Radar brightness changed more than the rest of the scene did.",
               "mr": "रडारची चमक बाकीच्या भागापेक्षा जास्त बदलली."},
    "and": {"en": " and ", "mr": " आणि "},
    "checks_h": {"en": "Extra checks", "mr": "अतिरिक्त तपासण्या"},
    "orbit": {"en": "Second NISAR orbit, 3 to 15 July", "mr": "दुसरी निसार कक्षा, ३ ते १५ जुलै"},
    "orbit_confirmed": {"en": "found it again", "mr": "पुन्हा सापडले"},
    "orbit_partial": {"en": "saw part of the evidence", "mr": "पुराव्याचा काही भाग दिसला"},
    "orbit_not seen": {"en": "did not see it", "mr": "दिसले नाही"},
    "orbit_not covered": {"en": "outside its view", "mr": "त्याच्या दृष्टीबाहेर"},
    "dem": {"en": "NASA's NASADEM elevation map", "mr": "नासाचा NASADEM उंची नकाशा"},
    "dem_found": {"en": "kept", "mr": "टिकले"},
    "dem_not": {"en": "not kept: {r}", "mr": "टिकले नाही: {r}"},
    "rep": {"en": "Reported event within 2 km", "mr": "२ किमीच्या आत नोंदवलेली घटना"},
    "rep_yes": {"en": "{place}, {km} km", "mr": "{place}, {km} किमी"},
    "rep_no": {"en": "none (nearest {km} km)", "mr": "नाही (सर्वात जवळची {km} किमी)"},
    "conf_high": {"en": "High confidence", "mr": "उच्च खात्री"},
    "conf_medium": {"en": "Medium confidence", "mr": "मध्यम खात्री"},
    "conf_low": {"en": "Low confidence", "mr": "कमी खात्री"},
    "maps": {"en": "Open in Google Maps", "mr": "गूगल मॅप्समध्ये उघडा"},
    "chip_before": {"en": "28 June", "mr": "२८ जून"},
    "chip_after": {"en": "10 July", "mr": "१० जुलै"},
    "chip_coh": {"en": "Coherence", "mr": "कोहेरन्स"},
    "chip_note": {"en": "1.9 km across, 40 m pixels. Radar colour: red HH, green HV, blue HH/HV. Coherence: dark = the "
                        "ground changed.",
                  "mr": "१.९ किमी रुंद, ४० मीटर चौकोन. रडार रंग: लाल HH, हिरवा HV, निळा HH/HV. कोहेरन्स: गडद = जमीन बदलली."},
    "flood_title": {"en": "Flood water", "mr": "पुराचे पाणी"},
    "flood_area": {"en": "{a} ha of water on 10 July, {d} dB darker than on 28 June, where no water was recorded "
                         "between 1984 and 2021.",
                   "mr": "१० जुलैला {a} हेक्टर पाणी, २८ जूनपेक्षा {d} dB गडद, जिथे १९८४ ते २०२१ दरम्यान पाणी नोंदवले नव्हते."},
    "flood_rep": {"en": "Nearest reported flood: {place}, {km} km.", "mr": "सर्वात जवळचा नोंदवलेला पूर: {place}, {km} किमी."},
    "lead": {"en": "A lead to check on the ground, not a confirmed landslide.",
             "mr": "जमिनीवर तपासण्याचा संकेत, निश्चित भूस्खलन नाही."},
}

REASON_MR = {"steeper than 45°": "४५° पेक्षा जास्त उतार", "gentler than 15°": "१५° पेक्षा कमी उतार",
             "radar layover or shadow": "रडारची सावली किंवा ले-ओव्हर",
             "near the edge of the slope band": "उताराच्या मर्यादेजवळ"}

TYPE_WORD = {"landslide": {"en": "landslide", "mr": "भूस्खलन"}, "flood": {"en": "flood", "mr": "पूर"},
             "river_overflow": {"en": "river overflow", "mr": "नदीला पूर"},
             "waterlogging": {"en": "waterlogging", "mr": "पाणी साचले"}}


def e(key: str, **kw) -> str:
    if ui.lang() == "de":
        from .i18n_de import DE_E
        s = DE_E.get(key) or E[key]["en"]
    else:
        s = E[key].get(ui.lang()) or E[key]["en"]
    return s.format(**kw) if kw else s


def _num(v, d=1):
    return f"{v:.{d}f}"


def why_slide(p: dict) -> list[str]:
    out = [e("slope", s=f"{p['slope_deg']:.0f}")]
    if p.get("coherence") is not None and p.get("coherence_vs_local") is not None:
        out.append(e("coh", c=_num(p["coherence"], 2), r=_num(p["coherence_vs_local"], 1)))
    th = data.metrics().get("thresholds", {})
    bits = []
    if p.get("hv_change_db") is not None and p["hv_change_db"] <= -th.get("slide_hv_drop_db", 2):
        bits.append(e("hv", v=_num(abs(p["hv_change_db"]))))
    if p.get("hh_change_db") is not None and p["hh_change_db"] >= th.get("slide_hh_rise_db", 3):
        bits.append(e("hh", v=_num(p["hh_change_db"])))
    out.append(e("bs", x=e("and").join(bits)) if bits else e("bs_rel"))
    return out


def checks(p: dict) -> list[tuple[str, bool | None, str]]:
    """(label, passed?, detail) for each extra check; passed None = could not be checked there."""
    out = []
    t = p.get("track106")
    if t:
        out.append((e("orbit"), True if t == "confirmed" else (None if t == "not covered" else False),
                    e(f"orbit_{t}") if f"orbit_{t}" in E else t))
    if "nasadem" in p:
        ok = p["nasadem"] == "found"
        reason = (p.get("nasadem_reason") or "").replace(" in NASADEM", "")
        if ui.lang() == "mr":
            reason = REASON_MR.get(reason, reason)
        elif ui.lang() == "de":
            from .i18n_de import REASON
            reason = REASON.get(reason, reason)
        out.append((e("dem"), ok, e("dem_found") if ok else e("dem_not", r=reason)))
    k = p.get("nearest_event_km")
    if k is not None:
        near = k <= 2.0
        kd = _num(k, 2 if 1.95 < k < 2.05 else 1)      # do not print "2.0 km" for a zone just outside 2 km
        out.append((e("rep"), near, e("rep_yes", place=p.get("nearest_event_place", ""), km=kd) if near
                    else e("rep_no", km=kd)))
    return out


def _badge(ok):
    if ok is True:
        return '<span class="ml-ck ok" aria-label="yes">✓</span>'
    if ok is False:
        return '<span class="ml-ck no" aria-label="no">✕</span>'
    return '<span class="ml-ck na" aria-label="not checked">–</span>'


def _chips(fid: str, kinds) -> str:
    figs = []
    for k in kinds:
        url = data.chip_url(fid, k)
        if not url:
            continue
        lbl = e(f"chip_{k}")
        figs.append(f'<figure><img src="{url}" alt="{html.escape(lbl)}: NISAR radar image of {fid}" loading="lazy" '
                    f'width="160" height="160"><figcaption>{html.escape(lbl)}</figcaption></figure>')
    return f'<div class="ml-chips">{"".join(figs)}</div>' if figs else ""


def maps_link(lat, lon) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={lat:.5f},{lon:.5f}"


def zone_card(p: dict, open_note=True) -> str:
    conf = p.get("confidence", "low")
    why = "".join(f"<li>{html.escape(w)}</li>" for w in why_slide(p))
    ck = "".join(f'<li>{_badge(ok)}<span><b>{html.escape(lbl)}</b>: {html.escape(det)}</span></li>'
                 for lbl, ok, det in checks(p))
    place = html.escape(p.get("near") or "")
    return (
        f'<article class="ml-card">'
        f'<header class="ml-card-head"><span class="ml-id">{p["id"]}</span><span class="ml-place">{place}</span>'
        f'<span class="ml-pill {conf}">{html.escape(e("conf_" + conf))} · {p["score"]:.2f}</span></header>'
        f'<div class="ml-card-body">{_chips(p["id"], ("before", "after", "coh"))}'
        f'<div class="ml-facts"><p class="ml-facts-h">{html.escape(e("why_h"))}</p><ul class="ml-why">{why}</ul>'
        f'<p class="ml-facts-h">{html.escape(e("checks_h"))}</p><ul class="ml-checks">{ck}</ul>'
        f'<p class="ml-links"><a href="{maps_link(p["lat"], p["lon"])}" target="_blank" rel="noopener">'
        f'{html.escape(e("maps"))}</a> · {p["lat"]:.5f}, {p["lon"]:.5f}</p></div></div>'
        + (f'<p class="ml-card-note">{html.escape(e("lead"))} {html.escape(e("chip_note"))}</p>' if open_note else "")
        + "</article>")


def flood_card(p: dict) -> str:
    rep = ""
    if p.get("nearest_event_km") is not None:
        rep = f'<p>{html.escape(e("flood_rep", place=p.get("nearest_event_place", ""), km=_num(p["nearest_event_km"])))}</p>'
    return (
        f'<article class="ml-card flood">'
        f'<header class="ml-card-head"><span class="ml-id">{p["id"]}</span><span class="ml-place">'
        f'{html.escape(e("flood_title"))}</span></header>'
        f'<div class="ml-card-body">{_chips(p["id"], ("before", "after"))}<div class="ml-facts">'
        f'<p>{html.escape(e("flood_area", a=_num(p["area_ha"]), d=_num(abs(p.get("drop_db", 0)))))}</p>{rep}'
        f'<p class="ml-links"><a href="{maps_link(p["lat"], p["lon"])}" target="_blank" rel="noopener">'
        f'{html.escape(e("maps"))}</a> · {p["lat"]:.5f}, {p["lon"]:.5f}</p></div></div></article>')


def show_zone(p: dict, **kw):
    st.markdown(zone_card(p, **kw), unsafe_allow_html=True)


def show_flood(p: dict):
    st.markdown(flood_card(p), unsafe_allow_html=True)


def type_word(t: str) -> str:
    if ui.lang() == "de":
        from .i18n_de import TYPE
        return TYPE.get(t) or t.replace("_", " ")
    return TYPE_WORD.get(t, {}).get(ui.lang()) or t.replace("_", " ")
