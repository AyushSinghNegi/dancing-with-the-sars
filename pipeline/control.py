"""R6: quantify candidate detections and radar change in declared control areas."""
from __future__ import annotations
import numpy as np
from . import common as K, config as C, zones
from .timeline import write_csv


def run(layers, slide_mask, coherence, write=True):
    rows = []
    for props, mask in zones.masks():
        if not props.get("control"):
            continue
        eligible = mask & layers["valid"] & np.isfinite(coherence)
        n = int(eligible.sum())
        delta = layers["hv_after"] - layers["hv_before"]
        hv = delta[eligible & np.isfinite(delta)]
        rows.append({"zone_id": props["id"], "zone_name": props["name"],
                     "review_status": props.get("review_status", "not reviewed"),
                     "valid_pixels": n, "candidate_pixels": int((slide_mask & eligible).sum()),
                     "candidate_area_ha": float((slide_mask & eligible).sum() * K.PIXEL_HA),
                     "median_coherence": float(np.median(coherence[eligible])) if n else None,
                     "median_hv_change_db": float(np.median(hv)) if hv.size else None})
    if write:
        write_csv(C.DERIVED / "control_stats.csv", ["zone_id", "zone_name", "review_status", "valid_pixels",
                  "candidate_pixels", "candidate_area_ha", "median_coherence", "median_hv_change_db"], rows)
    return rows
