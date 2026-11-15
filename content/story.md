<!--
Story text for the app's Story page (Urvashi owns this file; U4/U6).
Rules: one "## " heading per step, in order. Keep each step under 60 words.
Numbers ONLY as {placeholders}; the app fills them from data/derived/metrics.json.
Available: {flood_chance} (expected chance matches) {crosstrack_sentence} {cloud_sentence} (whole sentences, empty when that check is missing) {new_water_km2} {new_water_patches} {rise_km2} {flood_km2} {flood_patches} {slide_zones} {slide_high} {brighter_km2}
{flood_hits} {flood_observable} {slide_hits} {slide_observable} {before} {after}
{res_first} {res_first_date} {res_peak} {res_peak_date} {res_last_clause} (timeline; the step is dropped when there are fewer than 3 dates)
-->

## The Rain
In early July 2026, days of extreme rain hit the Western Ghats above Pune. Rivers rose, low streets were flooded
and hillsides gave way. Bars show the daily rain; triangles mark each NISAR pass, and the dotted lines are the two
passes we compare.

## Clouds Hide the Ground. Radar Does Not.
{cloud_sentence} NISAR's radar sends its own microwave pulses, which pass through cloud and rain. Calm water
bounces them away and looks dark; rough ground, trees and buildings send them back and look bright.

## Before and After
Drag the slider: {before} on the left, {after} on the right, two days after the worst rain. New dark patches are
new water. Look along the rivers and the edges of the reservoirs.

## What Changed
Reservoirs and rivers grew by **{rise_km2} km²**. On land that was never wet, **{flood_km2} km²** of flood water
still stood on {after}. On steep slopes we found **{slide_zones} likely slide zones**, {slide_high} of them high
confidence. {crosstrack_sentence}

## The Weeks After
NISAR kept coming back every 12 days. Pune's rivers and reservoirs grew from {res_first} km² on {res_first_date}
to **{res_peak} km²** on {res_peak_date}{res_last_clause}. The July storm started the monsoon; it did not end it.

## What Radar Could Not See
The heaviest rain fell on 5 to 8 July 2026, between passes on 3 and 10 July, so some flood water drained before
the radar returned. Radar found something near {flood_hits} of {flood_observable} reported floods it could see, but
places nobody reported score about {flood_chance}: no better than chance. For landslides it was {slide_hits} of
{slide_observable}. Water between buildings, and slides narrower than 40 m, can be missed.
