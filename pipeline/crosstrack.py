"""Second-track check (R10): do the slide zones show up in an independent NISAR pair?

The main results use track 034 (28 Jun -> 10 Jul). Track 106 passes over the same ground five days
later in its own cycle (3 Jul -> 15 Jul), from a different orbit and a different incidence angle,
and its pair also spans the 5-7 Jul rain peak. A real slope failure changes the ground for good, so
it should show in both pairs. Speckle, a wet-rock flash or a geometry artefact of one track usually
does not.

For every track-034 zone we run the same slide rule on the track-106 pair and record one status:
  confirmed    a track-106 slide zone lies within 80 m (2 pixels)
  partial      track 106 shows one piece of the evidence within 80 m (coherence loss or the
               backscatter jump on steep, dry ground), but not the full rule
  not seen     track 106 has good data there and shows neither
  not covered  track 106 has no data over most of the zone, or the slope is in its radar
               shadow or layover

Chance level: the same test on the same zones moved to random places of the same kind (steep, dry,
inside both tracks), CROSS_RANDOM_TRIALS times. "Lift" = real confirmation rate / chance rate.
A lift near 1 would mean the second track agrees no more than it would anywhere on the Ghats.

Also: water area on 3 Jul and 15 Jul (more points for the water timeline), and whether track 106
puts a slide zone near each reported landslide.

  python -m pipeline.crosstrack
Writes data/derived/crosstrack.json and adds "track106" to each slide zone in slide_zones.geojson.
"""
from __future__ import annotations

import json

import numpy as np
from scipy import ndimage as ndi

from . import ancillary
from . import common as K
from . import config as C
from . import nisar_io as io
from . import slide_zones, validate, water

STATUSES = ("confirmed", "partial", "not seen", "not covered")


def available() -> bool:
    names = {m["name"] for m in K.manifest()}
    return {io.crop_name(C.CROSSCHECK["before"]), io.crop_name(C.CROSSCHECK["after"])} <= names


def classify(ids, n, z2, evid2, covered2):
    """Status for zones 1..n of an id raster. Vectorised with bincount so random trials are cheap.

    z2 / evid2: second-track zones / evidence, already buffered. covered2: second track has usable data.
    Returns an array of status indices (into STATUSES), one per zone id 1..n.
    """
    flat = ids.ravel()
    size = np.bincount(flat, minlength=n + 1)[1:].astype(float)
    cov = np.bincount(flat, weights=covered2.ravel(), minlength=n + 1)[1:]
    hit = np.bincount(flat, weights=z2.ravel(), minlength=n + 1)[1:]
    part = np.bincount(flat, weights=evid2.ravel(), minlength=n + 1)[1:]
    with np.errstate(invalid="ignore", divide="ignore"):
        covered = (cov / size) >= 0.5
    out = np.full(n, 2)                      # not seen
    out[part > 0] = 1                        # partial
    out[hit > 0] = 0                         # confirmed
    out[~covered] = 3                        # not covered wins: no data, no verdict
    return out, size


