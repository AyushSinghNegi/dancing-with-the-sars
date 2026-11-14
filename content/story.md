<!--
Story text for the app's Story page (Urvashi owns this file; U4/U6).
Rules: one "## " heading per step, in order. Keep each step under 90 words.
Numbers ONLY as {placeholders}; the app fills them from data/derived/metrics.json.
Available: {crosstrack_sentence} {cloud_sentence} (whole sentences, empty when that check is missing) {new_water_km2} {new_water_patches} {rise_km2} {flood_km2} {flood_patches} {slide_zones} {slide_high} {brighter_km2}
{flood_hits} {flood_observable} {slide_hits} {slide_observable} {before} {after}
{res_first} {res_first_date} {res_peak} {res_peak_date} {res_last_clause} (timeline; the step is dropped when there are fewer than 3 dates)
-->

## The rain
In the first week of July 2026, the Western Ghats above Pune took days of extreme rain. Rivers rose,
low streets flooded, and hillsides gave way. Between 3 and 8 July, floods and landslides were reported
across Pune district. This chart shows the daily rainfall over our study area, with the two days the
NISAR satellite passed overhead.

## Clouds hide the ground. Radar does not.
{cloud_sentence} NISAR carries an L-band radar: it sends
its own microwave pulses, about 24 cm long, which pass through cloud and rain and come back from the
ground. Smooth water reflects the pulse away, so it looks dark. Rough ground, trees and buildings send
it back, so they look bright. That simple contrast is what we measure.

## Before and after
Drag the slider to compare the radar image from {before}, before the storms, with {after}, two days
after the worst of them. Dark patches that appear in the second image are new water. Look along the
rivers and the low ground east of the Ghats.

## What changed
Between the two passes, the reservoirs and rivers that feed Pune rose: {rise_km2} km² of new water along
their edges. Where no water was recorded between 1984 and 2021, {flood_km2} km² of flood water was still standing
on {after}. On the steep slopes we found {slide_zones} likely slide zones, {slide_high} of them high confidence:
places where the ground stopped matching itself between passes and the radar signal jumped. {crosstrack_sentence} White markers are
events reported in the news; click one to see its source.

## The weeks after
NISAR kept passing over Pune every 12 days. Seen from the same orbit, in the same radar mode, the surface of the
area's rivers and reservoirs grew from {res_first} km² on {res_first_date} to {res_peak} km² on {res_peak_date}{res_last_clause}.
The July storm was the start of the monsoon, not its end: the reservoirs west of Pune kept filling for weeks.

## What radar could not see
Radar is not magic, and we show where it falls short. The heaviest rain fell on 5 to 8 July, between NISAR
passes on 4 and 10 July, and had all but stopped by 9 July: flood water had two days to drain
before the radar came back. Of the reported floods radar could observe, {flood_hits} of {flood_observable} had a
detection nearby; for landslides, {slide_hits} of {slide_observable}. Water between tall buildings hides in bright
radar echoes, and slides narrower than our 40 m pixels can slip through. Knowing these limits is what makes the
rest of the map trustworthy.
