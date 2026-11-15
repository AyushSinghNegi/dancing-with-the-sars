"""Figures for the MonsoonLens reports and slides.

Every number is read from the pipeline output (data/derived, data/reference) or from deliverables/facts.py,
where each outside figure carries its source. Charts come in two themes: "light" for the PDF reports and
"dark" for the slides.

  python deliverables/figures.py          # -> deliverables/out/fig/*.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "deliverables"))
import facts  # noqa: E402

DER, REF = ROOT / "data" / "derived", ROOT / "data" / "reference"
LAY = ROOT / "app" / "static" / "layers" / "real"
OUT = ROOT / "deliverables" / "out" / "fig"
OUT.mkdir(parents=True, exist_ok=True)

for f in Path.home().joinpath(".fonts").glob("IBMPlex*.ttf"):
    font_manager.fontManager.addfont(str(f))

# Brand (same as the app)
NAVY, NAVY2, CYAN = "#070c17", "#0b1630", "#6fe3ff"
WATER, WATER_D, PERM, SLIDE, FLOOD = "#3d8ef0", "#1f6fd1", "#b7d3f6", "#f0743a", "#2f6fd0"
GREY = "#8a9bb0"

THEMES = {
    "light": dict(bg="#ffffff", ink="#10213a", muted="#5d6b75", grid="#e3e9f0", panel="#f4f7fb"),
    "dark": dict(bg=NAVY2, ink="#e8eef7", muted="#9fb0c6", grid="#22314d", panel="#101d3a"),
}

M = json.loads((DER / "metrics.json").read_text())
FB = json.loads((DER / "flood_baseline.json").read_text())


def style(theme):
    t = THEMES[theme]
    plt.rcParams.update({
        "font.family": "IBM Plex Sans", "font.size": 11, "axes.edgecolor": t["grid"], "axes.labelcolor": t["ink"],
        "xtick.color": t["muted"], "ytick.color": t["muted"], "text.color": t["ink"], "axes.facecolor": t["bg"],
        "figure.facecolor": t["bg"], "savefig.facecolor": t["bg"], "axes.spines.top": False,
        "axes.spines.right": False, "axes.grid": False, "axes.titleweight": "semibold", "axes.titlesize": 13,
        "axes.titlelocation": "left", "legend.frameon": False,
    })
    return t


def save(fig, name, theme):
    p = OUT / f"{name}_{theme}.png"
    fig.savefig(p, dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return p


def cond(text):
    return dict(fontfamily="IBM Plex Sans Condensed", fontweight="bold", text=text)


# ---------------------------------------------------------------- map of the findings
def _grid():
    import rasterio
    with rasterio.open(DER / "geotiff" / "new_water.tif") as r:
        return r.transform, r.crs, r.width, r.height


def _to_px(lons, lats):
    from pyproj import Transformer
    tf, crs, w, h = _grid()
    x, y = Transformer.from_crs("EPSG:4326", crs, always_xy=True).transform(lons, lats)
    col = (np.asarray(x) - tf.c) / tf.a
    row = (np.asarray(y) - tf.f) / tf.e
    return col, row


def _rgba(name, color=None, alpha=1.0):
    im = np.asarray(Image.open(LAY / name).convert("RGBA")).astype(float) / 255
    if color:
        c = matplotlib.colors.to_rgb(color)
        im[..., :3] = c
        im[..., 3] = (im[..., 3] > 0) * alpha
    return im


def map_findings(theme):
    t = style(theme)
    hh = np.asarray(Image.open(LAY / "hh_after.webp").convert("L")).astype(float) / 255
    tf, crs, w, h = _grid()
    fig, ax = plt.subplots(figsize=(8.6, 8.4))
    ax.imshow(hh, cmap="gray", vmin=0.02, vmax=0.95, interpolation="lanczos")
    ax.imshow(np.where(hh[..., None] >= 0, 0, 0) * 0 + np.array([[[0.03, 0.05, 0.1, 0.35]]]), extent=(0, hh.shape[1], hh.shape[0], 0))
    for name, color, a in (("permanent.png", PERM, 0.75), ("rise.png", WATER, 1.0), ("flood.png", "#ffffff", 1.0)):
        ax.imshow(_rgba(name, color, a), interpolation="nearest")
    zones = json.loads((DER / "slide_zones.geojson").read_text())["features"]
    zp = pd.DataFrame([f["properties"] for f in zones])
    cx, cy = _to_px(zp["lon"].values, zp["lat"].values)
    size = zp["confidence"].map({"high": 90, "medium": 50, "low": 26})
    ax.scatter(cx, cy, s=size, c=SLIDE, edgecolors="white", linewidths=0.8, zorder=5)
    ev = json.loads((REF / "events.geojson").read_text())["features"]
    ex, ey = _to_px([f["geometry"]["coordinates"][0] for f in ev], [f["geometry"]["coordinates"][1] for f in ev])
    ax.scatter(ex, ey, s=46, marker="^", c="#ffffff", edgecolors="#10213a", linewidths=0.9, zorder=6)
    places = {"Pune": (73.8567, 18.5204), "Pimpri-Chinchwad": (73.8, 18.6298), "Lonavala": (73.4072, 18.7546),
              "Mulshi": (73.515, 18.522), "Talegaon": (73.6757, 18.7353), "Khopoli": (73.3433, 18.7896)}
    px, py = _to_px([v[0] for v in places.values()], [v[1] for v in places.values()])
    for (name, _), x, y in zip(places.items(), px, py):
        if 0 <= x < w and 0 <= y < h:
            ax.text(x + 18, y - 14, name, fontsize=9.5, color="white", fontweight="semibold",
                    path_effects=[matplotlib.patheffects.withStroke(linewidth=2.6, foreground="#0b1630")])
    # scale bar (10 km) and north arrow
    px10 = 10000 / tf.a
    x0, y0 = w * 0.06, h * 0.95
    ax.add_patch(Rectangle((x0, y0 - 12), px10, 12, color="white", zorder=7))
    ax.text(x0 + px10 / 2, y0 - 26, "10 km", ha="center", color="white", fontsize=9, fontweight="semibold", zorder=7)
    ax.annotate("N", xy=(w * 0.94, h * 0.06), xytext=(w * 0.94, h * 0.14), color="white", ha="center",
                fontsize=11, fontweight="bold", arrowprops=dict(arrowstyle="-|>", color="white", lw=1.6))
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    from matplotlib.lines import Line2D
    handles = [
        Rectangle((0, 0), 1, 1, color=PERM, label="Rivers and reservoirs (JRC)"),
        Rectangle((0, 0), 1, 1, color=WATER, label=f"New water as reservoirs rose: {M['water']['rise_km2']:.1f} km²"),
        Rectangle((0, 0), 1, 1, color="white", ec="#10213a", label=f"Flood water on dry land: {M['water']['flood_km2']:.2f} km²"),
        Line2D([], [], marker="o", ls="", mfc=SLIDE, mec="white", ms=8,
               label=f"Likely slide zone ({M['slides']['zones']}, {M['slides']['high']} high confidence)"),
        Line2D([], [], marker="^", ls="", mfc="white", mec="#10213a", ms=8, label=f"Reported event ({M['validation']['events']})"),
    ]
    leg = ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.01), ncol=2, fontsize=9,
                    handlelength=1.4, columnspacing=1.2, labelcolor=t["ink"])
    ax.set_title("NISAR L-band radar, 10 July 2026 (HH), with the changes since 28 June", color=t["ink"], pad=8)
    return save(fig, "map_findings", theme)


# ---------------------------------------------------------------- before / after crops
def before_after(theme):
    t = style(theme)
    nw = np.asarray(Image.open(LAY / "new_water.png").convert("RGBA"))[..., 3] > 0
    sl = np.asarray(Image.open(LAY / "slide_raster.png").convert("RGBA"))[..., 3] > 0
    a = nw | sl
    size, s = 560, 8
    small = a[: a.shape[0] // s * s, : a.shape[1] // s * s].reshape(a.shape[0] // s, s, a.shape[1] // s, s).sum((1, 3))
    k = size // s
    cs = small.cumsum(0).cumsum(1)
    win = cs[k:, k:] - cs[:-k, k:] - cs[k:, :-k] + cs[:-k, :-k]
    r, c = np.unravel_index(np.argmax(win), win.shape)
    r, c = int(r * s), int(c * s)
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.3))
    for ax, (f, title) in zip(axs, (("hh_before.webp", "NISAR HH, 28 June"), ("hh_after.webp", "NISAR HH, 10 July"),
                                    ("change.webp", "Change in HH (blue darker, red brighter)"))):
        im = Image.open(LAY / f).convert("RGBA").crop((c, r, c + size, r + size))
        bg = Image.new("RGBA", im.size, (20, 26, 32, 255))
        bg.alpha_composite(im)
        ax.imshow(bg)
        ax.set_title(title, fontsize=11, color=t["ink"])
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    o = np.asarray(Image.open(LAY / "new_water.png").convert("RGBA").crop((c, r, c + size, r + size))).astype(float) / 255
    o[..., :3] = matplotlib.colors.to_rgb(CYAN)
    o[..., 3] = (o[..., 3] > 0) * 0.9
    axs[1].imshow(o)
    fig.text(0.01, -0.02, f"{size * 0.04:.0f} km across. Dark = smooth (water), bright = rough (forest, buildings). Cyan on the "
             "10 July image: new open water mapped by MonsoonLens.", fontsize=9, color=t["muted"])
    return save(fig, "before_after", theme)


# ---------------------------------------------------------------- rain
def rain(theme):
    t = style(theme)
    df = pd.read_csv(REF / "rainfall.csv", parse_dates=["date"])
    df = df[(df["date"] >= "2026-06-15") & (df["date"] <= "2026-07-31")]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.bar(df["date"], df["precip_mm"], width=0.8, color=WATER)
    for d, lab in (("2026-06-28", "radar pass 1 (28 Jun)"), ("2026-07-10", "radar pass 2 (10 Jul)")):
        ax.axvline(pd.Timestamp(d), color=t["ink"], ls=(0, (3, 3)), lw=1.1)
        ax.text(pd.Timestamp(d), ax.get_ylim()[1] * 0.98, " " + lab, fontsize=9, va="top", color=t["ink"])
    ax.axvspan(pd.Timestamp("2026-07-03"), pd.Timestamp("2026-07-08"), color=SLIDE, alpha=0.13, lw=0)
    ax.text(pd.Timestamp("2026-07-05"), ax.get_ylim()[1] * 0.80, "floods and\nlandslides\nreported", fontsize=8.5,
            color=SLIDE, ha="center", va="top")
    ax.set_ylabel("mm per day (area average)")
    ax.yaxis.grid(True, color=t["grid"], lw=0.7)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b"))
    ax.set_title("Daily rain over the study area, NASA GPM IMERG (Late Run)", color=t["ink"])
    return save(fig, "rain", theme)


# ---------------------------------------------------------------- checks
def checks(theme):
    t = style(theme)
    xt, dc = M["crosstrack"], M["dem_check"]
    fig, axs = plt.subplots(1, 4, figsize=(15, 3.9), gridspec_kw=dict(wspace=0.55))
    # 1 NASADEM by confidence
    ax = axs[0]
    labs = ["High", "Medium", "Low"]
    kept = [dc["by_confidence"][k]["found"] for k in ("high", "medium", "low")]
    tot = [dc["by_confidence"][k]["zones"] for k in ("high", "medium", "low")]
    ax.barh(labs, tot, color=t["grid"], height=0.6)
    ax.barh(labs, kept, color=SLIDE, height=0.6)
    for i, (k, n) in enumerate(zip(kept, tot)):
        ax.text(n + 0.6, i, f"{k} of {n}", va="center", fontsize=10, color=t["ink"])
    ax.invert_yaxis()
    ax.set_xlim(0, max(tot) * 1.45)
    ax.set_title(f"NASADEM keeps {dc['found']} of {dc['zones_main']}", color=t["ink"])
    ax.set_xlabel("slide zones by confidence")
    # 2 second orbit
    ax = axs[1]
    vals = [xt["real"]["confirmed"] * 100, xt["chance"]["confirmed"] * 100]
    ax.bar(["NISAR zones", "Random steep\nplaces"], vals, color=[WATER, GREY], width=0.6)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.4, f"{v:.1f}%", ha="center", fontsize=10.5, color=t["ink"], fontweight="semibold")
    ax.set_ylim(0, max(vals) * 1.3)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
    ax.set_title(f"Second orbit: {xt['lift_confirmed']:.0f}× chance", color=t["ink"])
    ax.set_ylabel("found again by track 106")
    ax.text(0.5, -0.32, f"{xt['status_counts']['confirmed']} of {xt['real']['zones_scored']} zones in view; "
            f"p ≈ {xt['p_value']:.3f}; {xt['chance']['trials']} random trials", transform=ax.transAxes, ha="center",
            fontsize=8.5, color=t["muted"])
    # 3 floods vs chance
    ax = axs[2]
    ref = FB["reference"]
    vals = [FB["observed"]["matched"], ref["flat_ground"]["expected_matches"], ref["settlements"]["expected_matches"]]
    ax.bar(["Reported\nfloods", "Random\nflat land", "Random\ntowns"], vals, color=[WATER, GREY, GREY], width=0.6)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.15, f"{v:.1f}" if v % 1 else f"{v:.0f}", ha="center", fontsize=10.5, color=t["ink"], fontweight="semibold")
    ax.set_ylim(0, 10)
    ax.set_title("Floods: no better than chance", color=t["ink"])
    ax.set_ylabel(f"matches out of {FB['observed']['of']}")
    # 4 sensitivity
    ax = axs[3]
    rows = M["sensitivity"]["range"]
    base = M["sensitivity"]["base"]
    items = [("Reservoir rise", rows["rise_km2"], base["rise_km2"], WATER), ("Flood water", rows["flood_km2"], base["flood_km2"], WATER_D)]
    for i, (lab, (lo, hi), b, col) in enumerate(items):
        ax.plot([lo, hi], [i, i], color=col, lw=6, solid_capstyle="round")
        ax.plot([b], [i], "o", color="white", mec=col, ms=9, mew=2)
        ax.text(hi + 0.35, i, f"{lo:.2g} – {hi:.3g} km²", va="center", fontsize=9.5, color=t["ink"])
    ax.set_yticks([0, 1])
    ax.set_yticklabels([x[0] for x in items])
    ax.set_xlim(0, 15)
    ax.set_ylim(-0.6, 1.6)
    ax.invert_yaxis()
    ax.set_title("Water threshold ±1 dB", color=t["ink"])
    ax.set_xlabel("km² (dot: chosen threshold)")
    return save(fig, "checks", theme)


# ---------------------------------------------------------------- reservoirs through the season
def season(theme):
    t = style(theme)
    df = pd.read_csv(DER / "timeline.csv", parse_dates=["date"])
    df = df[df["same_mode_as_primary"]]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(df["date"], df["water_in_jrc_extent_km2"], "-o", color=WATER, lw=2.4, ms=7, mfc="white", mew=2)
    for d, v in zip(df["date"], df["water_in_jrc_extent_km2"]):
        ax.text(d, v + 4, f"{v:.0f}", ha="center", fontsize=9.5, color=t["ink"])
    ax.set_ylabel("water surface, km²")
    ax.yaxis.grid(True, color=t["grid"], lw=0.7)
    ax.set_axisbelow(True)
    ax.set_ylim(0, df["water_in_jrc_extent_km2"].max() * 1.25)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b"))
    ax.set_title("Pune's rivers and reservoirs on every same-mode NISAR pass", color=t["ink"])
    return save(fig, "season", theme)


# ---------------------------------------------------------------- evidence chips for one zone
def chips(theme):
    t = style(theme)
    zones = [f["properties"] for f in json.loads((DER / "slide_zones.geojson").read_text())["features"]]
    z = next(p for p in sorted(zones, key=lambda p: -p["score"]) if p["confidence"] == "high" and p.get("nasadem") == "found")
    cd = LAY / "chips"
    files = [cd / f"{z['id']}_{k}.webp" for k in ("before", "after", "coh")]
    if not all(f.exists() for f in files):
        files = [cd / f"{z['id']}_{k}.webp" for k in ("before", "after", "coherence")]
    fig, axs = plt.subplots(1, 3, figsize=(9, 3.4))
    for ax, f, lab in zip(axs, files, ("28 June", "10 July", "Coherence (dark = changed)")):
        if f.exists():
            ax.imshow(Image.open(f).convert("RGB"))
        ax.set_title(lab, fontsize=10.5, color=t["ink"])
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.suptitle(f"{z['id']} near {z['near']}: slope {z['slope_deg']:.0f}°, score {z['score']:.2f}, high confidence, "
                 f"kept with NASADEM", fontsize=11.5, color=t["ink"], x=0.01, ha="left", y=1.02)
    return save(fig, "chips", theme)


# ---------------------------------------------------------------- business: problem in numbers
def cost_to_cover(theme):
    """Compute cost of one full pass over growing areas, from the measured pipeline runtime."""
    t = style(theme)
    tile = facts.TILE_KM2
    per = facts.COST_PER_TILE_RUN_USD
    areas = [("Study area\n(Pune)", tile), ("Western Ghats\n& Konkan hills", facts.WGHATS_PRONE_KM2),
             ("India, all\nlandslide-prone", facts.INDIA_PRONE_KM2), ("All land\non Earth", facts.EARTH_LAND_KM2)]
    runs_per_year = facts.RUNS_PER_YEAR
    vals = [max(1, a / tile) * per * runs_per_year for _, a in areas]
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    bars = ax.bar([a for a, _ in areas], vals, color=[CYAN, WATER, WATER_D, SLIDE], width=0.62)
    ax.set_yscale("log")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.25, f"${v:,.0f}" if v >= 10 else f"${v:,.2f}", ha="center",
                fontsize=11, color=t["ink"], fontweight="semibold")
    ax.set_ylim(min(vals) / 3, max(vals) * 8)
    ax.set_ylabel("compute cost per year, USD (log)")
    ax.yaxis.grid(True, color=t["grid"], lw=0.6, which="major")
    ax.set_axisbelow(True)
    ax.set_title(f"Cloud compute to run MonsoonLens on every NISAR pass for a year ({runs_per_year} runs per area)",
                 color=t["ink"], fontsize=12)
    return save(fig, "cost_to_cover", theme)


def funding(theme):
    t = style(theme)
    items = [("State Disaster Response Fund (SDRF)", facts.SDRF_CR), ("State Disaster Mitigation Fund (SDMF)", facts.SDMF_CR),
             ("National Disaster Risk Mgmt Fund (NDRMF)", facts.NDRMF_CR)]
    fig, ax = plt.subplots(figsize=(8.6, 2.9))
    y = np.arange(len(items))
    vals = [v / 1000 for _, v in items]
    ax.barh(y, vals, color=[WATER_D, CYAN, WATER], height=0.55)
    for i, v in enumerate(vals):
        ax.text(v + 1.5, i, f"₹{items[i][1]:,} crore", va="center", fontsize=10, color=t["ink"])
    ax.set_yticks(y)
    ax.set_yticklabels([n for n, _ in items])
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.4)
    ax.set_xlabel("₹ thousand crore, 2021–26 (15th Finance Commission)")
    ax.set_title("India's disaster-management budget already exists", color=t["ink"])
    return save(fig, "funding", theme)


def revenue(theme):
    t = style(theme)
    yrs = [p["year"] for p in facts.PLAN]
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    w = 0.38
    x = np.arange(len(yrs))
    rev = [p["revenue_k"] for p in facts.PLAN]
    grants = [p["grants_k"] for p in facts.PLAN]
    cost = [p["cost_k"] for p in facts.PLAN]
    ax.bar(x - w / 2, rev, w, color=WATER, label="Subscriptions and services")
    ax.bar(x - w / 2, grants, w, bottom=rev, color=CYAN, label="Grants and public funding")
    ax.bar(x + w / 2, cost, w, color=GREY, label="Operating cost")
    for i in range(len(yrs)):
        top = max(p["revenue_k"] + p["grants_k"] for p in facts.PLAN)
        ax.text(x[i] - w / 2, rev[i] + grants[i] + top * 0.02, f"${rev[i] + grants[i]:,}k", ha="center", va="bottom",
                fontsize=8.5, color=t["ink"])
        ax.text(x[i] + w / 2, cost[i] + top * 0.02, f"${cost[i]:,}k", ha="center", va="bottom", fontsize=8.5, color=t["muted"])
    ax.set_ylim(0, max(p["revenue_k"] + p["grants_k"] for p in facts.PLAN) * 1.15)
    ax.set_xticks(x)
    ax.set_xticklabels(yrs)
    ax.set_ylabel("USD thousand")
    ax.yaxis.grid(True, color=t["grid"], lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=9, labelcolor=t["ink"])
    ax.set_title("Five-year plan (planning assumptions, not forecasts)", color=t["ink"])
    return save(fig, "revenue", theme)


def coverage(theme):
    t = style(theme)
    yrs = [p["year"] for p in facts.PLAN]
    km2 = [p["coverage_mkm2"] for p in facts.PLAN]
    districts = [p["districts"] for p in facts.PLAN]
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.bar(yrs, km2, color=[CYAN, WATER, WATER, WATER_D, SLIDE], width=0.6)
    for i, (v, d) in enumerate(zip(km2, districts)):
        ax.text(i, v * 1.15, f"{v:g} M km²\n{d}", ha="center", fontsize=9, color=t["ink"])
    ax.set_yscale("log")
    ax.set_ylim(min(km2) / 2, max(km2) * 6)
    ax.set_ylabel("area watched, million km² (log)")
    ax.set_title("Coverage plan: from one district to all land", color=t["ink"])
    return save(fig, "coverage", theme)


def roadmap(theme):
    t = style(theme)
    rows = facts.ROADMAP
    fig, ax = plt.subplots(figsize=(10, 0.55 * len(rows) + 1.1))
    for i, (lane, label, a, b, color) in enumerate(rows):
        ax.add_patch(FancyBboxPatch((a, i - 0.32), b - a, 0.64, boxstyle="round,pad=0,rounding_size=0.18",
                                    color={"cyan": CYAN, "blue": WATER, "deep": WATER_D, "orange": SLIDE}[color], lw=0))
        fits = len(label) * 0.052 < (b - a) - 0.1
        ax.text(a + 0.08 if fits else b + 0.06, i, label, va="center", fontsize=9.2,
                color=("#0b1630" if color == "cyan" else "white") if fits else t["ink"], fontweight="semibold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
    ax.set_ylim(len(rows) - 0.4, -0.6)
    qs = facts.ROADMAP_TICKS
    ax.set_xticks(range(len(qs)))
    ax.set_xticklabels(qs, fontsize=9)
    ax.set_xlim(-0.1, len(qs) + 0.2)
    ax.xaxis.grid(True, color=t["grid"], lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Roadmap, Q4 2026 to 2030", color=t["ink"])
    return save(fig, "roadmap", theme)


ALL = [map_findings, before_after, rain, checks, season, chips, cost_to_cover, funding, revenue, coverage, roadmap]

if __name__ == "__main__":
    import matplotlib.patheffects  # noqa: F401
    import matplotlib.dates  # noqa: F401
    import matplotlib.ticker  # noqa: F401
    only = sys.argv[1:]
    for fn in ALL:
        if only and fn.__name__ not in only:
            continue
        for th in ("light", "dark"):
            print(fn(th))
