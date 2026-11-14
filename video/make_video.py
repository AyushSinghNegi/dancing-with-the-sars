"""30-second demo video for the Space Apps submission (English subtitles burnt in, plus an .srt).

Every number and picture comes from the pipeline output in data/derived and data/reference, so
re-running this after the pipeline changes keeps the video honest.

  python video/make_video.py            # -> video/out/monsoonlens_30s.mp4 and .srt
  python video/make_video.py --frames   # only write key frames to video/out/frames/ to check layout

Needs ffmpeg. Fonts: IBM Plex Sans (SIL Open Font License, video/fonts/).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DER = ROOT / "data" / "derived"
REF = ROOT / "data" / "reference"
LAYERS = ROOT / "app" / "static" / "layers" / "real"
FONTS = Path(__file__).resolve().parent / "fonts"
OUT = Path(__file__).resolve().parent / "out"

W, H, FPS = 1920, 1080, 30
BG = (13, 27, 38)
INK = (29, 51, 70)
WHITE = (255, 255, 255)
MUTED = (178, 192, 204)
C_RISE = (109, 167, 236)
C_FLOOD = (28, 92, 171)
C_PERM = (183, 211, 246)
C_SLIDE = (235, 104, 52)
FADE_IN = 12


def font(weight, size):
    return ImageFont.truetype(str(FONTS / f"IBMPlexSans-{weight}.ttf"), size)


class _Fonts(dict):
    def __missing__(self, key):
        self[key] = font(*key)
        return self[key]


F = _Fonts()


# ------------------------------------------------------------------ helpers
def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ramp(i, start, dur):
    return ease((i - start) / dur) if dur else float(i >= start)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def text_block(img, xy, text, fnt, fill, width, line_h=None, alpha=1.0):
    if alpha <= 0:
        return xy[1]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    lh = line_h or int(fnt.size * 1.32)
    for ln in wrap(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=(*fill, int(255 * alpha)))
        y += lh
    img.paste(layer, (0, 0), layer)
    return y


def subtitle(img, text, alpha=1.0):
    """Burnt-in English subtitle, bottom centre, readable on a phone."""
    if alpha <= 0 or not text:
        return
    fnt = F[(500, 40)]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lines = wrap(d, text, fnt, 1560)
    lh = 54
    tw = max(d.textlength(l, font=fnt) for l in lines)
    bh = lh * len(lines) + 26
    x0, y1 = (W - tw) / 2 - 30, H - 34
    y0 = y1 - bh
    d.rounded_rectangle((x0, y0, x0 + tw + 60, y1), radius=14, fill=(6, 14, 21, int(205 * alpha)))
    y = y0 + 11
    for l in lines:
        d.text(((W - d.textlength(l, font=fnt)) / 2, y), l, font=fnt, fill=(255, 255, 255, int(255 * alpha)))
        y += lh
    img.paste(layer, (0, 0), layer)


def blend(a, b, t):
    return Image.blend(a.convert("RGB"), b.convert("RGB"), t)


def fmt(v, d=1):
    return f"{v:,.{d}f}"


# ------------------------------------------------------------------ data
def load():
    m = json.loads((DER / "metrics.json").read_text())
    if m.get("demo"):
        sys.exit("metrics.json is demo data: the video only uses real NISAR results.")
    b = json.loads((DER / "bounds.json").read_text())["bounds_latlon"]
    rain = pd.read_csv(REF / "rainfall.csv", parse_dates=["date"])
    zones = json.loads((DER / "slide_zones.geojson").read_text())["features"]
    water = json.loads((DER / "new_water.geojson").read_text())["features"]
    val = pd.read_csv(DER / "validation.csv")
    return m, b, rain, zones, water, val


class Geo:
    """lon/lat -> pixel on the app's overlay images (plain lat/lon grid)."""

    def __init__(self, bounds, size):
        (self.s, self.w), (self.n, self.e) = bounds
        self.size = size

    def px(self, lon, lat, scale=1.0, off=(0, 0)):
        x = (lon - self.w) / (self.e - self.w) * self.size[0]
        y = (self.n - lat) / (self.n - self.s) * self.size[1]
        return off[0] + x * scale, off[1] + y * scale


