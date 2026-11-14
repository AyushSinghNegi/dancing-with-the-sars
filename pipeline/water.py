"""R5: one after-date Otsu threshold in linear HH power, applied to both dates.

New water = dark after, not dark before, outside JRC permanent water.
Remove connected patches smaller than four pixels. No slope or minimum-change
rule is added to this brief-defined layer. Brighter-ground evidence is separate.
"""
from __future__ import annotations

import csv

import numpy as np

from . import ancillary
from . import common as K
from . import config as C


def run(write=True):
    d = K.load_pair()
    aux = ancillary.load()
    occ, slope = aux["jrc_occurrence"], aux["slope"]
    perm = np.nan_to_num(occ) >= C.PERMANENT_WATER_OCCURRENCE
    flat = np.nan_to_num(slope, nan=90) <= C.FLOOD_MAX_SLOPE_DEG

    hh_b, hh_a = K.lee_db(d["hh_before"]), K.lee_db(d["hh_after"])
    hv_b, hv_a = K.lee_db(d["hv_before"]), K.lee_db(d["hv_after"])
    valid = np.isfinite(hh_b) & np.isfinite(hh_a) & np.isfinite(occ) & np.isfinite(slope)

    t_a, how_a = K.water_threshold(hh_a)
    t_b, how_b = t_a, how_a
    water_b = valid & (hh_b < t_b)
    water_a = valid & (hh_a < t_a)
    dark_fraction = float(water_a.sum() / valid.sum()) if valid.any() else 1.0
    usable = dark_fraction < C.WATER_MAX_DARK_FRACTION
    ratio = np.where(valid, hh_a - hh_b, np.nan)

    new_water = K.clean(water_a & ~water_b & ~perm)
    receded = K.clean(water_b & ~water_a & ~perm)
    # Bright-up on flat, vegetated or built land: possible water under canopy or in streets.
    brighter = K.clean(valid & (ratio >= C.CHANGE_DB) & flat & ~perm & ~water_a & np.isfinite(hv_b)
                       & (hv_b > -22))

    # Agreement between the permanent-water reference and the radar (sanity check).
    perm_valid = perm & valid
    perm_seen = float(np.mean(water_b[perm_valid])) if perm_valid.any() else float("nan")

    # Vary the single shared threshold for BOTH dates by ±1 dB.
    sensitivity = []
    for offset in (-1.0, 0.0, 1.0):
        mask = K.clean(valid & (hh_a < t_a + offset) & (hh_b >= t_a + offset) & ~perm)
        sensitivity.append({"offset_db": offset, "threshold_before_db": t_b + offset,
                            "threshold_after_db": t_a + offset,
                            "new_water_km2": float(mask.sum() * K.PIXEL_KM2)})
    areas = [r["new_water_km2"] for r in sensitivity]
    stats = [
        ("classification_usable", int(usable), "boolean", "0: global Otsu failed the dark-fraction quality check; water outputs are diagnostic only"),
        ("after_dark_fraction", dark_fraction, "fraction", "share of valid pixels below the shared threshold"),
        ("new_water_sensitivity_min_km2", min(areas), "km2", "minimum across shared-threshold -1/0/+1 dB"),
        ("new_water_sensitivity_max_km2", max(areas), "km2", "maximum across shared-threshold -1/0/+1 dB"),
        ("valid_fraction", float(valid.mean()), "fraction", "share of the box with radar data on both dates"),
        ("threshold_before_db", t_b, "dB", f"HH water threshold, 28 Jun ({how_b})"),
        ("threshold_after_db", t_a, "dB", f"HH water threshold, 10 Jul ({how_a})"),
        ("permanent_water_km2", float(perm.sum() * K.PIXEL_KM2), "km2", "JRC occurrence >= 50%"),
        ("permanent_water_seen_dark", perm_seen, "fraction", "share of JRC permanent water that radar sees as water on 28 Jun"),
        ("water_before_km2", float(water_b.sum() * K.PIXEL_KM2), "km2", "all dark-water pixels, 28 Jun"),
        ("water_after_km2", float(water_a.sum() * K.PIXEL_KM2), "km2", "all dark-water pixels, 10 Jul"),
        ("new_water_km2", float(new_water.sum() * K.PIXEL_KM2), "km2", "newly dark candidate water outside permanent water; unverified"),
        ("new_water_patches", int(_count(new_water)), "count", "separate new-water patches"),
        ("receded_km2", float(receded.sum() * K.PIXEL_KM2), "km2", "water on 28 Jun that is gone on 10 Jul (outside permanent water)"),
        ("brighter_flat_km2", float(brighter.sum() * K.PIXEL_KM2), "km2", "possible water under trees or between buildings (not counted as flood)"),
    ]
    layers = dict(hh_before=hh_b, hh_after=hh_a, hv_before=hv_b, hv_after=hv_a, ratio=ratio,
                  water_before=water_b, water_after=water_a, new_water=new_water, receded=receded,
                  brighter=brighter, permanent=perm, valid=valid)
    if write:
        C.DERIVED.mkdir(parents=True, exist_ok=True)
        with open(C.DERIVED / "water_stats.csv", "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["metric", "value", "unit", "meaning"])
            for m, v, u, why in stats:
                w.writerow([m, round(v, 4) if isinstance(v, float) else v, u, why])
        with open(C.DERIVED / "water_sensitivity.csv", "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(sensitivity[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(sensitivity)
        K.write_json(C.DERIVED / "water_threshold.json", {
            "method": how_a, "threshold_linear": float(10 ** (t_a / 10)),
            "threshold_db": t_a, "source_granule_id": C.PRIMARY["after"],
            "applied_to": "all compatible dates", "histogram_bins": 256,
            "classification_usable": usable, "after_dark_fraction": dark_fraction,
            "max_dark_fraction": C.WATER_MAX_DARK_FRACTION,
            "quality_note": "Global Otsu does not separate water from land in this scene" if not usable else "Global split passed degeneracy check; this is not field validation",
            "sensitivity": "shared threshold on both dates, -1/0/+1 dB"})
        for k, v in layers.items():
            K.save_layer(k, v)
        feats = K.patches_to_features(new_water, lambda r: {
            "kind": "new_water", "area_ha": round(float(r.sum() * K.PIXEL_HA), 2),
            "drop_db": round(float(np.nanmean(ratio[r])), 1)})
        K.write_json(C.DERIVED / "new_water.geojson", {"type": "FeatureCollection",
                     "classification_usable": usable, "features": feats})
    return {m: v for m, v, *_ in stats}, layers


def _count(mask):
    from scipy import ndimage as ndi
    return ndi.label(mask, structure=np.ones((3, 3)))[1]


if __name__ == "__main__":
    s, _ = run()
    for k, v in s.items():
        print(f"{k:28s} {v:.4g}" if isinstance(v, float) else f"{k:28s} {v}")