def chance_rates(ids, n, eligible, z2, evid2, covered2, trials, seed=7, min_shift_px=50):
    """Move every zone by one random offset per trial (the whole pattern rolls together, so zone sizes
    and spacing stay real) and count how often a zone that lands on eligible ground gets each status."""
    rng = np.random.default_rng(seed)
    h, w = ids.shape
    counts = np.zeros(len(STATUSES))
    for _ in range(trials):
        while True:
            dy, dx = int(rng.integers(-h // 2, h // 2)), int(rng.integers(-w // 2, w // 2))
            if max(abs(dy), abs(dx)) >= min_shift_px:   # at least 2 km away from the real place
                break
        rolled = np.roll(ids, (dy, dx), axis=(0, 1))
        st, size = classify(rolled, n, z2, evid2, covered2)
        elig = np.bincount(rolled.ravel(), weights=eligible.ravel(), minlength=n + 1)[1:]
        keep = (size > 0) & (elig == size)          # the whole zone sits on steep, dry ground
        counts += np.bincount(st[keep], minlength=len(STATUSES))
    return counts


def run(write=True):
    if not available():
        (C.DERIVED / "crosstrack.json").unlink(missing_ok=True)   # never leave a stale check behind
        print("      track-106 crops not found; skipping (python -m pipeline.crop --granule ... for CROSSCHECK)")
        return None
    aux = ancillary.load()
    b, a = (C.parse_granule_id(C.CROSSCHECK[k])["date"] for k in ("before", "after"))
    lab = (_short(b), _short(a))
    d2 = K.load_pair(C.CROSSCHECK["before"], C.CROSSCHECK["after"], C.CROSSCHECK["pair"])
    wstats2, lay2, _ = water.compute(d2, aux, labels=lab)
    det2 = slide_zones.detect(lay2, d2["coherence"], aux)
    wstats_d = {m: v for m, v, *_ in wstats2}

    # Main pair, from the saved layers (same rule, track-034 geometry).
    lay1 = {k: K.load_layer(k) for k in ("hh_before", "hh_after", "hv_before", "hv_after",
                                          "water_after", "permanent", "valid")}
    det1 = slide_zones.detect(lay1, K.load_pair()["coherence"], aux)
    ids = K.load_layer("slide_zone_ids").astype(np.int64)
    n = int(ids.max())

    buf = np.ones((2 * C.CROSS_BUFFER_PX + 1,) * 2, bool)
    z2 = ndi.binary_dilation(det2["zones"], buf)
    evid2 = ndi.binary_dilation((det2["coh_loss"] | det2["bs_change"]) & det2["steep"] & det2["not_water"], buf)
    covered2 = lay2["valid"] & ~det2["geom_bad"]
    eligible = det1["steep"] & det1["not_water"]

    st, _ = classify(ids, n, z2, evid2, covered2) if n else (np.zeros(0, int), None)
    real = np.bincount(st, minlength=len(STATUSES)) if n else np.zeros(len(STATUSES), int)
    rand = chance_rates(ids, n, eligible, z2, evid2, covered2, C.CROSS_RANDOM_TRIALS) if n else None

    def rates(c):
        seen = c[:3].sum()
        return {"confirmed": _r(c[0] / seen) if seen else None,
                "confirmed_or_partial": _r((c[0] + c[1]) / seen) if seen else None, "zones_scored": int(seen)}

    real_rates, rand_rates = rates(real), rates(rand) if rand is not None else {}
    lift = p_value = None
    if rand is not None and real[:3].sum() and rand[0] > 0:
        p_chance = rand[0] / rand[:3].sum()
        lift = (real[0] / real[:3].sum()) / p_chance
        # How likely this many found-again zones would be by chance alone (one-sided binomial test).
        from scipy.stats import binom
        p_value = float(binom.sf(int(real[0]) - 1, int(real[:3].sum()), p_chance))

    # Per-zone status, written back into the zone file the app reads.
    gj_path = C.DERIVED / "slide_zones.geojson"
    gj = json.loads(gj_path.read_text())
    by_conf = {}
    for f in gj["features"]:
        i = int(f["properties"]["id"][2:])
        s = STATUSES[st[i - 1]]
        f["properties"]["track106"] = s
        by_conf.setdefault(f["properties"]["confidence"], np.zeros(len(STATUSES), int))[st[i - 1]] += 1

    summary = {
        "method": det2["method"],
        "pair": {"track": C.parse_granule_id(C.CROSSCHECK["before"])["track"], "before": b, "after": a,
                 "granules": dict(C.CROSSCHECK)},
        "buffer_m": C.CROSS_BUFFER_PX * C.GRID_RES,
        "valid_fraction": _r(float(lay2["valid"].mean())),
        "radar_facing_azimuth_deg": round(det2["facing"], 0),
        "zones_track034": n,
        "status_counts": dict(zip(STATUSES, map(int, real))),
        "status_by_confidence": {k: dict(zip(STATUSES, map(int, v))) for k, v in sorted(by_conf.items())},
        "real": real_rates,
        "chance": {**rand_rates, "trials": C.CROSS_RANDOM_TRIALS},
        "lift_confirmed": None if lift is None else round(float(lift), 1),
        "p_value": None if p_value is None else round(p_value, 3),
        "scene_shift_db": {"track034": det1["scene_shift"], "track106": det2["scene_shift"]},
        # During the storm (3 Jul) rain roughens water surfaces, so radar sees much open water as bright;
        # track-106 water areas are kept for the record but not shown when this check fails.
        "water_reliable": bool((wstats_d.get("permanent_water_seen_dark") or 0) >= 0.6),
        "zones_track106": int(ndi.label(det2["zones"], structure=np.ones((3, 3)))[1]),
        "water": {m: _r(v) if isinstance(v, float) else v for m, v, *_ in wstats2},
        "events": _events(det2["zones"], lay2["valid"], b, a),
    }
    if write:
        K.write_json(gj_path, gj)
        K.write_json(C.DERIVED / "crosstrack.json", summary)
        K.save_layer("track106_slide_zones", det2["zones"])
    return summary


def _events(zones2, valid2, before, after):
    """Reported landslides: does track 106 put a zone near them too?"""
    d = validate._dist_m(zones2)
    out = []
    for f in validate.load_events():
        p = f["properties"]
        if p.get("type", "").strip().lower() not in validate.SLIDE_TYPES:
            continue
        lon, lat = f["geometry"]["coordinates"][:2]
        r, c, shape = K.lonlat_to_rowcol(lon, lat)
        prec = float(p.get("precision_m") or 500)
        row = {"id": p.get("id"), "place": p.get("place", ""), "date": p.get("date", "")}
        if not (0 <= r < shape[0] and 0 <= c < shape[1]) or not valid2[r, c]:
            row["result"] = "not observable"
        elif row["date"] and not (before < row["date"] <= after):
            row["result"] = "not observable"
        elif prec > 2000:
            row["result"] = "not scored"
        else:
            dist = d[r, c]
            row["distance_m"] = int(round(dist)) if np.isfinite(dist) else None
            row["result"] = "hit" if dist <= max(prec, validate.RADIUS["slide"]) else "miss"
        out.append(row)
    return out


def _short(date):
    import datetime as dt
    return dt.date.fromisoformat(date).strftime("%-d %b")


def _r(x, nd=3):
    return None if x is None else round(float(x), nd)


if __name__ == "__main__":
    s = run()
    if s:
        print(json.dumps({k: v for k, v in s.items() if k not in ("water", "events")}, indent=2))
