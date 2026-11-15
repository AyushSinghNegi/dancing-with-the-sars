"""App-wide guided tour: one card at a time, across all six pages, pointing at the control it explains.

How it works: while the tour runs, every page renders three hidden Streamlit buttons (next, back, close) inside a
container keyed "tourctl", plus a small script. The script draws a spotlight and a card in the page itself; the
card's buttons click the hidden ones, so Python keeps the step and moves between pages. When the tour ends the
container is gone, and the card removes itself on its next frame.
"""
from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

from . import ui

PATHS = {"": "home.py", "story": "views/1_Story.py", "explore": "views/2_Explore.py", "place": "views/4_Place.py",
         "field": "views/5_Field.py", "method": "views/3_Method.py"}


def steps():
    tr = ui.tr
    return [
        ("", "", tr("Welcome to MonsoonLens", "MonsoonLens मध्ये स्वागत"),
         tr("In July 2026 cloud hid Pune from ordinary satellites. This app shows what NISAR's radar saw through it: "
            "new water, flooding and likely landslide zones.",
            "जुलै २०२६ मध्ये ढगांनी पुणे सामान्य उपग्रहांपासून लपवले. निसारच्या रडारने ढगांतून काय पाहिले ते हे ॲप दाखवते: नवीन "
            "पाणी, पूर आणि संभाव्य भूस्खलन क्षेत्रे.")),
        ("", '[data-testid="stSidebarNav"]', tr("Six pages", "सहा पाने"),
         tr("Move between pages here. On a phone, open this menu with the arrow at the top left.",
            "इथून पानांमध्ये जा. फोनवर हा मेनू वर डावीकडील बाणाने उघडा.")),
        ("", ".st-key-lang_choice", tr("Your language", "तुमची भाषा"),
         tr("Read everything in English, Marathi or German.", "सर्व काही इंग्रजी, मराठी किंवा जर्मनमध्ये वाचा.")),
        ("", ".st-key-tour_3d", tr("See it in 3D", "३D मध्ये पाहा"),
         tr("Drag to turn the land. Press “Fly over the findings” for a one-minute flight to each one.",
            "जमीन फिरवण्यासाठी ओढा. प्रत्येक निष्कर्षावरून एका मिनिटाच्या उड्डाणासाठी “निष्कर्षांवरून उडा” दाबा.")),
        ("", ".st-key-tour_found", tr("The headline numbers", "मुख्य आकडे"),
         tr("What the radar found. Each card says how sure we are.",
            "रडारला काय सापडले. प्रत्येक कार्ड आम्हाला किती खात्री आहे ते सांगते.")),
        ("", ".st-key-tour_checks", tr("How we checked it", "आम्ही कसे तपासले"),
         tr("Every result is tested, and we show the tests that came out weak too.",
            "प्रत्येक निकाल तपासला आहे, आणि कमकुवत ठरलेल्या तपासण्याही आम्ही दाखवतो.")),
        ("story", ".st-key-rail", tr("The story", "कथा"),
         tr("Six short chapters, from the rain to what radar could not see. Click a stop, or use the ← and → keys.",
            "पावसापासून रडारला काय दिसले नाही इथपर्यंत सहा छोटी प्रकरणे. एखाद्या थांब्यावर क्लिक करा, किंवा ← आणि → कळा वापरा.")),
        ("explore", ".st-key-explore_mode", tr("Explore the map", "नकाशा पाहा"),
         tr("Choose the 3D view, the flat map with radar evidence for each zone, or water through the season.",
            "३D दृश्य, प्रत्येक क्षेत्राच्या रडार पुराव्यासह सपाट नकाशा, किंवा हंगामातील पाणी निवडा.")),
        ("place", ".st-key-tour_place", tr("Check a place", "एखादे ठिकाण तपासा"),
         tr("Type your village or town to see what was found within 2, 5 or 10 km. Share the page link with others.",
            "२, ५ किंवा १० किमीच्या आत काय सापडले ते पाहण्यासाठी तुमचे गाव किंवा शहर टाइप करा. पानाची लिंक इतरांना पाठवा.")),
        ("field", ".st-key-tour_downloads", tr("For district teams", "जिल्हा पथकांसाठी"),
         tr("Print the ranked list with radar images, or open it on a phone in Google Earth (KML), and go and check.",
            "रडार प्रतिमांसह क्रमवार यादी छापा, किंवा फोनवर गूगल अर्थमध्ये (KML) उघडा, आणि जाऊन तपासा.")),
        ("method", ".ml-toc", tr("How every number was made", "प्रत्येक आकडा कसा तयार झाला"),
         tr("The NISAR files, each step of the method, every check and the limits, for researchers and journalists.",
            "निसार फाइली, पद्धतीची प्रत्येक पायरी, प्रत्येक तपासणी आणि मर्यादा, संशोधक आणि पत्रकारांसाठी.")),
        ("method", "", tr("You are ready", "तुम्ही तयार आहात"),
         tr("Start with the story, or check your own village. You can take this tour again from the menu.",
            "कथेने सुरुवात करा, किंवा तुमचे स्वतःचे गाव तपासा. हा फेरफटका मेनूमधून पुन्हा घेता येईल.")),
    ]


