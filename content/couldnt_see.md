# What radar couldn't see (U5)

Panel text for the app, slides and project page. Every number has its source in the table below;
recheck them after each new pipeline run (`data/derived/metrics.json` generated 2026-11-14T13:38Z).

## Panel text

- **Flooded streets between buildings.** Radar bounces off walls and back to the satellite, so a
  flooded street can look bright, not dark. All 6 of the reported floods we missed were in built-up areas.
- **Water that came and went between passes.** The heaviest rain fell on 5 to 8 July; NISAR looked on
  28 June and again on 10 July. The map shows what was still standing on 10 July, not the peak.
- **Small slides, and slides on gentle ground.** Our map has 40 m pixels and searches slopes of 15° to 45°.
  A slide the width of one house can slip through, and 2 reported landslides were on ground gentler than that.
- **Slopes hidden from the satellite.** About 2% of the steep ground faces away from the radar or folds
  over itself in the image. We leave those slopes out and do not guess.
- **Early data.** NASA has calibrated these NISAR products but validated them at only a limited number of
  sites so far. Our numbers will move as the data matures.

Every likely slide zone is a lead to check on the ground, not a verdict: 46 of the 50 zones have no
reported event within 2 km.

## Where each number comes from

| Statement | Value | Source |
|---|---|---|
| Reported floods missed, all in built-up areas | 6 of 6 misses | `data/derived/validation.csv`, rows with result `miss` and a flood type; `reason` column |
| Heaviest rain 5 to 8 July | about 180, 158, 109, 140 mm/day | `data/reference/rainfall.csv` (GPM IMERG Late Run) |
| Radar pair dates | 28 Jun and 10 Jul 2026 | `data/derived/timeline.csv` |
| Pixel size | 40 m | `metrics.json` → `grid.res_m` |
| Slope range searched | 15° to 45° | `metrics.json` → `thresholds.slide_min_slope_deg`, `slide_max_slope_deg` |
| Reported landslides on gentler ground | 2 (E001, E006) | `data/derived/validation.csv`, `reason` column |
| Steep ground hidden from the radar | 1.9% | `metrics.json` → `slides.layover_shadow_share_of_steep` |
| Calibrated, validated at a limited number of sites | | NASA Science, NISAR mission page (science.nasa.gov/mission/nisar), opened 14 Nov 2026 |
| Zones with no reported event within 2 km | 46 of 50 | `metrics.json` → `validation.unreported_slide_zones`, `slides.zones` |

## Not in the panel, but true

- 2 reported landslides could not be checked because the report names a road, not a spot (E004, E005).
- 1 reported landslide lies outside the radar box (E007); 1 flood happened after the radar pair (E018).
- The full event-by-event table is in `content/validation.md`.
