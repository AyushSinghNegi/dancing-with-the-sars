"""The Overview hero: NISAR passes over Pune and its radar sweeps away the monsoon cloud.

The radar under the cloud is the real NISAR HH image of 10 July 2026 with the app's findings drawn on it. The cloud
is an illustration drawn in the browser (the satellite photos of those days showed only cloud; see the Story page).
One loop is about 12 seconds; it pauses off-screen, has a pause button, and is a still image for reduced motion.
"""
from __future__ import annotations

import base64
import html as _html
import io
import json

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from . import data, swipe, ui


def scene(size=520):
    return _scene(size, data.ver())


@st.cache_data(show_spinner=False)
def _scene(size, v):
    """WebP (base64) of the after-image crop with flood/new water and slide zones, plus share of slide pixels."""
    hs = swipe.hotspot(size)
    p = data.overlay_path("hh_after")
    if not p or not p.exists():
        return None
    def crop(im):
        return im.crop((hs[1], hs[0], hs[1] + size, hs[0] + size)) if hs else im
    base = Image.new("RGBA", (size, size), (14, 20, 30, 255))
    base.alpha_composite(crop(Image.open(p).convert("RGBA")).resize((size, size)))
    # Darker tone curve and a cool grade, so the radar reads as night-side instrument data, not snow, and the
    # blue water and orange slide zones stand out against it.
    arr = np.asarray(base).astype(np.float32)
    lum = arr[..., :3].mean(-1, keepdims=True) / 255.0
    lum = np.power(lum, 1.7) * 0.92
    arr[..., :3] = lum * np.array([205, 222, 240], np.float32) + np.array([8, 12, 22], np.float32)
    base = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")
    for name, rgb in (("rise", (109, 167, 236)), ("new_water", (61, 142, 240)), ("flood", (61, 142, 240)),
                      ("slide_raster", (240, 116, 58))):
        op = data.overlay_path(name)
        if not op or not op.exists():
            continue
        a = np.asarray(crop(Image.open(op).convert("RGBA")).resize((size, size), Image.NEAREST))[..., 3] > 0
        lay = np.zeros((size, size, 4), np.uint8)
        lay[a] = (*rgb, 235)
        base.alpha_composite(Image.fromarray(lay, "RGBA"))
    big = base.convert("RGB").resize((size * 3 // 2, size * 3 // 2), Image.LANCZOS)
    buf = io.BytesIO()
    big.save(buf, "WEBP", quality=84)
    # Where the findings sit in this crop (0-1 across and down), so the animation can ring them once revealed.
    pts = []
    bl = data.bounds().get("bounds_latlon")
    ref = data.overlay_path("new_water")
    if bl and ref and ref.exists():
        (s_, w_), (n_, e_) = bl
        ih, iw = Image.open(ref).size[::-1]
        r0, c0 = hs or (0, 0)
        def frac(lat, lon):
            return ((lon - w_) / (e_ - w_) * iw - c0) / size, ((n_ - lat) / (n_ - s_) * ih - r0) / size
        for z in data.zones():
            if z.get("confidence") in ("high", "medium"):
                fx, fy = frac(z["lat"], z["lon"])
                if 0.03 < fx < 0.97 and 0.03 < fy < 0.97:
                    pts.append([round(fx, 4), round(fy, 4), "s" if z["confidence"] == "high" else "m"])
        for f in data.flood_patches():
            fx, fy = frac(f["lat"], f["lon"])
            if 0.03 < fx < 0.97 and 0.03 < fy < 0.97:
                pts.append([round(fx, 4), round(fy, 4), "f"])
    return base64.b64encode(buf.getvalue()).decode(), pts


def render(after_iso: str, height=430):
    sc = scene()
    if not sc:
        return False
    b64, pts = sc
    tr = ui.tr
    lab_cloud = tr("Optical satellites, 3 to 8 July: only cloud", "प्रकाशीय उपग्रह, ३ ते ८ जुलै: फक्त ढग")
    lab_radar = tr("NISAR radar, {d}: sees the ground, new water in blue", "निसार रडार, {d}: जमीन दिसते, नवीन पाणी निळ्या रंगात",
                   d=ui.day(after_iso))
    lab_slide = tr("likely slide zones", "संभाव्य भूस्खलन क्षेत्रे")
    lab_note = tr("Cloud drawn as an illustration. Radar: real NISAR L-band image.",
                  "ढग हे चित्रण आहे. रडार: खरी निसार एल-बँड प्रतिमा.")
    lab_pause, lab_play = tr("Pause animation", "ॲनिमेशन थांबवा"), tr("Play animation", "ॲनिमेशन सुरू करा")
    alt = tr("Animation: the NISAR satellite passes over Pune and its radar sees through the monsoon cloud to the "
             "flood water and slide zones below.", "ॲनिमेशन: निसार उपग्रह पुण्यावरून जातो आणि त्याचे रडार ढगांतून "
             "खालचे पुराचे पाणी आणि भूस्खलन क्षेत्रे पाहते.")
    esc = _html.escape
    lab_cloud, lab_radar, lab_slide, lab_note, alt = map(esc, (lab_cloud, lab_radar, lab_slide, lab_note, alt))
    js_pause, js_play = json.dumps(lab_pause), json.dumps(lab_play)
    lab_pause = esc(lab_pause)
    page = f"""
<div class="hero" role="img" aria-label="{alt}">
  <img class="still" src="data:image/webp;base64,{b64}" alt="">
  <canvas id="c"></canvas>
  <div class="chip top" id="lc"><i class="d cloud"></i>{lab_cloud}</div>
  <div class="chip bot" id="lr"><i class="d water"></i>{lab_radar}<span class="sep"></span><i class="d slide"></i>{lab_slide}</div>
  <button id="pp" type="button" aria-label="{lab_pause}" title="{lab_pause}">
    <svg viewBox="0 0 24 24" width="16" height="16"><path id="ppi" d="M7 5h3v14H7zM14 5h3v14h-3z" fill="currentColor"/></svg>
  </button>
  <p class="note">{lab_note}</p>
</div>
<style>
  html, body {{ margin:0; background:transparent; font-family:'IBM Plex Sans', system-ui, sans-serif; }}
  .hero {{ position:relative; height:{height}px; border-radius:18px; overflow:hidden; background:#0b1220;
          box-shadow: 0 0 0 1px rgba(111,227,255,.22), 0 18px 50px rgba(0,0,0,.45); }}
  .hero canvas, .hero .still {{ position:absolute; inset:0; width:100%; height:100%; display:block; }}
  .hero .still {{ object-fit:cover; opacity:0; }}
  .chip {{ position:absolute; left:12px; right:auto; max-width:calc(100% - 70px); display:flex; align-items:center; gap:7px;
          flex-wrap:wrap; padding:5px 11px; border-radius:99px; font-size:12.5px; font-weight:600; line-height:1.35;
          color:#eaf2fb; background:rgba(7,12,23,.62); backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px);
          border:1px solid rgba(255,255,255,.14); transition:opacity .6s ease, transform .6s ease; }}
  .chip.top {{ top:12px; }} .chip.bot {{ bottom:34px; }}
  .chip.off {{ opacity:0; transform:translateY(4px); }}
  .d {{ width:9px; height:9px; border-radius:50%; flex:none; }}
  .d.cloud {{ background:#c9d3de; }} .d.water {{ background:#3d8ef0; box-shadow:0 0 8px #3d8ef0; }}
  .d.slide {{ background:#f0743a; box-shadow:0 0 8px #f0743a; }}
  .sep {{ width:4px; }}
  #pp {{ position:absolute; top:10px; right:10px; width:32px; height:32px; border-radius:50%; display:grid; place-items:center;
        color:#eaf2fb; background:rgba(7,12,23,.6); border:1px solid rgba(255,255,255,.2); cursor:pointer; padding:0; }}
  #pp:hover {{ background:rgba(20,40,70,.85); }}
  #pp:focus-visible {{ outline:3px solid #6fe3ff; outline-offset:2px; }}
  .hero::after {{ content:""; position:absolute; left:0; right:0; bottom:0; height:64px; pointer-events:none;
                 background:linear-gradient(180deg, rgba(7,12,23,0), rgba(7,12,23,.72)); }}
  .note {{ position:absolute; left:12px; bottom:8px; margin:0; font-size:11px; color:rgba(225,235,248,.8); z-index:2; }}
  .chip, #pp {{ z-index:2; }}
  @media (max-width: 480px) {{ .chip {{ font-size:11.5px; }} }}
</style>
<script>
(function () {{
  const cv = document.getElementById('c'), ctx = cv.getContext('2d');
  const still = document.querySelector('.still');
  const lc = document.getElementById('lc'), lr = document.getElementById('lr');
  const pp = document.getElementById('pp'), ppi = document.getElementById('ppi');
  const PTS = {json.dumps(pts)};
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const img = new Image();
  img.src = still.src;
  let W = 0, H = 0, dpr = 1, running = !reduce, visible = true, t0 = null, tPaused = 0, last = 0;

  // Tileable value noise, a few octaves: soft monsoon cloud (an illustration, not a satellite photo).
  const NW = 192, NH = 128;
  function noiseCanvas(seed) {{
    let s = seed;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const field = new Float32Array(NW * NH);
    for (const [cell, amp] of [[32, .55], [16, .27], [8, .13], [4, .05]]) {{
      const gx = NW / cell, gy = NH / cell, g = [];
      for (let i = 0; i < gx * gy; i++) g.push(rnd());
      for (let y = 0; y < NH; y++) for (let x = 0; x < NW; x++) {{
        const fx = x / cell, fy = y / cell, x0 = Math.floor(fx), y0 = Math.floor(fy);
        const sx = (fx - x0) * (fx - x0) * (3 - 2 * (fx - x0)), sy = (fy - y0) * (fy - y0) * (3 - 2 * (fy - y0));
        const v = (i, j) => g[((j % gy) * gx) + (i % gx)];
        const a = v(x0, y0) + (v(x0 + 1, y0) - v(x0, y0)) * sx, b = v(x0, y0 + 1) + (v(x0 + 1, y0 + 1) - v(x0, y0 + 1)) * sx;
        field[y * NW + x] += amp * (a + (b - a) * sy);
      }}
    }}
    const c = document.createElement('canvas'); c.width = NW; c.height = NH;
    const id = c.getContext('2d').createImageData(NW, NH);
    for (let i = 0; i < NW * NH; i++) {{
      const v = Math.min(1, Math.max(0, (field[i] - .26) * 2.3));
      const shade = 104 + 140 * Math.pow(v, 1.3);
      id.data[i * 4] = shade; id.data[i * 4 + 1] = shade + 6; id.data[i * 4 + 2] = shade + 16;
      id.data[i * 4 + 3] = 255 * Math.min(1, .72 + v * .4);
    }}
    c.getContext('2d').putImageData(id, 0, 0);
    return c;
  }}
  const clouds = [noiseCanvas(7), noiseCanvas(91)];
  const layer = document.createElement('canvas'), lctx = layer.getContext('2d');

  function size() {{
    const r = cv.getBoundingClientRect();
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    layer.width = W; layer.height = H;
  }}

  function cover(c, w, h) {{             // draw an image to fill w x h, centred, keeping its aspect
    const s = Math.max(w / img.width, h / img.height), iw = img.width * s, ih = img.height * s;
    c.drawImage(img, (w - iw) / 2, (h - ih) / 2, iw, ih);
    return [(w - iw) / 2, (h - ih) / 2, iw, ih];
  }}
  let box = [0, 0, 1, 1];

  function rings(t, scanY, fade) {{     // the app's findings, ringed once the radar has revealed them
    for (const [fx, fy, k] of PTS) {{
      const x = box[0] + fx * box[2], y = box[1] + fy * box[3];
      if (y > scanY - 8 || x < 4 || x > W - 4 || y < 4 || y > H - 4) continue;
      const age = Math.min(1, (scanY - y) / 120), ph = (t * 1.3 + fx * 7 + fy * 5) % 1;
      const col = k === 'f' ? '61,142,240' : '240,116,58';
      ctx.globalAlpha = fade * age;
      ctx.strokeStyle = 'rgba(' + col + ',' + (1 - ph) + ')'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(x, y, 5 + ph * 16, 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = 'rgb(' + col + ')'; ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(x, y, k === 'm' ? 3.2 : 4.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.globalAlpha = 1;
    }}
  }}

  function drawCloud(t, alpha) {{
    lctx.clearRect(0, 0, W, H);
    lctx.globalCompositeOperation = 'source-over';
    lctx.imageSmoothingEnabled = true;
    const sc = Math.max(W / NW, H / NH) * 1.25;
    for (let k = 0; k < 2; k++) {{
      const cw = NW * sc * (k ? 1.4 : 1), ch = NH * sc * (k ? 1.4 : 1);
      const off = ((t * (k ? 9 : 14)) % cw);
      lctx.globalAlpha = k ? .55 : 1;
      for (let x = -off; x < W; x += cw) for (let y = -ch * .1; y < H; y += ch) lctx.drawImage(clouds[k], x, y, cw, ch);
    }}
    lctx.globalAlpha = 1;
    // a darker monsoon underside
    const g = lctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, 'rgba(60,72,90,.0)'); g.addColorStop(1, 'rgba(40,50,66,.38)');
    lctx.fillStyle = g; lctx.fillRect(0, 0, W, H);
    return alpha;
  }}

  // Timeline of one loop (seconds).
  const T_IN = 1.4, T_SCAN = 5.2, T_HOLD = 3.4, T_BACK = 2.0, LOOP = T_IN + T_SCAN + T_HOLD + T_BACK;
  const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;

  function frame(t) {{
    const lt = t % LOOP;
    let scanY, cloudBack = 0, satY, satA = 1;
    if (lt < T_IN) {{ scanY = 0; satY = -40 + 40 * (lt / T_IN); }}
    else if (lt < T_IN + T_SCAN) {{ const p = ease((lt - T_IN) / T_SCAN); scanY = p * (H + 30); satY = scanY; }}
    else if (lt < T_IN + T_SCAN + T_HOLD) {{ scanY = H + 30; satY = H + 30 + (lt - T_IN - T_SCAN) * 40; satA = 0; }}
    else {{ scanY = H + 30; cloudBack = ease((lt - T_IN - T_SCAN - T_HOLD) / T_BACK); satA = 0; satY = -60; }}

    ctx.clearRect(0, 0, W, H);
    if (img.complete && img.width) box = cover(ctx, W, H);
    rings(t, scanY, 1 - cloudBack);

    // cloud layer, erased above the scan line with a soft edge
    drawCloud(t);
    lctx.globalCompositeOperation = 'destination-out';
    const edge = 46;
    const g = lctx.createLinearGradient(0, scanY - edge, 0, scanY);
    g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    lctx.fillStyle = 'rgba(0,0,0,1)';
    if (scanY - edge > 0) lctx.fillRect(0, 0, W, scanY - edge);
    lctx.fillStyle = g; lctx.fillRect(0, scanY - edge, W, edge);
    lctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = cloudBack > 0 ? cloudBack : 1;
    if (cloudBack > 0) {{ drawCloud(t); }}
    ctx.drawImage(layer, 0, 0, W, H);
    ctx.globalAlpha = 1;

    // radar beam: NISAR looks to the side, so the swath sits beside the ground track
    if (satA > 0 && scanY > -10 && scanY < H + 10) {{
      const sx = 30, sy = Math.max(14, satY - 2);
      const bg = ctx.createLinearGradient(sx, 0, W, 0);
      bg.addColorStop(0, 'rgba(111,227,255,.0)'); bg.addColorStop(.25, 'rgba(111,227,255,.20)'); bg.addColorStop(1, 'rgba(111,227,255,.06)');
      ctx.fillStyle = bg;
      ctx.beginPath(); ctx.moveTo(sx + 10, sy); ctx.lineTo(W, scanY - 16); ctx.lineTo(W, scanY + 4); ctx.closePath(); ctx.fill();
      ctx.shadowColor = '#6fe3ff'; ctx.shadowBlur = 14;
      ctx.strokeStyle = 'rgba(160,240,255,.95)'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(56, scanY); ctx.lineTo(W, scanY); ctx.stroke();
      ctx.shadowBlur = 0;
      drawSat(sx, sy, t);
    }} else if (satA > 0 && lt < T_IN) {{ drawSat(30, satY, t); }}
    if (lt >= T_IN + T_SCAN * .55 && lt < T_IN + T_SCAN + T_HOLD + T_BACK * .4) {{ lc.classList.add('off'); lr.classList.remove('off'); }}
    else {{ lc.classList.remove('off'); lr.classList.add('off'); }}
  }}

  function drawSat(x, y, t) {{       // top view: bus, solar wing, and the large mesh reflector on its boom
    ctx.save(); ctx.translate(x, y);
    ctx.fillStyle = '#e9eef5'; ctx.fillRect(-5, -7, 10, 14);
    ctx.fillStyle = '#2b5fa8'; ctx.fillRect(-21, -4, 14, 8); ctx.strokeStyle = '#9ec3ff'; ctx.lineWidth = .8;
    ctx.strokeRect(-21, -4, 14, 8);
    ctx.strokeStyle = '#dfe7f1'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(5, 0); ctx.lineTo(15, 0); ctx.stroke();
    ctx.fillStyle = 'rgba(232,201,120,.95)'; ctx.beginPath(); ctx.ellipse(21, 0, 7, 9, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(255,240,200,.8)'; ctx.stroke();
    ctx.fillStyle = 'rgba(111,227,255,' + (.5 + .5 * Math.sin(t * 6)) + ')';
    ctx.beginPath(); ctx.arc(0, -10, 2, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }}

  function loop(now) {{
    if (!running || !visible) {{ last = now; requestAnimationFrame(loop); return; }}
    if (t0 === null) t0 = now;
    if (last && now - last > 200) t0 += now - last;     // tab came back: continue, don't jump
    last = now;
    frame((now - t0) / 1000);
    requestAnimationFrame(loop);
  }}

  function showStill() {{
    ctx.clearRect(0, 0, W, H); if (img.width) box = cover(ctx, W, H);
    rings(0.35, H + 200, 1); lc.classList.add('off'); lr.classList.remove('off');
  }}
  img.onload = () => {{ size(); if (reduce) showStill(); else frame(0); }};
  window.addEventListener('resize', () => {{ size(); if (!running) showStill(); }});
  new IntersectionObserver(es => {{ visible = es[0].isIntersecting; }}).observe(cv);
  document.addEventListener('visibilitychange', () => {{ visible = !document.hidden; }});
  function setBtn() {{
    ppi.setAttribute('d', running ? 'M7 5h3v14H7zM14 5h3v14h-3z' : 'M8 5l11 7-11 7z');
    pp.setAttribute('aria-label', running ? {js_pause} : {js_play});
    pp.title = pp.getAttribute('aria-label');
  }}
  pp.addEventListener('click', () => {{ running = !running; if (!running) showStill(); setBtn(); }});
  setBtn();
  requestAnimationFrame(loop);
}})();
</script>
"""
    components.html(page, height=height + 4)
    return True
