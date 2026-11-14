"""R6: low coherence AND HV drop AND NASADEM slope >= configured 20 degrees.

These are candidate zones to investigate, not confirmed landslides. Local
coherence contrast and HH change are exported as diagnostics, not gates.
"""
from __future__ import annotations

import numpy as np

from . import ancillary
from . import common as K
from . import config as C


def run(layers=None, write=True):
    if layers is None:
        layers = {k: K.load_layer(k) for k in ("hh_before", "hh_after", "hv_before", "hv_after",
                                                 "water_after", "permanent", "valid")}
    d = K.load_pair()
    coh = d["coherence"]
    if coh is None or not np.isfinite(coh).any():
        raise ValueError("GUNW coherence is required for likely slide zones; crop the primary pair first")
    slope = np.nan_to_num(ancillary.load()["slope"])
    steep = slope >= C.SLIDE_MIN_SLOPE_DEG
    d_hv = layers["hv_after"] - layers["hv_before"]
    d_hh = layers["hh_after"] - layers["hh_before"]
    bs_change = d_hv <= -C.CHANGE_DB

    coh_med = K.local_median(coh, size_px=25)
    with np.errstate(invalid="ignore", divide="ignore"):
        anomaly = coh / coh_med
    coh_loss = np.isfinite(coh) & (coh < C.COHERENCE_LOW)
    cand = steep & layers["valid"] & coh_loss & bs_change
    method = "low coherence + HV drop + NASADEM slope"
    zones = K.clean(cand, min_px=C.SLIDE_MIN_PATCH_PIXELS)

    def props(r):
        s = float(np.mean(slope[r]))
        dhv = float(np.nanmean(d_hv[r]))
        dhh = float(np.nanmean(d_hh[r]))
        c = float(np.nanmean(coh[r])) if coh is not None else None
        a = float(np.nanmean(anomaly[r])) if anomaly is not None else None
        # Score: each piece of evidence adds up to 1/3 (slope, radar change, coherence loss).
        e_slope = np.clip((s - C.SLIDE_MIN_SLOPE_DEG) / 20, 0, 1)
        e_bs = np.clip((-dhv - C.CHANGE_DB) / 6 + 0.3, 0, 1)
        e_coh = np.clip((C.COHERENCE_LOW - c) / C.COHERENCE_LOW + 0.3, 0, 1) if a is not None else 0.0
        score = float((e_slope + e_bs + e_coh) / 3)
        area = float(r.sum() * K.PIXEL_HA)
        conf = "high" if score >= 0.7 and area >= 1 else ("medium" if score >= 0.5 else "low")
        return {"kind": "slide_zone", "area_ha": round(area, 2), "slope_deg": round(s, 1),
                "hv_change_db": round(dhv, 1), "mean_hv_drop_db": round(-dhv, 1), "hh_change_db": round(dhh, 1),
                "coherence": None if c is None else round(c, 2),
                "coherence_vs_local": None if a is None else round(a, 2),
                "score": round(score, 2), "confidence": conf}

    feats = K.patches_to_features(zones, props)
    feats.sort(key=lambda f: -f["properties"]["score"])
    for i, f in enumerate(feats, start=1):
        f["properties"]["id"] = f"SZ{i:03d}"
    summary = {
        "method": method,
        "zones": len(feats),
        "candidate_pixels_before_cleanup": int(cand.sum()),
        "candidate_pixels_after_cleanup": int(zones.sum()),
        "min_patch_pixels": C.SLIDE_MIN_PATCH_PIXELS,
        "high": sum(f["properties"]["confidence"] == "high" for f in feats),
        "medium": sum(f["properties"]["confidence"] == "medium" for f in feats),
        "area_ha": round(sum(f["properties"]["area_ha"] for f in feats), 1),
        "steep_share": round(float(steep.mean()), 3),
    }
    if write:
        K.write_json(C.DERIVED / "slide_zones.geojson", {"type": "FeatureCollection", "summary": summary,
                                                         "features": feats})
        K.save_layer("slide_zones", zones)
        if coh is not None:
            K.save_layer("coherence", coh)
            K.save_layer("coherence_anomaly", anomaly)
    return summary, zones


if __name__ == "__main__":
    s, _ = run()
    print(s)