def start():
    st.session_state.update(tour_on=True, tour_i=0, tour_jump=True)


def _move(d):
    ss = st.session_state
    ss.tour_i = ss.get("tour_i", 0) + d
    if not 0 <= ss.tour_i < len(steps()):
        ss.tour_on = False
    ss.tour_jump = True


def _end():
    st.session_state.tour_on = False


def run(page: str):
    """Call from every page's setup. Draws the current step, or moves to the page it belongs to."""
    ss = st.session_state
    if not ss.get("tour_on"):
        return
    S = steps()
    i = min(ss.get("tour_i", 0), len(S) - 1)
    pg, sel, title, text = S[i]
    if pg != page:
        if ss.pop("tour_jump", False):
            st.switch_page(PATHS[pg])
        ss.tour_on = False            # the visitor left the tour's page on their own: stop quietly
        return
    ss.tour_jump = False
    with st.container(key="tourctl"):
        st.button("next", key="tour_next", on_click=_move, args=(1,))
        st.button("back", key="tour_back", on_click=_move, args=(-1,))
        st.button("end", key="tour_end", on_click=_end)
        cfg = dict(sel=sel, title=title, text=text, i=i + 1, n=len(S), last=i == len(S) - 1,
                   L=dict(next=ui.tr("Next", "पुढे"), back=ui.tr("Back", "मागे"), finish=ui.tr("Finish", "पूर्ण"),
                          close=ui.tr("Close the tour", "फेरफटका बंद करा"),
                          of=ui.tr("{i} of {n}", "{n} पैकी {i}", i=i + 1, n=len(S))))
        components.html(_JS.replace("__CFG__", json.dumps(cfg, ensure_ascii=False)), height=0)


