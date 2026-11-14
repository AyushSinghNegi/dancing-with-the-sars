"""Look, language and shared pieces of the MonsoonLens app."""
from __future__ import annotations

import html

import streamlit as st

from . import data

INK = "#1d3346"       # map ink (the map has its own light/dark styling); page text follows the theme
MUTED = "#5d6b75"
RADAR = "#7d878f"
PAPER = "#f4f6f5"
LINE = "#d9dedd"
COLORS = {"new_water": "#3d8ef0", "flood": "#2f6fd0", "rise": "#6da7ec", "slide_zones": "#f0743a", "brighter": "#1baf7a",
          "permanent": "#9cc3f2"}
SPACE = "#070c17"     # night sky behind the hero, in both themes

# Page styling works in Streamlit's light AND dark theme (.streamlit/config.toml): text inherits the theme's
# colour, neutrals are translucent, and accents are mid-tone data colours that read on both.
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans+Devanagari:wght@400;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');
:root {
  --ml-line: rgba(128, 146, 172, .26);
  --ml-panel: rgba(128, 150, 182, .07);
  --ml-panel-2: rgba(128, 150, 182, .13);
  --ml-water: #3d8ef0; --ml-flood: #2f6fd0; --ml-slide: #f0743a; --ml-beam: #6fe3ff;
  --ml-space: #070c17; --ml-space-2: #0d1830;
  --ml-shadow: 0 1px 2px rgba(5, 12, 30, .06), 0 8px 24px rgba(5, 12, 30, .07);
}
html, body, .stApp, .stMarkdown, button, input, textarea, select, label, p, li, td, th {
  font-family: 'IBM Plex Sans', 'IBM Plex Sans Devanagari', system-ui, sans-serif;
}
[data-testid="stIconMaterial"], .material-symbols-rounded { font-family: 'Material Symbols Rounded' !important; }
.block-container { padding-top: 3.8rem; max-width: 1200px; }
h1, h2, h3, .ml-display {
  font-family: 'IBM Plex Sans Condensed', 'IBM Plex Sans Devanagari', sans-serif; letter-spacing: -0.01em;
}
h1 { font-size: 2.6rem; line-height: 1.05; font-weight: 700; }
h2 { font-size: 1.75rem; line-height: 1.15; font-weight: 700; margin-top: 1.8rem; }
h3 { font-size: 1.2rem; font-weight: 600; }
p, li { font-size: 1.02rem; line-height: 1.6; max-width: 74ch; }
.ml-muted, .ml-source, .ml-dates, .ml-step, .ml-kicker, .ml-pathd, .ml-place, .ml-card-note, .ml-links,
.ml-stat .sure, .ml-chips figcaption, [data-testid="stCaptionContainer"] {
  color: color-mix(in srgb, currentColor 70%, transparent) !important;
}
.ml-lede { font-size: 1.16rem; line-height: 1.6; max-width: 62ch; }
.ml-muted { font-size: 0.93rem; }
.ml-dates { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; font-size: 1.05rem; margin-bottom: 1.1rem; }
.ml-step, .ml-kicker { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; font-size: 1rem; margin: 0; }
.ml-source { font-size: 0.82rem; } .ml-source a { color: inherit; }
.ml-note { border-left: 3px solid currentColor; padding: 0.2rem 0 0.2rem 0.9rem; margin: 0.8rem 0; }
.ml-banner { background: #fff4d6; border: 1px solid #e9c46a; color: #5a4300; padding: 0.7rem 1rem;
  border-radius: 8px; font-size: 0.95rem; margin-bottom: 1rem; }
.stButton > button, .stLinkButton > a, .stPageLink a { border-radius: 10px; transition: transform .15s ease, box-shadow .15s ease; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: var(--ml-shadow); }
:focus-visible { outline: 3px solid var(--ml-water) !important; outline-offset: 2px; }
iframe[title="streamlit_folium.st_folium"] { border-radius: 14px; box-shadow: var(--ml-shadow); }

/* sidebar */
[data-testid="stSidebar"] .ml-brand-sub { font-size: .82rem; line-height: 1.4; margin: .2rem 0 .6rem;
  color: color-mix(in srgb, currentColor 65%, transparent); }
[data-testid="stLogo"] { height: 2.6rem !important; max-width: 15rem !important; }

