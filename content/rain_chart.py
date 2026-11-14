"""Rain chart for the pitch deck: GPM IMERG daily rain over the study area, 20 June to 20 July 2026,
with the two NISAR passes and the days NASA's daily satellite images saw only cloud.

  python content/rain_chart.py        # -> content/img/rain_chart.png (3328 x 1040, shown at 1664 x 520)

Every value comes from data/reference/rainfall.csv and data/reference/cloud_check.json.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "data" / "reference"
FONTS = ROOT / "video" / "fonts"
OUT = ROOT / "content" / "img" / "rain_chart.png"

S = 2                                  # drawn at twice the size it is shown
W, H = 1664 * S, 520 * S
NIGHT, PAPER, NOTE, WATER = (13, 27, 38), (243, 245, 244), (143, 163, 179), (109, 167, 236)
PASSES = ("2026-06-28", "2026-07-10")


def font(weight, size):
    return ImageFont.truetype(str(FONTS / f"IBMPlexSans-{weight}.ttf"), size * S)


def main():
    rain = pd.read_csv(REF / "rainfall.csv", parse_dates=["date"])
    assert "IMERG" in str(rain["source"].iloc[0]), "rainfall.csv is not GPM IMERG"
    r = rain[(rain.date >= "2026-06-20") & (rain.date <= "2026-07-20")].reset_index(drop=True)
    cloud = json.loads((REF / "cloud_check.json").read_text())

    img = Image.new("RGB", (W, H), NIGHT)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, yb, yt = 80 * S, 1650 * S, 420 * S, 70 * S
    top = 50.0 * math.ceil(r.precip_mm.max() / 50 + 0.15)
    y = lambda v: yb - v / top * (yb - yt)
    step = (x1 - x0) / len(r)
    cx = lambda k: x0 + k * step + step / 2

    # cloud band first, so bars paint over it
    if cloud.get("all_cloud") and cloud["all_cloud"] == cloud.get("images_available"):
        k0 = int(np.flatnonzero(r.date == cloud["from"])[0])
        k1 = int(np.flatnonzero(r.date == cloud["to"])[0])
        bx0, bx1 = x0 + k0 * step, x0 + (k1 + 1) * step
        d.rectangle((bx0, yt - 30 * S, bx1, yb), fill=(255, 255, 255, 20))
        d.line((bx0, yt - 30 * S, bx1, yt - 30 * S), fill=(255, 255, 255, 150), width=2 * S)
        d.text((bx0, yt - 38 * S), f"3 to 8 July: all {cloud['images_available']} NASA daily satellite images "
               "show only cloud", font=font(500, 26), fill=PAPER, anchor="lb")

    for v in range(50, int(top), 50):
        d.line((x0, y(v), x1, y(v)), fill=(255, 255, 255, 30), width=S)
        d.text((x0 - 14 * S, y(v)), f"{v}", font=font(400, 24), fill=NOTE, anchor="rm")
    d.text((4 * S, yt - 6 * S), "mm per day", font=font(400, 24), fill=NOTE, anchor="lm")

    bw = step * 0.7
    for k, row in r.iterrows():
        h = max(row.precip_mm / top * (yb - yt), 2 * S)
        bx = x0 + k * step + (step - bw) / 2
        d.rounded_rectangle((bx, yb - h, bx + bw, yb), radius=4 * S, fill=WATER)
        d.rectangle((bx, yb - min(h, 4 * S), bx + bw, yb), fill=WATER)
    d.line((x0, yb, x1, yb), fill=(255, 255, 255, 120), width=2 * S)

    for k, row in r.iterrows():
        if row.date.day in (20, 25, 30, 5, 10, 15):
            d.text((cx(k), yb + 10 * S), row.date.strftime("%-d %b"), font=font(400, 24), fill=NOTE, anchor="mt")
    for day in PASSES:
        k = int(np.flatnonzero(r.date == day)[0])
        ty = yb + 46 * S
        d.polygon([(cx(k), ty), (cx(k) - 10 * S, ty + 16 * S), (cx(k) + 10 * S, ty + 16 * S)], fill=PAPER)
        d.text((cx(k) + 18 * S, ty + 8 * S), "NISAR pass", font=font(600, 26), fill=PAPER, anchor="lm")

    k = int(r.precip_mm.idxmax())
    pk = r.loc[k]
    d.text((cx(k) + bw / 2 + 16 * S, y(pk.precip_mm) + 6 * S),
           f"{pk.precip_mm:.0f} mm on {pk.date.strftime('%-d %B')}", font=font(600, 30), fill=PAPER, anchor="lm")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(f"[rain_chart] {OUT} peak {pk.precip_mm:.0f} mm on {pk.date.date()}")


if __name__ == "__main__":
    main()
