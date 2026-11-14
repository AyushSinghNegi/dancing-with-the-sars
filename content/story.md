<!--
Story text for the app's Story page (Urvashi owns this file; U4/U6).
Rules: one "## " heading per step, in order. Keep each step under 90 words.
Numbers ONLY as {placeholders}; the app fills them from data/derived/metrics.json.
Available: {new_water_km2} {new_water_patches} {slide_zones} {slide_high} {brighter_km2}
{flood_hits} {flood_observable} {slide_hits} {slide_observable} {before} {after}
-->

## The rain
In the first week of July 2026, the Western Ghats above Pune took days of extreme rain. Rivers rose,
low streets flooded, and hillsides gave way. Between 3 and 8 July, floods and landslides were reported
across Pune district. This chart shows the daily rainfall over our study area, with the two days the
NISAR satellite passed overhead.

## Clouds hide the ground. Radar does not.
Ordinary satellite cameras saw only cloud for most of that week. NISAR carries an L-band radar: it sends
its own microwave pulses, about 24 cm long, which pass through cloud and rain and come back from the
ground. Smooth water reflects the pulse away, so it looks dark. Rough ground, trees and buildings send
it back, so they look bright. That simple contrast is what we measure.

## Before and after
Drag the slider to compare the radar image from {before}, before the storms, with {after}, two days
after the worst of them. Newly dark patches are possible water and require classification checks. Look along the
rivers and the low ground east of the Ghats.

## What changed
Comparing the two passes, we found {new_water_km2} km² of candidate new water, outside the
rivers and reservoirs that are always wet. On the steep slopes we found {slide_zones} likely slide zones,
{slide_high} of them with a high evidence score: places where the ground no longer matched itself between passes and
the vegetation signal dropped. White markers are events reported in the news; click one to see the source.

## What radar could not see
Radar is not magic, and we want to show where it fails. Of the reported floods that radar could observe,
{flood_hits} of {flood_observable} had a detection nearby; for landslides, {slide_hits} of {slide_observable}.
Water between tall buildings hides in bright radar echoes. Floods that drained before {after} are gone by the
second pass. Slides narrower than our 40 m pixels can slip through. These limits apply to every interpretation of the map.
