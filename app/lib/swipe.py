"""Before/after radar images cropped to the most changed part of the study area."""
from __future__ import annotations

import numpy as np
import streamlit as st
from PIL import Image

from . import data


def hotspot(size=520):
    return _hotspot(size, data.ver())


@st.cache_data(show_spinner=False)
def _hotspot(size, v):
    """Top-left pixel of the size x size window with the most new water + slide pixels."""
    nw = data.overlay_path("new_water")
    if not nw or not nw.exists():
        return None
    a = np.asarray(Image.open(nw).convert("RGBA"))[..., 3] > 0
    sl = data.overlay_path("slide_raster")
    if sl and sl.exists():
        a = a | (np.asarray(Image.open(sl).convert("RGBA"))[..., 3] > 0)
    s = 8  # coarse search
    small = a[: a.shape[0] // s * s, : a.shape[1] // s * s].reshape(a.shape[0] // s, s, a.shape[1] // s, s).sum((1, 3))
    k = size // s
    if small.shape[0] <= k or small.shape[1] <= k:
        return 0, 0
    cs = small.cumsum(0).cumsum(1)
    win = cs[k:, k:] - cs[:-k, k:] - cs[k:, :-k] + cs[:-k, :-k]
    r, c = np.unravel_index(np.argmax(win), win.shape)
    return int(r * s), int(c * s)


def pair(kind="hh", size=520, with_overlay=False):
    return _pair(kind, size, with_overlay, data.ver())


@st.cache_data(show_spinner=False)
def _pair(kind, size, with_overlay, v):
    """PIL images (before, after) for the swipe, same window."""
    hs = hotspot(size)
    out = []
    for when in ("before", "after"):
        p = data.overlay_path(f"{kind}_{when}")
        if not p or not p.exists():
            return None
        im = Image.open(p).convert("RGBA")
        if hs:
            r, c = hs
            im = im.crop((c, r, c + size, r + size))
        bg = Image.new("RGBA", im.size, (20, 26, 32, 255))
        bg.alpha_composite(im)
        if with_overlay and when == "after":
            ov = data.overlay_path("new_water")
            if ov and ov.exists():
                o = Image.open(ov).convert("RGBA")
                if hs:
                    o = o.crop((hs[1], hs[0], hs[1] + size, hs[0] + size))
                bg.alpha_composite(o)
        out.append(bg.convert("RGB").resize((size + size // 3, size + size // 3), Image.LANCZOS))
    return tuple(out)


def _b64(im, quality=82):
    import base64
    import io as _io
    buf = _io.BytesIO()
    im.save(buf, "WEBP", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def render(before_img, after_img, label_before, label_after, height=520, start=50):
    """Self-contained before/after slider (no external scripts). Drag, click, or use arrow keys."""
    import streamlit.components.v1 as components
    a, b = _b64(before_img), _b64(after_img)
    html = f"""
<div class="sw" id="sw" style="--pos:{start}%">
  <img src="data:image/webp;base64,{a}" alt="Radar image, {label_before}">
  <img class="top" src="data:image/webp;base64,{b}" alt="Radar image, {label_after}">
  <div class="bar"><div class="grip"></div></div>
  <span class="lab l">{label_before}</span><span class="lab r">{label_after}</span>
  <input type="range" min="0" max="100" value="{start}" aria-label="Compare {label_before} and {label_after}">
</div>
<style>
  body {{ margin:0; font-family:'IBM Plex Sans',system-ui,sans-serif; }}
  .sw {{ position:relative; width:100%; height:{height}px; overflow:hidden; border-radius:6px;
        background:#141a20; user-select:none; touch-action:none; cursor:ew-resize; }}
  .sw img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
  .sw .top {{ clip-path: inset(0 0 0 var(--pos)); }}
  .bar {{ position:absolute; top:0; bottom:0; left:var(--pos); width:2px; background:#fff; transform:translateX(-1px);
         box-shadow:0 0 0 1px rgba(0,0,0,.25); pointer-events:none; }}
  .grip {{ position:absolute; top:50%; left:50%; width:34px; height:34px; border-radius:50%; background:#fff;
          transform:translate(-50%,-50%); box-shadow:0 1px 4px rgba(0,0,0,.35); }}
  .grip::before, .grip::after {{ content:""; position:absolute; top:50%; border:6px solid transparent; transform:translateY(-50%); }}
  .grip::before {{ left:5px; border-right-color:#1d3346; }}
  .grip::after {{ right:5px; border-left-color:#1d3346; }}
  .lab {{ position:absolute; top:10px; padding:3px 8px; font-size:13px; font-weight:600; color:#1d3346;
         background:rgba(255,255,255,.88); border-radius:4px; pointer-events:none; }}
  .lab.l {{ left:10px; }} .lab.r {{ right:10px; }}
  .sw input {{ position:absolute; inset:auto 0 0 0; width:100%; opacity:0; height:100%; margin:0; cursor:ew-resize; }}
  .sw:focus-within {{ outline:3px solid #2a78d6; outline-offset:2px; }}
</style>
<script>
  const sw=document.getElementById('sw'), r=sw.querySelector('input');
  const set=v=>{{ sw.style.setProperty('--pos', v+'%'); r.value=v; }};
  r.addEventListener('input', e=>set(e.target.value));
</script>"""
    components.html(html, height=height + 6)
