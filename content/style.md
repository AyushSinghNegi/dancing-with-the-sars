# Visual style (U4)

This file writes down the style the app already uses, so slides, video and the project page match it.
The colour values are copied from `app/lib/ui.py`; change them there first, then here.

## Landing copy

| Where | Text | In the app now? |
|---|---|---|
| One-line pitch | NISAR sees what monsoon clouds hide | No. The landing title is "What NISAR radar saw in the 2026 Pune monsoon". Use the pitch on slide 1 and the project page. |
| Button 1 | Start the story | Yes |
| Button 2 | Explore the map | Yes |

## Colours

One hue family for water (blue), one accent for changed ground (orange), one extra hue (green) for
"possible water". Text and buttons are slate so that blue always means water.

| Role | Hex | Drawn as | Meaning |
|---|---|---|---|
| **Changed ground (the accent)** | `#eb6834` | outline, light fill | Likely slide zone |
| Flooding | `#1c5cab` | fill | New water where no water was recorded before |
| Reservoirs and rivers rising | `#6da7ec` | fill | New water at the edge of water that is always there |
| New open water (charts, focus ring) | `#2a78d6` | fill | Both of the above together; rainfall bars |
| Possible water under cover | `#1baf7a` | hatch | Brighter radar on flat ground; shown, never counted |
| Rivers and reservoirs | `#b7d3f6` | fill | Permanent water, background only |
| Reported event | `#1d3346` ring on white | dot | News or official report |
| Text and buttons | `#1d3346` | | |
| Muted text | `#5d6b75` | | |
| Radar grey (dates, step numbers) | `#7d878f` | | |
| Page background | `#fcfcfb` | | |

Rules:

- Orange is used for changed ground and nothing else. Do not use it for buttons, headings or highlights.
- Blue is used for water and nothing else.
- Never rely on colour alone: slide zones are outlined, possible water is hatched, reported events
  are dots, and every map has a legend with words.
- The yellow DEMO banner (`#fff4d6`) appears only when the app runs on synthetic data.

### Colour-blind check

Checked on 14 Nov 2026 with a palette validator that simulates red-green colour blindness
(protan and deutan) and measures how far apart each pair of colours stays (OKLab distance x 100;
8 or more is the target). All pairs were compared, as on a map any two colours can touch.

| Check | Colours | Result |
|---|---|---|
| Separation, colour-blind | flooding, rising, slide zone, possible water | Pass. Closest pair: slide-zone orange and possible-water green, 9.2 (deutan) |
| Separation, normal vision | same four | Pass. Closest pair: possible-water green and rising blue, 19.2 |
| Accent against main blue | slide zone, flooding | Pass. 24.4 (protan) |
| Blue water ramp reads light to dark | flooding, rising, permanent | Pass |
| Contrast against the page | rising `#6da7ec` 2.44:1, possible water `#1baf7a` 2.74:1, permanent `#b7d3f6` 1.50:1 | Below 3:1, so these three always need a label, outline or hatch. The app's legend and hatch do this. |

Known weak spots, stated plainly:

- Orange and green are the closest pair for red-green colour-blind readers. Keep the hatch on green
  and the outline on orange.
- For blue-yellow colour blindness (tritan, rare) the closest pair measures 4.7. The outline, hatch
  and legend are what tell the layers apart there.
- Permanent water is deliberately pale: it is background, not a finding.

## Legend format

Every map or chart carries, in this order:

`What it shows · unit · date or date pair · NISAR file ID`

- **What it shows:** plain words first ("New open water"), expert term second if needed ("coherence").
- **Unit:** km² for areas, mm per day for rain, dB for radar brightness, "0 to 1" for coherence.
- **Date:** the exact pass date, or both dates for a change layer. No "before the storm".
- **NISAR file ID:** the full ID, never shortened. On small screens it may sit one click away
  (the Method page lists every ID), but slides and the project page show it in full.

File IDs used by the main result (from `data/derived/metrics.json`):

| Role | NISAR file ID |
|---|---|
| Before, 28 Jun 2026 | `NISAR_L2_PR_GCOV_024_034_D_079_4005_DHDH_A_20260628T134239_20260628T134314_P05023_N_F_J_001` |
| After, 10 Jul 2026 | `NISAR_L2_PR_GCOV_025_034_D_079_4005_DHDH_A_20260710T134239_20260710T134313_P05023_N_F_J_001` |
| Pair (coherence) | `NISAR_L2_PR_GUNW_024_034_D_079_025_4000_SH_20260628T134239_20260628T134314_20260710T134239_20260710T134313_P05023_N_F_J_001` |

Example legend line:

`New open water · km² · 28 Jun to 10 Jul 2026 · NISAR_L2_PR_GCOV_025_034_D_079_4005_DHDH_A_20260710T134239_20260710T134313_P05023_N_F_J_001`

Other sources are named the same way: "GPM IMERG Late Run daily (GPM_3IMERGDL v07)" for rain,
"JRC Global Surface Water v1.4" for permanent water. See `data/reference/SOURCES.md`.

## Font

One family: **IBM Plex Sans** (SIL Open Font License; files for the video are in `video/fonts/`).

| Use | Face |
|---|---|
| Body text, labels, legends | IBM Plex Sans 400, 500, 600 |
| Headings, big numbers, dates | IBM Plex Sans Condensed 600, 700 |
| Marathi | IBM Plex Sans Devanagari 400, 600 |

Slides use the same family. If it is not installed, install it rather than substituting another font.

## Words

- Say "likely slide zone", never "landslide", for a radar detection that no report confirms.
- Numbers come from `data/derived/` or a source we opened. If a value is missing, write "not available".
- Headlines are 8 words or fewer; one idea per sentence.