def hotspot(size=600, s=8):
    a = np.asarray(Image.open(LAYERS / "new_water.png").convert("RGBA"))[..., 3] > 0
    small = a[: a.shape[0] // s * s, : a.shape[1] // s * s].reshape(a.shape[0] // s, s, a.shape[1] // s, s).sum((1, 3))
    k = size // s
    cs = small.cumsum(0).cumsum(1)
    win = cs[k:, k:] - cs[:-k, k:] - cs[k:, :-k] + cs[:-k, :-k]
    r, c = np.unravel_index(np.argmax(win), win.shape)
    return int(r * s), int(c * s)


def tint(mask_img, color, alpha=255, grow=0):
    a = np.asarray(mask_img.convert("RGBA"))[..., 3] > 0
    if grow:
        from scipy import ndimage as ndi
        a = ndi.binary_dilation(a, iterations=grow)
    out = np.zeros((*a.shape, 4), np.uint8)
    out[a] = (*color, alpha)
    return Image.fromarray(out, "RGBA")


# ------------------------------------------------------------------ scenes
class Video:
    def __init__(self, data):
        self.m, self.bounds, self.rain, self.zones, self.water, self.val = data
        self.hh_b = Image.open(LAYERS / "hh_before.webp").convert("RGBA")
        self.hh_a = Image.open(LAYERS / "hh_after.webp").convert("RGBA")
        self.geo = Geo(self.bounds, self.hh_a.size)
        self.subs = []          # (start_s, end_s, text) for the .srt
        self.t0 = 0.0
        self._prep_map()

    # ---- shared map (scenes 3 and 4)
    MAP_H = 840
    MAP_XY = (96, 40)

    def _prep_map(self):
        sc = self.MAP_H / self.hh_a.size[1]
        self.map_scale = sc
        size = (round(self.hh_a.size[0] * sc), self.MAP_H)
        base = Image.new("RGBA", self.hh_a.size, (*BG, 255))
        radar = self.hh_a.copy()
        r = np.asarray(radar).astype(float)
        r[..., :3] *= 0.5
        base.alpha_composite(Image.fromarray(r.astype(np.uint8), "RGBA"))
        base.alpha_composite(tint(Image.open(LAYERS / "permanent.png"), C_PERM, 150))
        self.map_base = base.resize(size, Image.LANCZOS)
        rise = tint(Image.open(LAYERS / "rise.png"), C_RISE, 255, grow=3)
        self.map_rise = rise.resize(size, Image.LANCZOS)
        self.map_size = size

    def map_pt(self, lon, lat):
        return self.geo.px(lon, lat, self.map_scale, self.MAP_XY)

    def map_frame(self, rise_a, flood_a, slide_n, labels_a=1.0, dim=1.0):
        img = Image.new("RGB", (W, H), BG)
        img.paste(self.map_base.convert("RGB"), self.MAP_XY)
        if rise_a > 0:
            r = self.map_rise.copy()
            r.putalpha(r.getchannel("A").point(lambda v: int(v * rise_a * dim)))
            img.paste(r, self.MAP_XY, r)
        d = ImageDraw.Draw(img, "RGBA")
        if flood_a > 0:
            for f in self.water:
                if f["properties"]["kind"] != "flood":
                    continue
                x, y = self.map_pt(f["properties"]["lon"], f["properties"]["lat"])
                rr = 7
                d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(*C_FLOOD, int(255 * flood_a * dim)),
                          outline=(255, 255, 255, int(230 * flood_a * dim)), width=2)
        for k, f in enumerate(self.zones[: int(slide_n)]):
            p = f["properties"]
            x, y = self.map_pt(p["lon"], p["lat"])
            rr = 9 if p["confidence"] == "high" else 6
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(*C_SLIDE, int(235 * dim)),
                      outline=(255, 255, 255, int(200 * dim)), width=2 if rr > 6 else 1)
        if labels_a > 0:
            x, y = self.map_pt(73.856, 18.520)
            d.text((x + 10, y - 18), "Pune", font=F[(600, 34)], fill=(255, 255, 255, int(235 * labels_a)))
            x, y = self.map_pt(73.33, 18.86)
            d.text((x, y), "Western Ghats", font=F[(500, 28)], fill=(255, 255, 255, int(200 * labels_a)))
            # scale bar: 10 km
            km = 10_000 / ((self.geo.e - self.geo.w) * 111_320 * math.cos(math.radians(18.5))) * self.map_size[0]
            x0, y0 = self.MAP_XY[0] + 24, self.MAP_XY[1] + self.MAP_H - 36
            d.rectangle((x0, y0, x0 + km, y0 + 5), fill=(255, 255, 255, int(220 * labels_a)))
            d.text((x0 + km + 10, y0 - 14), "10 km", font=F[(400, 26)], fill=(255, 255, 255, int(220 * labels_a)))
        return img

    # ---- scene 1: rain
    def s1(self, i, n):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img, "RGBA")
        r = self.rain[(self.rain.date >= "2026-06-20") & (self.rain.date <= "2026-07-20")].reset_index(drop=True)
        x0, x1, yb, yt, top = 170, 1760, 760, 290, 160.0
        a_hdr = ramp(i, 0, 14)
        text_block(img, (170, 104), "Pune, July 2026", F[(600, 64)], WHITE, 1500, alpha=a_hdr)
        text_block(img, (170, 190), "Rain over the study area, mm per day (NASA POWER)", F[(400, 30)], MUTED, 1500,
                   alpha=a_hdr)
        for v in (50, 100, 150):
            y = yb - v / top * (yb - yt)
            d.line((x0, y, x1, y), fill=(255, 255, 255, int(28 * a_hdr)), width=1)
            d.text((x0 - 12, y), f"{v}", font=F[(400, 26)], fill=(*MUTED, int(255 * a_hdr)), anchor="rm")
        step = (x1 - x0) / len(r)
        bw = step * 0.7
        for k, row in r.iterrows():
            g = ramp(i, 12 + k * 2.6, 16)
            if g <= 0:
                continue
            h = row.precip_mm / top * (yb - yt) * g
            bx = x0 + k * step + (step - bw) / 2
            d.rounded_rectangle((bx, yb - max(h, 2), bx + bw, yb), radius=4, fill=(*C_RISE, 255))
            d.rectangle((bx, yb - min(max(h, 2), 4), bx + bw, yb), fill=(*C_RISE, 255))
        d.line((x0, yb, x1, yb), fill=(255, 255, 255, 120), width=2)
        for k, row in r.iterrows():
            if row.date.day in (20, 25, 30, 5, 10, 15) or k == len(r) - 1:
                cx = x0 + k * step + step / 2
                d.text((cx, yb + 14), row.date.strftime("%-d %b"), font=F[(400, 26)],
                       fill=(*MUTED, int(255 * a_hdr)), anchor="mt")
        # radar passes used
        a_pass = ramp(i, 100, 20)
        for day in ("2026-06-28", "2026-07-10"):
            k = int(np.flatnonzero(r.date == day)[0])
            cx = x0 + k * step + step / 2
            ty = yb + 56
            d.polygon([(cx, ty), (cx - 11, ty + 18), (cx + 11, ty + 18)], fill=(255, 255, 255, int(255 * a_pass)))
            d.text((cx, ty + 26), "NISAR pass", font=F[(600, 28)], fill=(255, 255, 255, int(255 * a_pass)),
                   anchor="mt")
        # peak label
        a_pk = ramp(i, 118, 18)
        pk = r.loc[r.precip_mm.idxmax()]
        k = int(r.precip_mm.idxmax())
        cx = x0 + k * step + step / 2
        py = yb - pk.precip_mm / top * (yb - yt)
        d.text((cx + 34, py + 8), f"{pk.precip_mm:.0f} mm on {pk.date.strftime('%-d %B')}", font=F[(600, 34)],
               fill=(255, 255, 255, int(255 * a_pk)), anchor="lm")
        return img

    # ---- scene 2: radar swipe on the window with the most new water
    VIEW = 840
    VIEW_XY = (96, 40)

    def _prep_s2(self):
        r, c = hotspot(600)
        crop = lambda im: im.crop((c, r, c + 600, r + 600))
        mk = lambda im: (lambda bg: (bg.alpha_composite(crop(im)), bg)[1])(Image.new("RGBA", (600, 600), (*BG, 255)))
        self.sw_b = mk(self.hh_b).resize((self.VIEW,) * 2, Image.LANCZOS)
        self.sw_a = mk(self.hh_a).resize((self.VIEW,) * 2, Image.LANCZOS)
        nw = tint(crop(Image.open(LAYERS / "new_water.png")), C_RISE, 235)
        self.sw_nw = nw.resize((self.VIEW,) * 2, Image.NEAREST)
        self.sw_km = 600 * 40 / 1000      # window width in km (40 m pixels)

    def s2(self, i, n):
        if not hasattr(self, "sw_b"):
            self._prep_s2()
        img = Image.new("RGB", (W, H), BG)
        V, (vx, vy) = self.VIEW, self.VIEW_XY
        p = ramp(i, 30, 110)                     # swipe progress: 28 June on the left gives way to 10 July
        split = int(V * (1 - p))
        view = self.sw_a.copy()
        if split > 0:
            view.paste(self.sw_b.crop((0, 0, split, V)), (0, 0))
        nw_a = ramp(i, 150, 24)
        if nw_a > 0:
            view = Image.blend(view, Image.new("RGBA", view.size, (*BG, 255)), 0.3 * nw_a)
            o = self.sw_nw.copy()
            o.putalpha(o.getchannel("A").point(lambda v: int(v * nw_a)))
            view.alpha_composite(o)
        img.paste(view.convert("RGB"), (vx, vy))
        d = ImageDraw.Draw(img, "RGBA")
        if 0 < p < 1:
            x = vx + split
            d.line((x, vy, x, vy + V), fill=(255, 255, 255, 255), width=4)
            d.ellipse((x - 20, vy + V / 2 - 20, x + 20, vy + V / 2 + 20), fill=(255, 255, 255, 255))
            d.polygon([(x - 6, vy + V / 2), (x - 13, vy + V / 2 - 7), (x - 13, vy + V / 2 + 7)], fill=(*INK, 255))
            d.polygon([(x + 6, vy + V / 2), (x + 13, vy + V / 2 - 7), (x + 13, vy + V / 2 + 7)], fill=(*INK, 255))
        for label, side, show in (("28 June", "l", split > 0.15 * V), ("10 July", "r", split < 0.85 * V)):
            if not show:
                continue
            tw = d.textlength(label, font=F[(600, 34)])
            bx = vx + 18 if side == "l" else vx + V - 18 - tw - 32
            d.rounded_rectangle((bx, vy + 18, bx + tw + 32, vy + 70), radius=10, fill=(6, 14, 21, 210))
            d.text((bx + 16, vy + 24), label, font=F[(600, 34)], fill=WHITE)
        # 5 km scale bar
        px5 = 5 / self.sw_km * V
        sx, sy = vx + 24, vy + V - 40
        d.rounded_rectangle((sx - 12, sy - 20, sx + px5 + 84, sy + 22), radius=8, fill=(6, 14, 21, 190))
        d.rectangle((sx, sy, sx + px5, sy + 6), fill=(255, 255, 255, 230))
        d.text((sx + px5 + 10, sy - 13), "5 km", font=F[(400, 26)], fill=(255, 255, 255, 230))
        tx = vx + V + 84
        a = ramp(i, 4, 16)
        y = text_block(img, (tx, 120), "Radar sees through cloud", F[(600, 56)], WHITE, 760, alpha=a)
        y = text_block(img, (tx, y + 18), "NASA and ISRO's NISAR satellite, L-band radar. Dark means smooth: "
                       "open water. Bright means rough: slopes, trees, buildings.", F[(400, 32)], MUTED, 740,
                       line_h=46, alpha=ramp(i, 14, 16))
        if nw_a > 0:
            y += 46
            d = ImageDraw.Draw(img, "RGBA")
            d.rectangle((tx, y + 6, tx + 30, y + 36), fill=(*C_RISE, int(255 * nw_a)))
            text_block(img, (tx + 48, y), "Blue: ground that was dry on 28 June and under water on 10 July, beyond the usual shoreline",
                       F[(500, 28)], WHITE, 690, line_h=40, alpha=nw_a)
        return img

    # ---- scene 3: what changed, whole box
    def s3(self, i, n):
        w = self.m["water"]
        sz = self.m["slides"]
        rise_a, flood_a = ramp(i, 16, 30), ramp(i, 66, 24)
        slide_n = len(self.zones) * ramp(i, 110, 60)
        img = self.map_frame(rise_a, flood_a, slide_n, labels_a=ramp(i, 0, 14))
        tx, y = 1100, 96
        rows = [
            (C_RISE, w["rise_km2"], 1, " km²", "of new water as Pune's reservoirs and rivers rose", 16),
            (C_FLOOD, w["flood_km2"], 2, " km²", "of flood water still standing where no water was recorded "
                                                 "since 1984", 66),
            (C_SLIDE, sz["zones"], 0, "", f"likely slide zones on steep slopes, {sz['high']} of them high "
                                          "confidence", 110),
        ]
        d = ImageDraw.Draw(img, "RGBA")
        for color, val, dig, unit, text, start in rows:
            a = ramp(i, start, 16)
            if a <= 0:
                y += 236
                continue
            cnt = val * ramp(i, start, 36)
            d.rectangle((tx, y + 30, tx + 24, y + 54), fill=(*color, int(255 * a)))
            num = fmt(cnt, dig)
            d.text((tx + 46, y), num, font=F[(600, 92)], fill=(255, 255, 255, int(255 * a)))
            if unit:
                d.text((tx + 46 + d.textlength(fmt(val, dig), font=F[(600, 92)]) + 8, y + 44), unit.strip(),
                       font=F[(500, 40)], fill=(*MUTED, int(255 * a)))
            text_block(img, (tx + 46, y + 116), text, F[(400, 30)], MUTED, 700, line_h=42, alpha=a)
            d = ImageDraw.Draw(img, "RGBA")
            y += 236
        return img

    # ---- scene 4: checked against reports
    def s4(self, i, n):
        img = self.map_frame(1, 1, len(self.zones), labels_a=1, dim=0.55)
        d = ImageDraw.Draw(img, "RGBA")
        obs = self.val[self.val.observable == "yes"]
        hits = obs[obs.result == "hit"]
        for k, row in enumerate(obs.itertuples()):
            a = ramp(i, 10 + k * 3, 10)
            if a <= 0:
                continue
            x, y = self.map_pt(row.lon, row.lat)
            rr = 13
            if row.result == "hit":
                d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 255, 255, int(255 * a)),
                          outline=(*INK, int(255 * a)), width=2)
                d.line([(x - 6, y), (x - 1, y + 5), (x + 7, y - 5)], fill=(*INK, int(255 * a)), width=3)
            else:
                d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 255, 255, int(255 * a)), width=3)
        tx = 1100
        a = ramp(i, 4, 16)
        cnt = int(round(len(hits) * ramp(i, 20, 40)))
        d.text((tx, 96), f"{cnt} of {len(obs)}", font=F[(600, 92)], fill=(255, 255, 255, int(255 * a)))
        y = text_block(img, (tx, 214), "reported floods and landslides that the radar could observe had a "
                       "detection nearby", F[(400, 32)], MUTED, 700, line_h=44, alpha=a)
        d = ImageDraw.Draw(img, "RGBA")
        a2 = ramp(i, 40, 16)
        y += 30
        d.ellipse((tx, y + 8, tx + 26, y + 34), fill=(255, 255, 255, int(255 * a2)))
        d.text((tx + 44, y + 2), "matched", font=F[(500, 28)], fill=(255, 255, 255, int(255 * a2)))
        d.ellipse((tx + 220, y + 8, tx + 246, y + 34), outline=(255, 255, 255, int(255 * a2)), width=3)
        d.text((tx + 264, y + 2), "missed, with the reason", font=F[(500, 28)], fill=(255, 255, 255, int(255 * a2)))
        y += 76
        xt = self.m.get("crosstrack") or {}
        sc = xt.get("status_counts") or {}
        scored = sum(sc.get(k, 0) for k in ("confirmed", "partial", "not seen"))
        lift = xt.get("lift_confirmed")
        lines = ["Most flood water drained before the radar came back on 10 July; we say so in the app."]
        if scored and lift and lift >= 2:
            lines.append(f"A second NISAR track found {sc['confirmed']} of {scored} slide zones again, "
                         f"{lift:.0f}× more often than chance.")
        for k, ln in enumerate(lines):
            y = text_block(img, (tx, y), ln, F[(400, 30)], MUTED, 700, line_h=42, alpha=ramp(i, 60 + 24 * k, 16))
            y += 18
        return img

    # ---- scene 5: end card
    def s5(self, i, n):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img, "RGBA")
        a = ramp(i, 0, 18)
        d.text((W / 2, 300), "MonsoonLens", font=F[(700, 128)], fill=(255, 255, 255, int(255 * a)), anchor="mm")
        d.text((W / 2, 410), "Floods and landslides under the monsoon cloud, mapped with NISAR radar",
               font=F[(400, 34)], fill=(*MUTED, int(255 * a)), anchor="mm")
        a2 = ramp(i, 12, 18)
        url = "monsoonlens.streamlit.app"
        tw = d.textlength(url, font=F[(600, 56)])
        d.rounded_rectangle((W / 2 - tw / 2 - 36, 486, W / 2 + tw / 2 + 36, 576), radius=45,
                            fill=(*C_RISE, int(255 * a2)))
        d.text((W / 2, 531), url, font=F[(600, 56)], fill=(*BG, int(255 * a2)), anchor="mm")
        a3 = ramp(i, 24, 18)
        d.text((W / 2, 650), "Team iGenfinity, NASA Space Apps Challenge 2026", font=F[(600, 34)],
               fill=(255, 255, 255, int(255 * a3)), anchor="mm")
        d.text((W / 2, 712), "NISAR data: NASA and ISRO via ASF DAAC. Rain: NASA POWER. Water history: JRC. "
               "Terrain: Copernicus DEM.", font=F[(400, 26)], fill=(*MUTED, int(255 * a3)), anchor="mm")
        return img


