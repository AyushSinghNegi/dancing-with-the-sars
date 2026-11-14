<!--
Story text for the app's Story page (Urvashi owns this file; U4/U6).
Rules: one "## " heading per step, in order. Keep each step under 90 words.
Numbers ONLY as {placeholders}; the app fills them from data/derived/metrics.json.
Available: {crosstrack_sentence} (a whole sentence, empty when there is no second-track check) {new_water_km2} {new_water_patches} {rise_km2} {flood_km2} {flood_patches} {slide_zones} {slide_high} {brighter_km2}
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
after the worst of them. Dark patches that appear in the second image are new water. Look along the
rivers and the low ground east of the Ghats.

## What changed
Between the two passes, the reservoirs and rivers that feed Pune rose: {rise_km2} km² of new water along
their edges. Where no water had been recorded since 1984, {flood_km2} km² of flood water was still standing
on {after}. On the steep slopes we found {slide_zones} likely slide zones, {slide_high} of them high confidence:
places where the ground stopped matching itself between passes and the radar signal jumped. {crosstrack_sentence} White markers are
events reported in the news; click one to see its source.

## What radar could not see
Radar is not magic, and we show where it falls short. The heaviest rain fell on 5 to 7 July, between NISAR
passes on 4 and 10 July, and flood releases into the Mutha river stopped on 9 July: most flood water had drained
before the radar came back. Of the reported floods radar could observe, {flood_hits} of {flood_observable} had a
detection nearby; for landslides, {slide_hits} of {slide_observable}. Water between tall buildings hides in bright
radar echoes, and slides narrower than our 40 m pixels can slip through. Knowing these limits is what makes the
rest of the map trustworthy.