/* hero: a night-sky panel in both themes */
.st-key-hero { position: relative; overflow: hidden; border-radius: 22px; padding: 2.2rem 2.2rem 2.6rem 2.4rem;
  background: radial-gradient(1200px 500px at 85% -10%, #16305c 0%, rgba(22,48,92,0) 60%),
              radial-gradient(800px 400px at 0% 110%, #1b1f4a 0%, rgba(27,31,74,0) 55%),
              linear-gradient(180deg, #070c17 0%, #0b1426 100%);
  color: #e8eef7; box-shadow: 0 20px 60px rgba(4, 10, 25, .35); margin-bottom: .6rem; }
.st-key-hero::before { content: ""; position: absolute; inset: -50%; pointer-events: none; opacity: .75;
  background-image:
    radial-gradient(1px 1px at 20px 30px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 120px 80px, #cfe3ff 50%, transparent 51%),
    radial-gradient(1.5px 1.5px at 200px 160px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 330px 50px, #fff 50%, transparent 51%),
    radial-gradient(1px 1px at 420px 210px, #bcd6ff 50%, transparent 51%), radial-gradient(1.2px 1.2px at 520px 120px, #fff 50%, transparent 51%),
    radial-gradient(1px 1px at 610px 260px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 70px 240px, #dbe8ff 50%, transparent 51%);
  background-size: 640px 300px; animation: ml-drift 140s linear infinite; }
@keyframes ml-drift { from { transform: translate3d(0, 0, 0); } to { transform: translate3d(-640px, 300px, 0); } }
.st-key-hero::after, .ml-band::after {   /* Earth's limb, lit by a thin band of atmosphere */
  content: ""; position: absolute; left: -18%; right: -18%; height: 640px; bottom: -604px; border-radius: 50%;
  pointer-events: none; z-index: 0;
  background: radial-gradient(ellipse 60% 22% at 50% 2%, #2f7fd6 0%, #164a8c 30%, #0b2348 62%, #070c17 100%);
  box-shadow: 0 -1px 0 rgba(160, 235, 255, .75), 0 -5px 16px rgba(90, 180, 255, .45), 0 -22px 60px rgba(61, 142, 240, .22); }
.st-key-hero > div { position: relative; z-index: 1; }
.st-key-hero h1, .st-key-hero p, .st-key-hero .ml-dates, .st-key-hero .ml-kicker { color: #e8eef7 !important; }
.st-key-hero .ml-dates, .st-key-hero .ml-kicker { color: #9fb7d8 !important; }
.st-key-hero .ml-kicker { display: inline-flex; width: max-content; max-width: 100%; gap: .5rem; align-items: center; background: rgba(111, 227, 255, .10);
  border: 1px solid rgba(111, 227, 255, .28); padding: .25rem .75rem; border-radius: 99px; font-size: .9rem; margin-bottom: .9rem; }
.st-key-hero .ml-kicker i { width: .5rem; height: .5rem; border-radius: 50%; background: var(--ml-beam);
  box-shadow: 0 0 10px var(--ml-beam); animation: ml-blink 2.4s ease-in-out infinite; }
@keyframes ml-blink { 50% { opacity: .35; } }
.ml-hero { font-size: clamp(2.1rem, 3.4vw, 3.5rem); line-height: 1.02; font-weight: 700; margin: 0 0 .7rem 0;
  text-wrap: balance; color: #f2f6fc !important; }
.st-key-herobtns { gap: .55rem !important; }
.st-key-hero .stButton > button { border-radius: 99px; padding: .3rem .85rem !important; min-height: 2.3rem !important; }
.st-key-hero .stButton > button[kind="secondary"] { background: rgba(255,255,255,.06); color: #e8eef7;
  border-color: rgba(255,255,255,.28); }
.st-key-hero [data-testid="stCaptionContainer"] { color: #8ea5c5 !important; }

/* findings */
.ml-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(172px, 1fr)); gap: 14px; margin: 0.4rem 0 1.4rem; }
.ml-stat { background: var(--ml-panel); border: 1px solid var(--ml-line); border-radius: 16px; padding: 16px 18px 14px 22px;
  position: relative; transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
  animation: ml-rise .6s cubic-bezier(.2, .7, .2, 1) both; }
.ml-grid .ml-stat:nth-child(2) { animation-delay: .08s; } .ml-grid .ml-stat:nth-child(3) { animation-delay: .16s; }
.ml-grid .ml-stat:nth-child(4) { animation-delay: .24s; } .ml-grid .ml-stat:nth-child(5) { animation-delay: .32s; }
@keyframes ml-rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.ml-stat:hover { transform: translateY(-2px); box-shadow: var(--ml-shadow); border-color: color-mix(in srgb, var(--c, #3d8ef0) 55%, transparent); }
.ml-stat::before { content: ""; position: absolute; left: 0; top: 16px; bottom: 16px; width: 5px; border-radius: 0 4px 4px 0;
  background: var(--c, currentColor); box-shadow: 0 0 14px color-mix(in srgb, var(--c, #3d8ef0) 60%, transparent); }
.ml-stat.hatch::before { background: repeating-linear-gradient(45deg, var(--c) 0 3px, transparent 3px 6px); box-shadow: none; }
.ml-stat .k { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 2.5rem; line-height: 1; }
.ml-stat .k small { font-size: 1.05rem; font-weight: 600; margin-left: 0.2rem; color: color-mix(in srgb, currentColor 65%, transparent); }
.ml-stat .lbl { margin: 0.45rem 0 0.6rem; font-size: 0.98rem; line-height: 1.45; overflow-wrap: break-word; }
[lang="de"] .ml-stat .lbl, [lang="de"] .ml-stat .sure { hyphens: auto; }   /* long German compounds */
.ml-stat .sure { font-size: 0.84rem; line-height: 1.45; border-top: 1px dashed var(--ml-line); padding-top: 0.5rem; margin: 0; }
.ml-checkrow { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 0; margin: 0.4rem 0 1.4rem;
  background: linear-gradient(135deg, #0b1630 0%, #13234a 100%); border-radius: 16px; overflow: hidden;
  border: 1px solid rgba(111, 227, 255, .18); box-shadow: 0 12px 40px rgba(4, 10, 25, .25); }
.ml-check { padding: 18px 18px; color: #e8eef2; border-right: 1px solid rgba(160, 190, 230, .16); }
.ml-check:last-child { border-right: none; }
.ml-check .k { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 2rem; color: #fff; line-height: 1.05; }
.ml-check .t { font-weight: 600; color: #9fe9ff; margin: 0.3rem 0 0.25rem; font-size: 0.95rem; }
.ml-check p { font-size: 0.86rem; line-height: 1.45; color: #c3d0e0; margin: 0; }
.ml-pass { display: flex; gap: 0.8rem; align-items: center; background: var(--ml-panel-2); border: 1px solid var(--ml-line);
  border-radius: 12px; padding: 10px 14px; font-size: 0.95rem; margin: 0.2rem 0 1.2rem; }
.ml-pass b { font-family: 'IBM Plex Sans Condensed', sans-serif; font-size: 1.05rem; }
.ml-pass .orb { width: 34px; height: 34px; flex: none; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 16px; }
.st-key-paths [data-testid="stVerticalBlockBorderWrapper"] { transition: transform .2s ease, box-shadow .2s ease; background: var(--ml-panel); }
.st-key-paths [data-testid="stVerticalBlockBorderWrapper"]:hover { transform: translateY(-3px); box-shadow: var(--ml-shadow); }
.ml-pathd { font-size: 0.93rem; line-height: 1.45; margin: 0.1rem 0 0.4rem; }
.ml-path-ic { width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center; margin-bottom: .4rem;
  background: color-mix(in srgb, var(--c) 18%, transparent); color: var(--c); font-size: 1.3rem; }

/* findings list (story) */
.ml-finding { display: grid; grid-template-columns: 18px 7.5rem 1fr; gap: 0.2rem 0.9rem; align-items: baseline;
  padding: 0.7rem 0; border-top: 1px solid var(--ml-line); }
.ml-finding:last-child { border-bottom: 1px solid var(--ml-line); }
.ml-swatch { width: 14px; height: 14px; border-radius: 3px; display: inline-block; transform: translateY(2px); }
.ml-swatch.hatch { background-image: repeating-linear-gradient(45deg, currentColor 0 3px, transparent 3px 6px); }
.ml-num { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 1.6rem; white-space: nowrap; }
.ml-num small { font-size: 0.95rem; font-weight: 600; margin-left: 0.15rem; color: color-mix(in srgb, currentColor 65%, transparent); }
.ml-text { font-size: 1rem; line-height: 1.45; }
.ml-legend { display: flex; flex-wrap: wrap; gap: 0.4rem 1.1rem; font-size: 0.9rem; margin: 0.4rem 0 0.6rem; }
.ml-legend span { display: inline-flex; align-items: center; gap: 0.4rem; }

/* evidence cards */
.ml-card { background: var(--ml-panel); border: 1px solid var(--ml-line); border-radius: 16px; padding: 14px 16px; margin: 0 0 14px;
  transition: box-shadow .2s ease; }
.ml-card:hover { box-shadow: var(--ml-shadow); }
.ml-card-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }
.ml-id { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 1.3rem; }
.ml-card.flood .ml-id { color: var(--ml-water); }
.ml-place { flex: 1; min-width: 10rem; }
.ml-pill { font-size: 0.8rem; font-weight: 600; padding: 2px 10px; border-radius: 99px; white-space: nowrap;
  background: color-mix(in srgb, var(--ml-slide) 20%, transparent); color: var(--ml-slide); }
.ml-pill.high { background: var(--ml-slide); color: #fff; box-shadow: 0 0 14px color-mix(in srgb, var(--ml-slide) 55%, transparent); }
.ml-pill.low { background: var(--ml-panel-2); color: inherit; }
.ml-card-body { display: flex; gap: 16px; flex-wrap: wrap; }
.ml-chips { display: flex; gap: 8px; flex-wrap: wrap; }
.ml-chips figure { margin: 0; }
.ml-chips img { width: 150px; height: 150px; border-radius: 10px; display: block; image-rendering: pixelated; background: #0d1b26;
  border: 1px solid var(--ml-line); }
.ml-chips figcaption { font-size: 0.78rem; text-align: center; margin-top: 3px; }
.ml-facts { flex: 1; min-width: 260px; }
.ml-facts p, .ml-facts li { font-size: 0.95rem; line-height: 1.5; }
.ml-facts-h { font-weight: 600; margin: 0 0 0.2rem !important; }
.ml-why { margin: 0 0 0.7rem; padding-left: 1.1rem; }
.ml-checks { list-style: none; margin: 0 0 0.7rem; padding-left: 0; }
.ml-checks li { display: flex; gap: 0.55rem; align-items: baseline; margin: 0.15rem 0; }
.ml-ck { display: inline-grid; place-items: center; width: 1.25rem; height: 1.25rem; border-radius: 50%;
  font-size: 0.72rem; font-weight: 700; flex: none; transform: translateY(2px); }
.ml-ck.ok { background: var(--ml-water); color: #fff; }
.ml-ck.no { border: 1.5px solid color-mix(in srgb, currentColor 55%, transparent); color: color-mix(in srgb, currentColor 70%, transparent); }
.ml-ck.na { border: 1.5px dashed color-mix(in srgb, currentColor 40%, transparent); color: color-mix(in srgb, currentColor 55%, transparent); }
.ml-links { font-size: 0.9rem !important; margin: 0; }
.ml-links a { color: var(--ml-water); font-weight: 600; }
.ml-card-note { font-size: 0.8rem !important; margin: 0.7rem 0 0; max-width: none; }

/* downloads */
.ml-dlrow { display: flex; flex-wrap: wrap; gap: 10px; margin: 0.2rem 0 1.2rem; }
.ml-dl { display: inline-flex; flex-direction: column; gap: 1px; padding: 10px 15px; border-radius: 12px; border: 1px solid var(--ml-line);
  background: var(--ml-panel); color: inherit !important; text-decoration: none !important; font-weight: 600; font-size: 0.93rem;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease; }
.ml-dl small { font-weight: 400; font-size: 0.78rem; color: color-mix(in srgb, currentColor 65%, transparent); }
.ml-dl.primary { background: linear-gradient(135deg, #1f6fd1, #3d8ef0); border-color: transparent; color: #fff !important; }
.ml-dl.primary small { color: #dbe9ff; }
.ml-dl:hover { transform: translateY(-1px); box-shadow: var(--ml-shadow); border-color: var(--ml-water); }

/* page header band: the same night sky as the Overview, with Earth's limb along the bottom */
.ml-band { position: relative; overflow: hidden; isolation: isolate; border-radius: 20px; padding: 1.5rem 2rem 2.7rem;
  margin: 0 0 1.3rem; color: #e8eef7;
  background: radial-gradient(900px 320px at 92% -30%, #17325f 0%, rgba(23,50,95,0) 60%), linear-gradient(180deg, #070c17 0%, #0b1426 100%);
  box-shadow: 0 16px 44px rgba(4, 10, 25, .28); }
.ml-band::before { content: ""; position: absolute; inset: -50%; z-index: 0; pointer-events: none; opacity: .7;
  background-image:
    radial-gradient(1px 1px at 20px 30px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 140px 70px, #cfe3ff 50%, transparent 51%),
    radial-gradient(1.4px 1.4px at 260px 20px, #fff 50%, transparent 51%), radial-gradient(1px 1px at 380px 95px, #fff 50%, transparent 51%),
    radial-gradient(1px 1px at 470px 40px, #bcd6ff 50%, transparent 51%), radial-gradient(1.2px 1.2px at 560px 110px, #fff 50%, transparent 51%);
  background-size: 620px 150px; animation: ml-drift 160s linear infinite; }
.ml-band > * { position: relative; z-index: 1; }
.ml-band h1 { color: #f2f6fc !important; margin: .2rem 0 .5rem; padding: 0; font-size: clamp(2rem, 3vw, 2.8rem); }
.ml-band p { color: #c9d6e8 !important; margin: 0; max-width: 70ch; font-size: 1.05rem; line-height: 1.6; }
.ml-band .ml-kicker { color: #9fe9ff !important; font-size: .95rem; }

/* sidebar: where NISAR is in its 12-day cycle */
.ml-orbit { display: flex; gap: .7rem; align-items: center; margin: .9rem 0 .4rem; padding: .6rem .7rem; border-radius: 14px;
  background: linear-gradient(135deg, rgba(11,22,48,.92), rgba(19,35,74,.92)); border: 1px solid rgba(111,227,255,.2);
  color: #e6edf6; }
.ml-orbit svg { width: 64px; height: 64px; flex: none; }
.ml-orbit b { display: block; font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; font-size: .92rem; line-height: 1.25; }
.ml-orbit span { display: block; font-size: .8rem; line-height: 1.35; color: #a9bdd8; margin-top: .15rem; }
.ml-orbit .eta { display: inline; color: #9fe9ff; font-weight: 600; }
@media (prefers-reduced-motion: reduce) { .ml-orbit .sat { display: none; } }

/* smoother reruns: keep the page readable instead of greying it out */
[data-stale="true"], .stale-element { opacity: .9 !important; transition: opacity .3s ease !important; }
html { scroll-behavior: smooth; }
[data-testid="stDecoration"] { background: linear-gradient(90deg, #6fe3ff, #3d8ef0 55%, #f0743a) !important; height: 3px !important; }

/* story: chapter rail along an orbit track */
.st-key-rail { position: relative; gap: 0 !important; margin: 0 0 1.1rem; flex-wrap: nowrap !important; }
.st-key-rail::before { content: ""; position: absolute; left: 0; right: 0; top: 11px; height: 2px; border-radius: 2px;
  background: var(--ml-line); }
.st-key-rail > div { flex: 1 1 0 !important; min-width: 0; }
.st-key-rail button { width: 100%; background: transparent !important; border: none !important; box-shadow: none !important;
  flex-direction: column !important; gap: .45rem; padding: 0 .2rem .2rem !important; min-height: 0 !important; color: inherit !important; }
.st-key-rail button::before { content: ""; width: 12px; height: 12px; border-radius: 50%; margin-top: 5px;
  background: var(--ml-panel-2); border: 2px solid color-mix(in srgb, currentColor 35%, transparent); transition: all .25s ease; }
.st-key-rail button p { font-size: .82rem !important; line-height: 1.25; opacity: .7; white-space: normal; text-align: center; }
.st-key-rail button:hover p { opacity: 1; }
.st-key-rail button:hover::before { border-color: var(--ml-water); }
.st-key-rail button[kind="primary"]::before, .st-key-rail [data-testid="stBaseButton-primary"]::before {
  background: var(--ml-beam); border-color: #fff; box-shadow: 0 0 0 4px rgba(111,227,255,.18), 0 0 14px var(--ml-beam); }
.st-key-rail button[kind="primary"] p, .st-key-rail [data-testid="stBaseButton-primary"] p { opacity: 1; font-weight: 600; }
[class*="st-key-chapter"] { animation: ml-chapter .45s cubic-bezier(.2, .7, .2, 1) both; }
@keyframes ml-chapter { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.ml-hint { font-size: .8rem !important; margin: .6rem 0 0; color: color-mix(in srgb, currentColor 60%, transparent) !important; }
.st-key-storykeys { position: absolute !important; height: 0 !important; overflow: hidden; }

/* story visuals in an instrument frame: corner brackets and a source label */
.st-key-viz { position: relative; padding: 14px 14px 12px !important; border-radius: 16px; background: var(--ml-panel);
  border: 1px solid var(--ml-line);
  background-image:
    linear-gradient(var(--ml-water), var(--ml-water)), linear-gradient(var(--ml-water), var(--ml-water)),
    linear-gradient(var(--ml-water), var(--ml-water)), linear-gradient(var(--ml-water), var(--ml-water)),
    linear-gradient(var(--ml-water), var(--ml-water)), linear-gradient(var(--ml-water), var(--ml-water)),
    linear-gradient(var(--ml-water), var(--ml-water)), linear-gradient(var(--ml-water), var(--ml-water));
  background-size: 16px 2px, 2px 16px, 16px 2px, 2px 16px, 16px 2px, 2px 16px, 16px 2px, 2px 16px;
  background-position: 8px 8px, 8px 8px, calc(100% - 8px) 8px, calc(100% - 8px) 8px,
    8px calc(100% - 8px), 8px calc(100% - 8px), calc(100% - 8px) calc(100% - 8px), calc(100% - 8px) calc(100% - 8px);
  background-repeat: no-repeat; }
.ml-instr { margin: 0 0 0 1.2rem !important; display: flex; gap: .45rem; align-items: center;
  font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; font-size: .88rem;
  color: color-mix(in srgb, currentColor 75%, transparent); }
.ml-instr i { width: 7px; height: 7px; border-radius: 50%; background: var(--ml-beam); box-shadow: 0 0 8px var(--ml-beam); }

/* method: phased pipeline */
.ml-phase { font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 600; font-size: 1.05rem; margin: 1.2rem 0 .4rem;
  display: flex; align-items: center; gap: .6rem; }
.ml-phase::after { content: ""; flex: 1; height: 1px; background: var(--ml-line); }
.ml-steps { list-style: none; margin: 0; padding: 0; position: relative; }
.ml-steps::before { content: ""; position: absolute; left: 17px; top: 8px; bottom: 8px; width: 2px; background: var(--ml-line); }
.ml-steps li { position: relative; padding: 0 0 1rem 3.1rem; max-width: none; }
.ml-steps .n { position: absolute; left: 0; top: 0; width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center;
  font-family: 'IBM Plex Sans Condensed', sans-serif; font-weight: 700; font-size: 1rem; color: #fff;
  background: linear-gradient(135deg, #1f6fd1, #3d8ef0); box-shadow: 0 0 0 4px var(--ml-panel-2); }
.ml-steps .t { font-weight: 600; font-size: 1.05rem; margin: .35rem 0 .2rem; }
.ml-steps .d { margin: 0; font-size: .97rem; line-height: 1.6; max-width: 80ch; }
.ml-chips2 { display: flex; flex-wrap: wrap; gap: .35rem; margin: .45rem 0 0; }
.ml-chips2 span { font-size: .8rem; padding: 2px 9px; border-radius: 99px; border: 1px solid var(--ml-line); background: var(--ml-panel);
  white-space: nowrap; }
.ml-flow { display: flex; flex-wrap: wrap; align-items: stretch; gap: 0; margin: .4rem 0 1rem; }
.ml-flow div { flex: 1 1 120px; padding: .7rem .8rem; border: 1px solid var(--ml-line); background: var(--ml-panel); font-size: .9rem;
  line-height: 1.35; position: relative; }
.ml-flow div:first-child { border-radius: 12px 0 0 12px; } .ml-flow div:last-child { border-radius: 0 12px 12px 0; }
.ml-flow div + div { border-left: none; }
.ml-flow b { display: block; font-family: 'IBM Plex Sans Condensed', sans-serif; font-size: 1rem; color: var(--ml-water); }
.ml-facts-card { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; border-radius: 16px; overflow: hidden;
  border: 1px solid rgba(111,227,255,.18); background: linear-gradient(135deg, #0b1630 0%, #13234a 100%); margin: .3rem 0 .4rem; }
.ml-facts-card div { padding: .9rem 1rem; border-right: 1px solid rgba(160,190,230,.14); border-bottom: 1px solid rgba(160,190,230,.14); }
.ml-facts-card dt { font-size: .8rem; color: #9fe9ff; margin: 0 0 .15rem; font-weight: 600; }
.ml-facts-card dd { margin: 0; color: #e8eef7; font-size: .95rem; line-height: 1.4; }
.ml-cardgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 12px; margin: .4rem 0 1.2rem; }
.ml-cardgrid > div { background: var(--ml-panel); border: 1px solid var(--ml-line); border-radius: 14px; padding: .85rem 1rem; }
.ml-cardgrid b { display: block; margin-bottom: .25rem; font-size: 1rem; }
.ml-cardgrid p { margin: 0; font-size: .92rem; line-height: 1.55; max-width: none; }
.ml-cardgrid .lim b::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: .45rem;
  background: var(--ml-slide); transform: translateY(-1px); }
.ml-toc { display: flex; flex-wrap: wrap; gap: .4rem; margin: 0 0 1rem; }
.ml-toc a { font-size: .86rem; padding: 4px 11px; border-radius: 99px; border: 1px solid var(--ml-line); background: var(--ml-panel);
  color: inherit !important; text-decoration: none !important; transition: border-color .15s ease, background .15s ease; }
.ml-toc a:hover { border-color: var(--ml-water); background: var(--ml-panel-2); }

@media (max-width: 640px) {
  .ml-band { padding: 1.1rem 1.1rem 2.3rem; border-radius: 16px; }
  .st-key-rail button p { display: none; }
  .st-key-rail button[kind="primary"] p, .st-key-rail [data-testid="stBaseButton-primary"] p { display: block; font-size: .75rem !important; }
  .ml-facts-card { grid-template-columns: 1fr; }
  .ml-flow div { flex-basis: 45%; border-left: 1px solid var(--ml-line) !important; border-radius: 0 !important; }
  .ml-finding { grid-template-columns: 16px 6rem 1fr; }
  .ml-num { font-size: 1.3rem; }
  h1 { font-size: 2rem; }
  .st-key-hero { padding: 1.4rem 1.1rem 1rem; border-radius: 16px; }
  .ml-chips img { width: 28vw; height: 28vw; }
  .ml-stat .k { font-size: 2.1rem; }
  .ml-grid { grid-template-columns: 1fr !important; }
  .ml-check { border-right: none; border-bottom: 1px solid rgba(160, 190, 230, .16); }
}
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
</style>
"""

# Marathi strings: drafted by the team's assistant, to be checked by a native speaker before submission.
T = {
    "title": {"en": "What NISAR radar saw in the 2026 Pune monsoon",
              "mr": "२०२६ च्या पुणे पावसाळ्यात निसार रडारने काय पाहिले"},
    "lede": {"en": "Monsoon cloud hides the ground exactly when people most need to see it. {cloud} NASA and ISRO's "
                   "NISAR satellite sends radar through cloud and rain. We compared its passes over Pune before and "
                   "after the floods and landslides of 3 to 8 July 2026.",
             "mr": "पावसाळ्यातील ढग नेमके तेव्हाच जमीन झाकतात जेव्हा ती पाहण्याची सर्वात जास्त गरज असते. {cloud} नासा "
                   "आणि इस्रोचा निसार उपग्रह ढग आणि पावसातून रडार पाठवतो. ३ ते ८ जुलै २०२६ च्या पूर आणि भूस्खलनांच्या "
                   "आधी आणि नंतरच्या पुण्यावरील निरीक्षणांची आम्ही तुलना केली."},
    "dates_line": {"en": "NISAR L-band radar passes on {b} and {a} {y}, Pune district, India",
                   "mr": "{b} आणि {a} {y} रोजीची निसार एल-बँड रडार निरीक्षणे, पुणे जिल्हा, भारत"},
    "found": {"en": "What the radar found", "mr": "रडारला काय सापडले"},
    "new_water": {"en": "of new open water on flat ground, outside rivers and reservoirs",
                  "mr": "नद्या आणि धरणांबाहेर, सपाट जमिनीवर नवीन साचलेले पाणी"},
    "rise": {"en": "of new water as Pune's reservoirs and rivers rose and filled",
             "mr": "पुण्याची धरणे आणि नद्या भरल्यामुळे वाढलेले नवीन पाणी"},
    "flood": {"en": "of flood water still standing on 10 July where no water was recorded between 1984 and 2021",
              "mr": "१९८४ ते २०२१ दरम्यान कधीही पाणी न नोंदवलेल्या ठिकाणी १० जुलैला अजूनही साचलेले पुराचे पाणी"},
    "legend_flood": {"en": "Flooding (no water 1984 to 2021)", "mr": "पूर (१९८४ ते २०२१ पाणी नव्हते)"},
    "legend_rise": {"en": "Reservoirs and rivers rising", "mr": "धरणे आणि नद्या वाढल्या"},
    "slides": {"en": "likely slide zones on slopes of {smin}° to {smax}°, {high} of them high confidence. They are "
                     "leads to check: {unrep} have no reported event within 2 km",
               "mr": "{smin}° ते {smax}° उताराच्या भागात संभाव्य भूस्खलन क्षेत्रे, त्यापैकी {high} उच्च खात्रीची. ही "
                     "तपासण्याजोगी ठिकाणे आहेत: {unrep} क्षेत्रांच्या 2 किमी परिसरात कोणतीही घटना नोंदवलेली नाही"},
    "xt_good": {"en": "of the slide zones that a second NISAR track could see were found by it too, "
                      "{lift}× more often than chance",
                "mr": "दुसऱ्या निसार मार्गाला दिसू शकलेल्या भूस्खलन क्षेत्रांपैकी तिथेही सापडलेली क्षेत्रे, योगायोगापेक्षा "
                      "{lift}× जास्त वेळा"},
    "xt_good_small": {"en": "of the slide zones a second NISAR track could see were found by it too: {lift}× more often "
                            "than chance, from a small sample, as that track covers {cov} of the area",
                      "mr": "दुसऱ्या निसार मार्गाला दिसू शकलेल्या भूस्खलन क्षेत्रांपैकी तिथेही सापडलेली क्षेत्रे: योगायोगापेक्षा "
                            "{lift}× जास्त वेळा; पण नमुना लहान आहे, कारण तो मार्ग क्षेत्राचा फक्त {cov} भाग पाहतो"},
    "xt_story_good_small": {"en": "A second NISAR track, passing on {b} and {a} from a different orbit, sees {cov} of the "
                                  "area. Of the {n} zones inside its view, it found {c} again on its own: {lift}× more "
                                  "often than chance, though {n} is a small sample.",
                            "mr": "{b} आणि {a} रोजी वेगळ्या कक्षेतून गेलेला दुसरा निसार मार्ग क्षेत्राचा {cov} भाग पाहतो. "
                                  "त्याच्या दृष्टीतील {n} क्षेत्रांपैकी {c} त्याने स्वतंत्रपणे पुन्हा शोधली: योगायोगापेक्षा "
                                  "{lift}× जास्त वेळा, पण {n} हा लहान नमुना आहे."},
    "xt_weak": {"en": "of the slide zones that a second NISAR track could see were found by it too, about what "
                      "chance would give: treat single-track zones with extra care",
                "mr": "दुसऱ्या निसार मार्गाला दिसू शकलेल्या भूस्खलन क्षेत्रांपैकी तिथेही सापडलेली क्षेत्रे, साधारण "
                      "योगायोगाइतकी: एकाच मार्गावरील क्षेत्रे काळजीपूर्वक तपासा"},
    "xt_story_good": {"en": "A second NISAR track, passing on {b} and {a} from a different orbit, found {c} of the {n} "
                            "zones it could see on its own: {lift}× more often than chance.",
                      "mr": "{b} आणि {a} रोजी वेगळ्या कक्षेतून गेलेल्या दुसऱ्या निसार मार्गाने, त्याला दिसू शकलेल्या "
                            "{n} पैकी {c} क्षेत्रे स्वतंत्रपणे शोधली: योगायोगापेक्षा {lift}× जास्त वेळा."},
    "xt_story_weak": {"en": "A second NISAR track, passing on {b} and {a}, found only {c} of the {n} zones it could see, "
                            "about what chance would give, so treat each zone as a lead to check.",
                      "mr": "{b} आणि {a} रोजी गेलेल्या दुसऱ्या निसार मार्गाने त्याला दिसू शकलेल्या {n} पैकी फक्त {c} "
                            "क्षेत्रे शोधली, साधारण योगायोगाइतकी; म्हणून प्रत्येक क्षेत्र तपासण्याजोगे समजा."},
    "xt_col": {"en": "Second track", "mr": "दुसरा मार्ग"},
    "brighter": {"en": "where water may be hiding under trees or between buildings (not counted as flood)",
                 "mr": "जिथे झाडांखाली किंवा इमारतींमध्ये पाणी असू शकते (पुरात मोजलेले नाही)"},
    "matched": {"en": "of reported events that radar could observe were matched by a detection",
                "mr": "रडारला दिसू शकणाऱ्या नोंदवलेल्या घटनांपैकी शोधलेल्या घटना"},
    "start_story": {"en": "Start the story", "mr": "कथा सुरू करा"},
    "explore": {"en": "Explore the map", "mr": "नकाशा पाहा"},
    "method": {"en": "How we did it", "mr": "आम्ही हे कसे केले"},
    "before": {"en": "Before", "mr": "आधी"},
    "after": {"en": "After", "mr": "नंतर"},
    "couldnt": {"en": "What radar could not see", "mr": "रडारला काय दिसले नाही"},
    "lim_streets": {"en": "**Flooded streets between buildings.** Radar bounces off walls and back to the satellite, "
                          "so a flooded street can look bright, not dark. {built_sentence}",
                    "mr": "**इमारतींमधील पाण्याखालचे रस्ते.** रडार भिंतींवरून उपग्रहाकडे परत येते, त्यामुळे पाण्याखालचा "
                          "रस्ता गडद न दिसता उजळ दिसू शकतो. {built_sentence}"},
    "lim_built_all": {"en": "All {n} of the reported floods we missed were in built-up areas.",
                      "mr": "आम्हाला न सापडलेले नोंदवलेले सर्व {n} पूर दाट वस्तीच्या भागात होते."},
    "lim_built_some": {"en": "{k} of the {n} reported floods we missed were in built-up areas.",
                       "mr": "आम्हाला न सापडलेल्या {n} नोंदवलेल्या पुरांपैकी {k} दाट वस्तीच्या भागात होते."},
    "lim_timing": {"en": "**Water that came and went between passes.** The heaviest rain fell from {p1} to {p2}; "
                         "NISAR looked on {b} and again on {a}. The map shows what was still standing on {a}, "
                         "not the peak.",
                   "mr": "**दोन निरीक्षणांच्या मधे आलेले आणि ओसरलेले पाणी.** सर्वात जास्त पाऊस {p1} ते {p2} दरम्यान "
                         "पडला; निसारने {b} रोजी आणि पुन्हा {a} रोजी पाहिले. नकाशा {a} रोजी साचलेले पाणी दाखवतो, "
                         "सर्वोच्च पातळी नाही."},
    "lim_small": {"en": "**Small slides, and slides on gentle ground.** Our map has {res} m pixels and searches slopes "
                        "of {smin}° to {smax}°. A slide the width of one house can slip through{gentle_part}.",
                  "mr": "**लहान भूस्खलने आणि कमी उतारावरील भूस्खलने.** आमच्या नकाशातील प्रत्येक चौकोन {res} मीटरचा आहे "
                        "आणि आम्ही {smin}° ते {smax}° उतार तपासतो. एका घराएवढ्या रुंदीचे भूस्खलन सुटू शकते{gentle_part}."},
    "lim_gentle": {"en": ", and {n} reported landslides were on ground gentler than that",
                   "mr": ", आणि नोंदवलेली {n} भूस्खलने याहून कमी उताराच्या जमिनीवर होती"},
    "lim_hidden": {"en": "**Slopes hidden from the satellite.** About {pct}% of the steep ground faces away from the "
                         "radar or folds over itself in the image. We leave those slopes out and do not guess.",
                   "mr": "**उपग्रहापासून लपलेले उतार.** तीव्र उताराच्या जमिनीपैकी सुमारे {pct}% भाग रडारपासून दूर "
                         "वळलेला आहे किंवा प्रतिमेत स्वतःवरच दुमडला जातो. असे उतार आम्ही वगळतो आणि अंदाज लावत नाही."},
    "lim_early": {"en": "**Early data.** NASA has calibrated these NISAR products but validated them at only a "
                        "limited number of sites so far. Our numbers will move as the data matures.",
                  "mr": "**सुरुवातीचा डेटा.** नासाने ही निसार उत्पादने कॅलिब्रेट केली आहेत, पण आतापर्यंत मर्यादित "
                        "ठिकाणीच त्यांची पडताळणी झाली आहे. डेटा परिपक्व होईल तसे आमचे आकडे बदलतील."},
    "lim_lead": {"en": "Every likely slide zone is a lead to check on the ground, not a verdict: {u} of the {z} zones "
                       "have no reported event within 2 km.",
                 "mr": "प्रत्येक संभाव्य भूस्खलन क्षेत्र हा जमिनीवर तपासण्याचा संकेत आहे, निर्णय नाही: {z} पैकी {u} "
                       "क्षेत्रांच्या 2 किमी परिसरात कोणतीही घटना नोंदवलेली नाही."},
    "res_last_clause": {"en": ", and was {v} km² on {d}", "mr": ", आणि {d} रोजी {v} चौ. किमी होता"},
    "timeline_caption": {"en": "Dark water on each NISAR pass of the same orbit and radar mode, counted inside the area "
                               "where the JRC record has seen water at least once (1984 to 2021).",
                         "mr": "एकाच कक्षेतून आणि एकाच रडार पद्धतीतील प्रत्येक निसार निरीक्षणातील गडद पाणी, JRC नोंदीत "
                               "(१९८४ ते २०२१) किमान एकदा पाणी दिसलेल्या भागात मोजलेले."},
    "cloud_sentence": {"en": "From {f} to {t}, all {n} of NASA's daily satellite photos of the area showed only cloud.",
                       "mr": "{f} ते {t} दरम्यान या भागाची नासाची रोजची सर्व {n} उपग्रह छायाचित्रे फक्त ढगांनी भरलेली होती."},
    "cloud_caption": {"en": "NASA's daily satellite photos of our study area. Rows: {sensors}; columns: dates "
                            "(month-day). From {f} to {t}, all {n} available photos show only cloud; on the radar "
                            "days, {p1} and {p2}, the cloud was broken. Black: no photo of the area that day. "
                            "Source: [NASA Worldview]({url}) (GIBS).",
                      "mr": "आमच्या अभ्यास क्षेत्राची नासाची रोजची उपग्रह छायाचित्रे. ओळी: {sensors}; स्तंभ: तारखा "
                            "(महिना-दिवस). {f} ते {t} दरम्यान उपलब्ध सर्व {n} छायाचित्रांत फक्त ढग आहेत; रडारच्या "
                            "दिवशी, {p1} आणि {p2}, ढग विरळ होते. काळे: त्या दिवशी या भागाचे छायाचित्र नाही. "
                            "स्रोत: [नासा वर्ल्डव्ह्यू]({url}) (GIBS)."},
    "demo": {"en": "<b>Demo data.</b> The radar values on this page are synthetic, made in NISAR's file format so the "
                   "app could be built before the real Pune files were processed. Terrain, rivers and reservoirs are "
                   "real; floods and slide zones are not.",
             "mr": "<b>प्रात्यक्षिक डेटा.</b> या पानावरील रडार मूल्ये कृत्रिम आहेत. भूभाग, नद्या आणि धरणे खरी आहेत; पूर "
                   "आणि भूस्खलन क्षेत्रे खरी नाहीत."},
    "no_data": {"en": "Results are not built yet. Run `python -m pipeline.run_all`.",
                "mr": "निकाल अजून तयार नाहीत."},
    "layers": {"en": "Layers", "mr": "स्तर"},
    "legend_new_water": {"en": "New open water", "mr": "नवीन साचलेले पाणी"},
    "legend_slides": {"en": "Likely slide zone", "mr": "संभाव्य भूस्खलन क्षेत्र"},
    "legend_brighter": {"en": "Possible water under cover", "mr": "झाकलेले संभाव्य पाणी"},
    "legend_permanent": {"en": "Rivers and reservoirs", "mr": "नद्या आणि धरणे"},
    "legend_events": {"en": "Reported event", "mr": "नोंदवलेली घटना"},
    "lang": {"en": "Language", "mr": "भाषा"},
    "step": {"en": "Step {i} of {n}", "mr": "{n} पैकी टप्पा {i}"},
    "back": {"en": "Back", "mr": "मागे"},
    "next": {"en": "Next", "mr": "पुढे"},
    "story_title": {"en": "Story", "mr": "कथा"},
    "matched_floods": {"en": "reported floods that radar could observe had a detection nearby",
                       "mr": "रडारला दिसू शकणाऱ्या नोंदवलेल्या पुरांजवळ शोध लागला"},
    "matched_slides": {"en": "reported landslides that radar could observe had a detection nearby",
                       "mr": "रडारला दिसू शकणाऱ्या नोंदवलेल्या भूस्खलनांजवळ शोध लागला"},
    "x_of_y": {"en": "{x} of {y}", "mr": "{y} पैकी {x}"},
    "and_join": {"en": "{a} and {b}", "mr": "{a} आणि {b}"},
    "slide_fragile_one": {"en": "Both landslide matches are to the same zone, {d} km from the reports, and neither holds "
                                "when the slide rule uses NASA's NASADEM elevation map instead (see Method).",
                          "mr": "दोन्ही भूस्खलन जुळण्या एकाच क्षेत्राशी आहेत, नोंदींपासून {d} किमी अंतरावर, आणि त्याऐवजी "
                                "नासाचा NASADEM उंची नकाशा वापरल्यास त्यापैकी एकही टिकत नाही (पद्धत पान पाहा)."},
    "slide_fragile": {"en": "With NASA's NASADEM elevation map instead, {k} of {n} landslide matches hold (see Method).",
                      "mr": "त्याऐवजी नासाचा NASADEM उंची नकाशा वापरल्यास {n} पैकी {k} भूस्खलन जुळण्या टिकतात "
                            "(पद्धत पान पाहा)."},
    "fell_short": {"en": "Where radar fell short, and why", "mr": "रडार कुठे कमी पडले आणि का"},
    "rain_caption": {"en": "Daily rainfall averaged over the study box. Source: {src}.",
                     "mr": "अभ्यास क्षेत्रातील सरासरी रोजचा पाऊस. स्रोत: {src}."},
    "swipe_caption": {"en": "Drag to compare. Dark is smooth: water. Bright is rough: buildings, trees, rock. "
                            "Area shown: the part of the study box with the most change.",
                      "mr": "तुलना करण्यासाठी ओढा. गडद म्हणजे गुळगुळीत पृष्ठभाग: पाणी. उजळ म्हणजे खडबडीत: इमारती, "
                            "झाडे, खडक. दाखवलेला भाग: अभ्यास क्षेत्रातील सर्वात जास्त बदल झालेला भाग."},
}


def english_only_note():
    """Technical pages are in English only; say so in the chosen language instead of switching silently."""
    if lang() == "mr":
        st.info("हे तांत्रिक पान सध्या बहुतांश इंग्रजीत आहे. आकडे आणि कथा मराठीत पाहण्यासाठी "
                "मुख्य पान आणि कथा पाहा.")
    elif lang() == "de":
        st.info("Diese technische Seite ist auf Englisch. Zahlen und Geschichte gibt es auf den anderen Seiten auf "
                "Deutsch.")


MONTHS = {"en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"],
          "mr": ["जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून", "जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर",
                 "नोव्हेंबर", "डिसेंबर"],
          "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
                 "November", "Dezember"]}


def day(iso: str) -> str:
    """'5 July', '5 जुलै' or '5. Juli', in the page language."""
    d = int(iso[8:10])
    return f"{d}{'.' if lang() == 'de' else ''} {MONTHS.get(lang(), MONTHS['en'])[int(iso[5:7]) - 1]}"


MONTHS_SHORT = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                "de": ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]}


def day_short(iso: str) -> str:
    """'5 Jul', '5. Juli' or '5 जुलै': for chart axes."""
    lg = lang()
    months = MONTHS_SHORT.get(lg) or MONTHS.get(lg, MONTHS["en"])
    return f"{int(iso[8:10])}{'.' if lg == 'de' else ''} {months[int(iso[5:7]) - 1]}"


def date(iso: str) -> str:
    """'5 July 2026' or '5 जुलै 2026', in the page language."""
    return f"{day(iso)} {iso[:4]}"


def lang() -> str:
    return st.session_state.get("lang", "en")


def tr(en: str, mr: str, **kw) -> str:
    """Inline text for page-specific strings: English and Marathi here, German from i18n_de.DE."""
    if lang() == "de":
        from .i18n_de import DE
        s = DE.get(en, en)
    else:
        s = mr if lang() == "mr" and mr else en
    return s.format(**kw) if kw else s


def t(key: str, **kw) -> str:
    if lang() == "de":
        from .i18n_de import DE_T
        s = DE_T.get(key) or T.get(key, {}).get("en", key)
    else:
        s = T.get(key, {}).get(lang()) or T.get(key, {}).get("en", key)
    return s.format(**kw) if kw else s


LANGS = {"en": "English", "mr": "मराठी", "de": "Deutsch"}
ASSETS = __import__("pathlib").Path(__file__).resolve().parents[1] / "assets"


def dark() -> bool:
    """True when the visitor sees Streamlit's dark theme (system setting or ⋮ > Settings)."""
    try:
        return (st.context.theme.type or "light") == "dark"
    except Exception:
        return False


def ink() -> str:
    """Text colour for SVG and chart text, matching the active theme."""
    return "#e6edf6" if dark() else "#10213a"


def muted() -> str:
    return "#9fb0c6" if dark() else "#5d6b75"


def surface() -> str:
    """Page background, for rings that separate a mark from what is behind it."""
    return "#070c17" if dark() else "#f4f7fb"


def hairline() -> str:
    return "rgba(230,237,246,.14)" if dark() else "#dde4ec"


def page_header(title: str, lede: str = "", kicker: str = ""):
    """A slim night-sky band with Earth's limb along the bottom, used at the top of every page but the Overview."""
    k = f'<p class="ml-kicker">{kicker}</p>' if kicker else ""
    p = f"<p>{lede}</p>" if lede else ""
    st.markdown(f'<header class="ml-band">{k}<h1>{html.escape(title)}</h1>{p}</header>', unsafe_allow_html=True)


ORBIT_SVG = """<svg viewBox="0 0 120 120" aria-hidden="true">
<defs><radialGradient id="mlEarth" cx="36%" cy="32%" r="72%"><stop offset="0" stop-color="#5fb2ff"/>
<stop offset=".5" stop-color="#1d63b3"/><stop offset="1" stop-color="#081f42"/></radialGradient></defs>
<g transform="rotate(-62 60 60)"><path d="M108 60 A48 15 0 0 0 12 60" fill="none" stroke="#6fe3ff" stroke-opacity=".28"
stroke-width="1.4" stroke-dasharray="3 3"/></g>
<circle cx="60" cy="60" r="31" fill="#6fe3ff" opacity=".14"/>
<circle cx="60" cy="60" r="28.5" fill="url(#mlEarth)"/>
<path d="M47 49c4-3 9-3 12 0s2 7-2 9-5 6-9 5-6-5-4-8 1-4 3-6z M66 66c3-2 7-1 8 2s-1 6-4 6-6-1-6-4 0-3 2-4z"
fill="#7fc8a0" opacity=".55"/>
<path d="M60 31.5a28.5 28.5 0 0 1 0 57a22 28.5 0 0 0 0-57z" fill="#020814" opacity=".45"/>
<g transform="rotate(-62 60 60)"><path id="mlOrbit" d="M108 60 A48 15 0 0 1 12 60 A48 15 0 0 1 108 60" fill="none"/>
<path d="M108 60 A48 15 0 0 1 12 60" fill="none" stroke="#6fe3ff" stroke-opacity=".8" stroke-width="1.4"/>
<g class="sat"><circle r="3.2" fill="#fff"/><circle r="6" fill="#6fe3ff" opacity=".35"/>
<animateMotion dur="9s" repeatCount="indefinite" rotate="auto"><mpath href="#mlOrbit"/></animateMotion>
<animate attributeName="opacity" dur="9s" repeatCount="indefinite" values="1;1;.2;.2;1" keyTimes="0;.47;.53;.97;1"/></g></g>
</svg>"""


def orbit_widget():
    """Sidebar card: a small Earth with NISAR's orbit, and how many days until it is expected over Pune again."""
    np_ = data.next_pass()
    if not np_:
        return
    import pandas as pd
    days = (pd.Timestamp(np_[1]) - pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize()).days
    when = tr("tomorrow", "उद्या") if days == 1 else tr("in {n} days", "{n} दिवसांनी", n=days)
    st.markdown(f'<div class="ml-orbit">{ORBIT_SVG}<div><b>'
                + tr("Next expected NISAR pass over Pune", "पुण्यावरील पुढचे अपेक्षित निसार निरीक्षण")
                + f'</b><span><span class="eta">{when}</span>, {date(np_[1])}</span><span>'
                + tr("Every 12 days, cloud or not.", "दर १२ दिवसांनी, ढग असोत वा नसोत.")
                + "</span></div></div>", unsafe_allow_html=True)


def setup(page_title: str):
    st.set_page_config(page_title=f"MonsoonLens: {page_title}", page_icon=str(ASSETS / "logo_icon.png"),
                       layout="wide", initial_sidebar_state="auto")
    st.markdown(CSS, unsafe_allow_html=True)
    data.publish_overlays()
    if "lang" not in st.session_state:                    # ?lang=de or ?lang=mr opens the app in that language
        q = st.query_params.get("lang")
        st.session_state["lang"] = q if q in LANGS else "en"
    st.logo(str(ASSETS / "logo.png"), icon_image=str(ASSETS / "logo_icon.png"), size="large")
    with st.sidebar:
        st.markdown(f'<p class="ml-brand-sub">{tr("What NASA-ISRO NISAR radar saw through the 2026 Pune monsoon",
                                                  "२०२६ च्या पुणे पावसाळ्यात नासा-इस्रो निसार रडारने काय पाहिले")}</p>',
                    unsafe_allow_html=True)
        names = list(LANGS.values())
        choice = st.radio(t("lang"), names, horizontal=True, index=list(LANGS).index(lang()), key="lang_choice")
        st.session_state["lang"] = list(LANGS)[names.index(choice)]
        orbit_widget()
        st.caption(tr("Light or dark: ⋮ menu (top right) › Settings.", "फिका किंवा गडद रंग: ⋮ मेनू (वर उजवीकडे) › Settings."))
        st.caption(tr("Built by team iGenfinity for NASA Space Apps 2026", "नासा स्पेस ॲप्स २०२६ साठी iGenfinity टीमने बनवले"))
    # Keep the language in the address, so a shared link opens in the language it was sent in.
    if lang() != "en":
        st.query_params["lang"] = lang()
    elif "lang" in st.query_params:
        del st.query_params["lang"]


def demo_banner():
    if data.source()["demo"]:
        st.markdown(f'<div class="ml-banner">{t("demo")}</div>', unsafe_allow_html=True)


def require_results() -> bool:
    if not data.source()["dir"]:
        st.warning(t("no_data"))
        return False
    return True


def fmt_num(v, digits=1):
    if v is None:
        return "not available"
    if isinstance(v, (int,)) or float(v).is_integer() and abs(v) >= 10:
        return f"{int(round(v)):,}"
    return f"{v:,.{digits}f}"


def finding(color: str, number: str, unit: str, text: str, hatch=False):
    sw = f'<span class="ml-swatch{" hatch" if hatch else ""}" style="background-color:{color};color:{color}"></span>' \
        if not hatch else f'<span class="ml-swatch hatch" style="color:{color};border:1px solid {color}"></span>'
    return (f'<div class="ml-finding">{sw}<div class="ml-num">{html.escape(number)}<small>{html.escape(unit)}</small></div>'
            f'<div class="ml-text">{html.escape(text)}</div></div>')


def legend(items):
    parts = []
    for color, label, kind in items:
        if kind == "hatch":
            sw = f'<span class="ml-swatch hatch" style="color:{color};border:1px solid {color}"></span>'
        elif kind == "dot":
            sw = f'<span class="ml-swatch" style="background:#fff;border:2px solid currentColor;border-radius:50%"></span>'
        elif kind == "outline":
            sw = f'<span class="ml-swatch" style="background:{color}55;border:2px solid {color}"></span>'
        else:
            sw = f'<span class="ml-swatch" style="background:{color}"></span>'
        parts.append(f"<span>{sw}{html.escape(label)}</span>")
    st.markdown(f'<div class="ml-legend">{"".join(parts)}</div>', unsafe_allow_html=True)


def sources_line():
    """One short credit line; the full file list with links is on the Method page."""
    m = data.metrics()
    srcs = m.get("sources", [])
    if not srcs:
        return
    tracks = sorted({s["granule_id"].split("_")[5] for s in srcs if s["granule_id"].count("_") > 5})
    days = sorted({s["granule_id"].split("_A_")[-1][:8] if "_A_" in s["granule_id"] else "" for s in srcs} - {""})
    iso = lambda d: f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    when = f"{data.nice_date(iso(days[0]), False)} to {data.nice_date(iso(days[-1]))}" if days else ""
    tr = ("track " if len(tracks) == 1 else "tracks ") + " and ".join(t.lstrip("0") or "0" for t in tracks)
    st.markdown(f'<p class="ml-source">Radar: {len(srcs)} NISAR L2 provisional files, {tr}, {when} '
                f'(NASA/JPL-Caltech and ISRO, via ASF DAAC); every file is linked on the Method page. '
                f'Results built {m.get("generated", "")[:10]}, pipeline v{m.get("pipeline_version", "")}.</p>',
                unsafe_allow_html=True)