SCENES = [  # (method, frames, subtitle)
    ("s1", 180, "Early July 2026: days of extreme rain over Pune. Thick cloud hid the ground from ordinary "
                "satellites."),
    ("s2", 210, "NISAR's radar sees through cloud. Between 28 June and 10 July, Pune's reservoirs spread."),
    ("s3", 210, "We mapped what changed: rising reservoirs, flood water still standing, and slopes that gave way."),
    ("s4", 165, "Every result is checked against news reports, and the app shows what radar missed, and why."),
    ("s5", 120, "Open the map, see every source, and check it yourself."),
]


def run(frames_only=False):
    v = Video(load())
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "frames").mkdir(exist_ok=True)
    parts, t, prev_last = [], 0.0, None
    srt = []
    for idx, (name, n, sub) in enumerate(SCENES, start=1):
        fn = getattr(v, name)
        if frames_only:
            for i in sorted({0, n // 3, (2 * n) // 3, n - 1}):
                im = fn(i, n)
                subtitle(im, sub)
                im.convert("RGB").save(OUT / "frames" / f"{name}_{i:03d}.jpg", quality=90)
            continue
        tmp, final = OUT / f".scene{idx}.tmp.mp4", OUT / f"scene{idx}.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18",
                               "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), str(tmp)],
                              stdin=subprocess.PIPE)
        last = None
        for i in range(n):
            im = fn(i, n)
            sa = min(ramp(i, 4, 8), 1 - ramp(i, n - 8, 8)) if idx < len(SCENES) else ramp(i, 4, 8)
            subtitle(im, sub, sa)
            if prev_last is not None and i < FADE_IN:
                im = blend(prev_last, im, ease((i + 1) / FADE_IN))
            ff.stdin.write(im.convert("RGB").tobytes())
            last = im
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit(f"ffmpeg failed on {name}")
        os.replace(tmp, final)
        parts.append(final)
        prev_last = last
        srt.append((t + 4 / FPS, t + n / FPS - 4 / FPS, sub))
        t += n / FPS
        print(f"[video] {name}: {n} frames", flush=True)
    if frames_only:
        print(f"[video] key frames in {OUT / 'frames'}")
        return
    lst = OUT / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    tmp, final = OUT / ".monsoonlens_30s.tmp.mp4", OUT / "monsoonlens_30s.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", str(tmp)], check=True)
    os.replace(tmp, final)

    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    (OUT / "monsoonlens_30s.en.srt").write_text(
        "".join(f"{k}\n{ts(a)} --> {ts(b)}\n{txt}\n\n" for k, (a, b, txt) in enumerate(srt, start=1)))
    print(f"[video] {final} ({t:.1f} s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", action="store_true")
    run(ap.parse_args().frames)
