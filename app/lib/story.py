"""Story text from content/story.md with numbers filled from pipeline output."""
from __future__ import annotations

import re
from pathlib import Path

from . import data, ui

CONTENT = Path(__file__).resolve().parents[2] / "content"
MONTHS = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          "mr": ["जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून", "जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर",
                 "नोव्हेंबर", "डिसेंबर"]}


def numbers() -> dict:
    v = data.value
    before, after = data.dates()
    months = MONTHS.get(ui.lang(), MONTHS["en"])
    fmt_date = lambda d: f"{int(d[8:10])} {months[int(d[5:7]) - 1]}"
    def n(x, digits=1):
        return "not available" if x is None else ui.fmt_num(x, digits)
    return {
        "new_water_km2": n(v("water.new_water_km2")),
        "rise_km2": n(v("water.rise_km2")),
        "flood_km2": n(v("water.flood_km2"), 2),
        "flood_patches": n(v("water.flood_patches"), 0),
        "new_water_patches": n(v("water.new_water_patches"), 0),
        "slide_zones": n(v("slides.zones"), 0),
        "slide_high": n(v("slides.high"), 0),
        "brighter_km2": n(v("water.brighter_flat_km2")),
        "flood_hits": n(v("validation.flood.hits"), 0),
        "flood_observable": n(v("validation.flood.observable"), 0),
        "slide_hits": n(v("validation.slide.hits"), 0),
        "slide_observable": n(v("validation.slide.observable"), 0),
        "before": fmt_date(before), "after": fmt_date(after),
        "crosstrack_sentence": _crosstrack_sentence(fmt_date),
        "cloud_sentence": cloud_sentence(),
    }


def cloud_sentence() -> str:
    c = data.cloud_check()
    if not c:
        return ""
    return ui.t("cloud_sentence", f=ui.day(c["from"]), t=ui.day(c["to"]), n=c["all_cloud"])


def _crosstrack_sentence(fmt_date) -> str:
    xt = data.crosstrack()
    if not xt:
        return ""
    key = ("xt_story_good_small" if xt["small"] else "xt_story_good") if xt["good"] else "xt_story_weak"
    return ui.t(key, b=fmt_date(xt["pair"]["before"]), a=fmt_date(xt["pair"]["after"]),
                c=ui.fmt_num(xt["confirmed"], 0), n=ui.fmt_num(xt["scored"], 0),
                lift=ui.fmt_num(xt["lift"] or 0, 0), cov=xt["coverage"])


def steps() -> list[tuple[str, str]]:
    path = CONTENT / ("story.mr.md" if ui.lang() == "mr" and (CONTENT / "story.mr.md").exists() else "story.md")
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    nums = numbers()
    out = []
    for p in parts:
        head, _, body = p.partition("\n")
        body = " ".join(line.strip() for line in body.strip().splitlines())
        for k, val in nums.items():
            body = body.replace("{" + k + "}", str(val))
        body = re.sub(r"\s{2,}", " ", body).strip()
        out.append((head.strip(), body))
    return out
