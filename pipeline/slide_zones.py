"""Likely slide zones on steep ground (R6).

A landslide strips vegetation and churns the surface between two radar passes.
NISAR sees that in two independent ways (both are rare, sharp outliers in the real Pune data):
  1. Interferometric COHERENCE collapses (the surface no longer matches itself
     between 28 Jun and 10 Jul). Monsoon vegetation lowers coherence everywhere,
     so we look for coherence that is low AND far below its own 1 km
     neighbourhood (a local anomaly), not just low.
  2. BACKSCATTER changes: HV (volume scattering from leaves and branches) drops
     when vegetation is removed; HH can rise on fresh rough debris.
We keep pixels on 15-45 deg slopes, outside radar layover and shadow (worked out from the DEM and the
look direction measured in the data), that show (1) and (2), or a very strong (2) when coherence is
missing; group them into zones of at least 2 pixels (0.32 ha), and score each zone 0-1.

These are LIKELY zones for people to check, not confirmed landslides.

  python -m pipeline.slide_zones
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
    aux = ancillary.load()
    slope = np.nan_to_num(aux["slope"])
    aspect = K.aspect_degrees(aux["elevation"])
    facing = K.radar_facing_azimuth(layers["hh_before"], slope, aspect)
    geom_bad = K.layover_shadow(slope, aspect, facing)
    steep = (slope >= C.SLIDE_MIN_SLOPE_DEG) & (slope <= C.SLIDE_MAX_SLOPE_DEG) & ~geom_bad
    d_hv = layers["hv_after"] - layers["hv_before"]
    d_hh = layers["hh_after"] - layers["hh_before"]
    not_water = ~layers["water_after"] & ~layers["permanent"] & layers["valid"]
    bs_change = (d_hh >= C.SLIDE_HH_RISE_DB) | (d_hv <= -C.SLIDE_HV_DROP_DB)
    strong_bs = (d_hh >= 2 * C.SLIDE_HH_RISE_DB) | (d_hv <= -2 * C.SLIDE_HV_DROP_DB)

    if coh is not None:
        coh_med = K.local_median(coh, size_px=25)
        with np.errstate(invalid="ignore", divide="ignore"):
            anomaly = coh / coh_med
        coh_loss = (coh < C.COHERENCE_LOW) & (anomaly < 0.6)
        cand = steep & not_water & coh_loss & bs_change
        method = "coherence anomaly + backscatter change + slope"
    else:
        coh_med = anomaly = None
        coh_loss = np.zeros_like(steep)
        cand = steep & not_water & strong_bs
        method = "backscatter change + slope only (no GUNW coherence available)"
    zones = K.clean(cand, min_px=C.MIN_SLIDE_PIXELS)

    def props(r):
        s = float(np.mean(slope[r]))
        dhv = float(np.nanmean(d_hv[r]))
        dhh = float(np.nanmean(d_hh[r]))
        c = float(np.nanmean(coh[r])) if coh is not None else None
        a = float(np.nanmean(anomaly[r])) if anomaly is not None else None
        # Score: each piece of evidence adds up to 1/3 (slope, radar change, coherence loss).
        e_slope = np.clip((s - C.SLIDE_MIN_SLOPE_DEG) / 20, 0, 1)
        e_bs = np.clip(max(dhh - C.SLIDE_HH_RISE_DB, -dhv - C.SLIDE_HV_DROP_DB) / 4 + 0.3, 0, 1)
        e_coh = np.clip((0.6 - a) / 0.5 + 0.3, 0, 1) if a is not None else 0.0
        score = float((e_slope + e_bs + e_coh) / 3)
        area = float(r.sum() * K.PIXEL_HA)
        conf = "high" if score >= 0.8 else ("medium" if score >= 0.6 else "low")
        return {"kind": "slide_zone", "area_ha": round(area, 2), "slope_deg": round(s, 1),
                "hv_change_db": round(dhv, 1), "hh_change_db": round(dhh, 1),
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
        "high": sum(f["properties"]["confidence"] == "high" for f in feats),
        "medium": sum(f["properties"]["confidence"] == "medium" for f in feats),
        "area_ha": round(sum(f["properties"]["area_ha"] for f in feats), 1),
        "steep_share": round(float(steep.mean()), 3),
        "radar_facing_azimuth_deg": round(facing, 0),
        "layover_shadow_share_of_steep": round(float(geom_bad[slope >= C.SLIDE_MIN_SLOPE_DEG].mean()), 3),
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