_JS = r"""<script>
(function () {
  const C = __CFG__;
  const w = window.parent, d = w.document;
  // Run in the page itself, so the card outlives this little frame.
  const old = d.getElementById('ml-tour-js'); if (old) old.remove();
  const s = d.createElement('script'); s.id = 'ml-tour-js';
  s.textContent = '(' + main.toString() + ')(' + JSON.stringify(C) + ');';
  d.head.appendChild(s);

  function main(C) {
    const d = document, token = Math.random();
    window.__mlTour = token;
    if (!d.getElementById('ml-tour-css')) {
      const st = d.createElement('style'); st.id = 'ml-tour-css';
      st.textContent = `
        #ml-tour .spot { position: fixed; z-index: 1000000; pointer-events: none; border-radius: 16px;
          box-shadow: 0 0 0 4px rgba(111,227,255,.9), 0 0 0 9999px rgba(4,9,20,.58); transition: all .35s cubic-bezier(.2,.7,.2,1); }
        #ml-tour .dim { position: fixed; inset: 0; z-index: 999999; background: rgba(4,9,20,.58); pointer-events: none; }
        #ml-tour .card { position: fixed; z-index: 1000001; width: min(360px, calc(100vw - 24px)); padding: 16px 18px 14px;
          border-radius: 16px; background: #0b1630; color: #e8eef7; border: 1px solid rgba(111,227,255,.35);
          box-shadow: 0 18px 50px rgba(0,0,0,.45); font: 14px/1.5 'IBM Plex Sans', system-ui, sans-serif;
          transition: top .35s cubic-bezier(.2,.7,.2,1), left .35s cubic-bezier(.2,.7,.2,1); animation: mlTourIn .35s ease both; }
        #ml-tour .card .k { font-size: 12px; color: #9fe9ff; font-weight: 600; margin: 0 0 4px; }
        #ml-tour .card h4 { margin: 0 0 6px; font: 600 18px 'IBM Plex Sans Condensed', 'IBM Plex Sans', sans-serif; color: #fff; }
        #ml-tour .card p.t { margin: 0 0 12px; color: #d3deec; }
        #ml-tour .row { display: flex; gap: 8px; align-items: center; }
        #ml-tour .row .sp { flex: 1; }
        #ml-tour button { font: 600 13px 'IBM Plex Sans', system-ui, sans-serif; padding: 7px 14px; border-radius: 99px;
          cursor: pointer; border: 1px solid rgba(255,255,255,.25); background: transparent; color: #e8eef7; }
        #ml-tour button.primary { background: #3d8ef0; border-color: #3d8ef0; color: #fff; }
        #ml-tour button.x { border: none; padding: 4px 6px; color: #a9bdd8; text-decoration: underline; font-weight: 500; }
        #ml-tour button:disabled { opacity: .4; cursor: default; }
        #ml-tour button:focus-visible { outline: 3px solid #6fe3ff; outline-offset: 2px; }
        @keyframes mlTourIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
        @media (prefers-reduced-motion: reduce) { #ml-tour .spot, #ml-tour .card { transition: none; animation: none; } }`;
      d.head.appendChild(st);
    }
    let root = d.getElementById('ml-tour');
    if (!root) { root = d.createElement('div'); root.id = 'ml-tour'; d.body.appendChild(root); }
    const esc = x => String(x).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
    root.innerHTML = '<div class="dim" hidden></div><div class="spot" hidden></div>' +
      '<div class="card" role="dialog" aria-modal="false" aria-labelledby="ml-tour-h"><p class="k">' + esc(C.L.of) + '</p>' +
      '<h4 id="ml-tour-h">' + esc(C.title) + '</h4><p class="t">' + esc(C.text) + '</p><div class="row">' +
      '<button type="button" class="b"' + (C.i === 1 ? ' disabled' : '') + '>' + esc(C.L.back) + '</button>' +
      '<button type="button" class="n primary">' + esc(C.last ? C.L.finish : C.L.next) + '</button>' +
      '<span class="sp"></span><button type="button" class="x">' + esc(C.L.close) + '</button></div></div>';
    const spot = root.querySelector('.spot'), dim = root.querySelector('.dim'), card = root.querySelector('.card');
    const press = k => { const b = d.querySelector('.st-key-tour_' + k + ' button'); if (b) b.click(); };
    root.querySelector('.b').onclick = () => press('back');
    root.querySelector('.n').onclick = () => press(C.last ? 'end' : 'next');
    root.querySelector('.x').onclick = () => press('end');
    const onKey = e => { if (e.key === 'Escape' && window.__mlTour === token) press('end'); };
    d.addEventListener('keydown', onKey);
    setTimeout(() => { try { root.querySelector('.n').focus({preventScroll: true}); } catch (e) {} }, 400);

    // On a phone the sidebar is an overlay: open it for steps that point into it, close it for the rest.
    const sb = d.querySelector('[data-testid="stSidebar"]');
    const tgt0 = C.sel ? d.querySelector(C.sel) : null;
    if (window.innerWidth < 760 && sb) {
      const r0 = sb.getBoundingClientRect(), open = r0.width > 80 && r0.right > 80, inSb = !!(tgt0 && sb.contains(tgt0));
      if (inSb && !open) { const e = d.querySelector('[data-testid="stExpandSidebarButton"]'); if (e) e.click(); }
      if (!inSb && open) {
        const c = d.querySelector('[data-testid="stSidebarCollapseButton"]'), b = c && (c.querySelector('button') || c);
        if (b) b.click();
      }
    }
    const t0 = performance.now(); let scrolled = false;
    function frame() {
      if (window.__mlTour !== token) { d.removeEventListener('keydown', onKey); return; }
      if (!d.querySelector('.st-key-tourctl')) { root.remove(); d.removeEventListener('keydown', onKey); return; }
      const el = C.sel ? d.querySelector(C.sel) : null;
      let r = el ? el.getBoundingClientRect() : null;
      const W = window.innerWidth, H = window.innerHeight;
      const ok = r && r.width > 4 && r.height > 4 && r.right > 0 && r.left < W;
      const cw = card.offsetWidth, ch = card.offsetHeight;
      if (ok && !scrolled) {
        scrolled = true;
        // Bring the target and the card below it into view together; tall targets go to the top.
        if (r.top < 56 || r.bottom + ch + 24 > H) {
          let p = el.parentElement;
          while (p && p !== d.body) {
            const o = getComputedStyle(p).overflowY;
            if ((o === 'auto' || o === 'scroll') && p.scrollHeight > p.clientHeight + 4) break;
            p = p.parentElement;
          }
          const want = r.height + ch + 24 <= H - 64 ? Math.max(64, (H - r.height - ch - 12) / 2) : 64;
          (p && p !== d.body ? p : (d.scrollingElement || d.documentElement)).scrollBy({top: r.top - want, behavior: 'smooth'});
        }
      }
      if (ok) {
        const pad = 8, top = Math.max(r.top - pad, 4), left = Math.max(r.left - pad, 4);
        const bottom = Math.min(r.bottom + pad, H - 4), right = Math.min(r.right + pad, W - 4);
        spot.hidden = false; dim.hidden = true;
        Object.assign(spot.style, {top: top + 'px', left: left + 'px', width: (right - left) + 'px', height: (bottom - top) + 'px'});
        let y = bottom + 12;
        if (y + ch > H - 8) y = top - ch - 12;
        if (y < 8) y = Math.max(8, H - ch - 12);
        const x = Math.min(Math.max(8, left), W - cw - 8);
        card.style.top = y + 'px'; card.style.left = x + 'px';
      } else if (!C.sel || performance.now() - t0 > 2500) {
        spot.hidden = true; dim.hidden = false;
        card.style.top = Math.max(8, (H - ch) / 2) + 'px'; card.style.left = Math.max(8, (W - cw) / 2) + 'px';
      } else {
        card.style.top = Math.max(8, (H - ch) / 2) + 'px'; card.style.left = Math.max(8, (W - cw) / 2) + 'px';
      }
      requestAnimationFrame(frame);
    }
    frame();
  }
})();
</script>"""
