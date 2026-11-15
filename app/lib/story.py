"""Story text from content/story.md with numbers filled from pipeline output."""
from __future__ import annotations

import re
from pathlib import Path

from . import data, ui

CONTENT = Path(__file__).resolve().parents[2] / "content"


def numbers() -> dict:
    v = data.value
    before, after = data.dates()
    fmt_date = ui.date      # one style everywhere: "28 June 2026", "28. Juni 2026", "28 जून 2026"
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
        # what places nobody reported score under the same rule (pipeline/flood_baseline.py)
        "flood_chance": n(((data.flood_baseline() or {}).get("flat") or {}).get("expected_matches"), 1),
        "slide_hits": n(v("validation.slide.hits"), 0),
        "slide_observable": n(v("validation.slide.observable"), 0),
        "before": fmt_date(before), "after": fmt_date(after),
        "crosstrack_sentence": _crosstrack_sentence(fmt_date),
        "cloud_sentence": cloud_sentence(),
        **_timeline_numbers(fmt_date),
    }


def timeline_rows():
    """Same-mode timeline rows, oldest first, or None when there are fewer than 3 dates."""
    tl = data.table("timeline.csv")
    if tl is None or "water_in_jrc_extent_km2" not in tl:
        return None
    tl = tl[tl["same_mode_as_primary"].astype(str).str.lower() == "true"].sort_values("date")
    return tl if len(tl) >= 3 else None


def _timeline_numbers(fmt_date) -> dict:
    tl = timeline_rows()
    if tl is None:
        return {}
    first, peak, last = tl.iloc[0], tl.loc[tl["water_in_jrc_extent_km2"].idxmax()], tl.iloc[-1]
    v = lambda r: ui.fmt_num(r["water_in_jrc_extent_km2"], 0)
    clause = "" if last["date"] == peak["date"] else ui.t("res_last_clause", v=v(last), d=fmt_date(last["date"]))
    return {"res_first": v(first), "res_first_date": fmt_date(first["date"]), "res_peak": v(peak),
            "res_peak_date": fmt_date(peak["date"]), "res_last_clause": clause}


def cloud_sentence() -> str:
    c = data.cloud_check()
    if not c:
        return ""
    return ui.t("cloud_sentence", f=ui.day(c["from"]), t=ui.date(c["to"]), n=c["all_cloud"])


def _crosstrack_sentence(fmt_date) -> str:
    xt = data.crosstrack()
    if not xt:
        return ""
    key = ("xt_story_good_small" if xt["small"] else "xt_story_good") if xt["good"] else "xt_story_weak"
    return ui.t(key, b=fmt_date(xt["pair"]["before"]), a=fmt_date(xt["pair"]["after"]),
                c=ui.fmt_num(xt["confirmed"], 0), n=ui.fmt_num(xt["scored"], 0),
                lift=ui.fmt_num(xt["lift"] or 0, 0), cov=xt["coverage"])


# One key per "## " section of content/story.md, in order; the Story page picks each step's picture by key.
KEYS = ["rain", "cloud", "swipe", "changed", "weeks", "limits"]


def steps() -> list[tuple[str, str, str]]:
    local = CONTENT / f"story.{ui.lang()}.md"
    path = local if ui.lang() != "en" and local.exists() else CONTENT / "story.md"
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    nums = numbers()
    out = []
    for i, p in enumerate(parts):
        head, _, body = p.partition("\n")
        body = " ".join(line.strip() for line in body.strip().splitlines())
        for k, val in nums.items():
            body = body.replace("{" + k + "}", str(val))
        body = re.sub(r"\s{2,}", " ", body).strip()
        key = KEYS[i] if i < len(KEYS) else f"extra{i}"
        if key == "weeks" and "{res_" in body:      # no timeline yet: skip the step rather than show placeholders
            continue
        out.append((head.strip(), body, key))
    return out
