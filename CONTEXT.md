# CONTEXT.md: read this first (humans and AI assistants)

Paste this file at the start of every Claude / ChatGPT chat about this project.

Current specification: RSN Data and Science brief. Pipeline 0.5 implements its linear-power Otsu, NASADEM/20°/HV-drop slide screen, fixed 200 m matching, and zone-median timeline.csv. The previous context method is preserved as a historical comparison in docs/BASELINE-RUN.md. The current water classifier fails its quality check; do not quote its diagnostic zeros as flood estimates.

## What we are building
**MonsoonLens**: an open web app that shows what NASA-ISRO **NISAR** L-band radar saw
around **Pune, India** during the **July 2026 monsoon**: new flood water, likely
landslide zones on the Western Ghats slopes, and what radar could *not* see,
checked against reported events. NASA Space Apps Challenge 2026, challenge
"Dancing with the SARs", local event GDG Ahlen (virtual). Team: Ayush
(app, integration, lead), RSN (data and science), Urvashi (validation, story, pitch).

## Non-negotiable rules
1. **Every number on screen comes from our pipeline output or a cited source.** No invented,
   estimated or "illustrative" numbers, ever. If a value is missing, show "not available".
2. **Synthetic data stays in `data/demo/`** and the app shows a DEMO banner whenever it uses it.
   `MONSOONLENS_DEMO=1` is the only way to touch it. Never copy demo outputs into `data/derived/`.
3. Compare backscatter only between dates with the **same track, radar mode and polarisation**
   (`config.same_mode`). Mode is field 9 of a GCOV file name (`4005`); pol is field 10 (`DHDH`).
4. Never commit `.h5` files, `.netrc`, tokens, or anything over 20 MB.
5. Say "likely slide zone", never "landslide", for radar detections that no report confirms.

## Data (all real except `data/demo/`)
| What | Where | Notes |
|---|---|---|
| NISAR GCOV 28 Jun 2026 (before) | `config.PRIMARY["before"]` | track 034 D, frame 079, mode 4005, DHDH |
| NISAR GCOV 10 Jul 2026 (after) | `config.PRIMARY["after"]` | same track, mode, pol |
| NISAR GUNW 28 Jun to 10 Jul | `config.PRIMARY["pair"]` | coherence for slide zones |
| Candidate NISAR scenes (49 Pune, 146 Brahmaputra backup) | `data/reference/candidate_scenes.csv` | from NASA CMR |
| JRC Global Surface Water occurrence v1.4 | `data/crops/aux_jrc_occurrence.tif` | permanent water = occurrence >= 50% |
| NASADEM_HGT.001: elevation, slope | `data/crops/aux_nasadem_elevation.tif`, `aux_nasadem_slope.tif` | Earthdata Login |
| Daily rainfall (supplied NASA POWER/MERRA-2; IMERG planned) | `data/reference/rainfall.csv` | Urvashi, U2 |
| Reported events | `data/reference/events.geojson` | Urvashi, U3 (schema below) |

Project box (WGS84): lon 73.30 to 74.10, lat 18.15 to 18.90. Analysis grid: UTM 43N (EPSG:32643), 40 m.

NISAR file layout (confirmed from ASF docs, check with `pipeline.inspect_h5` on the real file):
- GCOV: `/science/LSAR/GCOV/grids/frequencyA/` holds `HHHH`, `HVHV` (gamma0, linear power),
  `mask` (0 = invalid or partially focused, 255 = outside swath), `numberOfLooks`, `rtcGammaToSigmaFactor`, `xCoordinates`,
  `yCoordinates`, `projection` (EPSG code). Full-frame layers are ~5 GB each, so we stream the box only.
- GUNW: the real selected coherence is at
  `/science/LSAR/GUNW/grids/frequencyA/wrappedInterferogram/HH/coherenceMagnitude`,
  20 m native spacing (unwrapped coherence is 80 m). The code selects the finest layer.

## Pipeline (python -m pipeline.<step>)
| Step | Module | Output |
|---|---|---|
| Inspect a file | `inspect_h5` | paths, EPSG, spacing, mask values |
| Cut to the box (streams from ASF) | `acquire --primary`, `acquire --timeline` | `data/crops/*_HH.tif`, `_HV.tif`, `_COH.tif`, `manifest.json` |
| JRC water + DEM | `ancillary` | `data/crops/aux_*.tif` |
| New water | `water` | `water_stats.csv`, `new_water.geojson` |
| Slide zones | `slide_zones` | `slide_zones.geojson` |
| Validation | `validate` | `validation.csv`, `validation_summary.json` |
| Timeline | `timeline` | `timeline.csv` (zone HH/HV), `water_timeline.csv` |
| Everything + map images | `run_all` | `overlays/`, `geotiff/`, `bounds.json`, `metrics.json` |

Crops are stored as int16 GeoTIFF (dB x 100); coherence as uint8 (x 250).

### Method in one paragraph
Lee filtering is performed in linear power. Scikit-image Otsu is fitted to all finite positive
10 July HH power samples; the one threshold is applied to both dates. New water = dark after,
not dark before, outside JRC occurrence >=50%, patch >=4 pixels. No slope or 3 dB gate is
added to this brief-defined water layer. Shared-threshold sensitivity is -1/0/+1 dB on both
dates. A split classifying >=95% of valid pixels as dark is rejected for flood reporting;
outputs remain available as diagnostics. Current global Otsu fails this check. Slide zones
require NASADEM slope >=20°, coherence <0.35 and HV drop >=3 dB, with >=3 connected pixels;
HH change/local coherence contrast are diagnostics only. Scores are not probabilities.
Validation uses a fixed 200 m radius plus a separate precision-aware comparison column.
Rejected water classifications are not scored as flood hits/misses. timeline.csv contains
HH/HV medians for four desk-reviewed zones and five compatible dates; water_timeline.csv
is a supplementary diagnostic water series. Full raw downloads are local-only, resumable
via pipeline.download_raw. Python 3.11 is required and tested.

## events.geojson schema (U3)
FeatureCollection of Points, properties:
`id` (E001...), `type` (flood | waterlogging | river_overflow | landslide | road_closure),
`date` (YYYY-MM-DD, event date), `place`, `precision_m` (100 exact spot, 500 neighbourhood,
2000 village or stretch of road), `source_name`, `source_url`, `note`.
Use news or official sources you can link. Coordinates from the place named in the source.

## rainfall.csv schema (U2)
`date,precip_mm,source` (one row per day, 2026-06-15 to 2026-10-31, box-average daily IMERG).

## App
Streamlit, `app/streamlit_app.py` (landing) + `app/views/1_Story.py`, `2_Explore.py`, `3_Method.py`.
The app reads only `data/derived/` (or `data/demo/derived/` with a banner). Run: `streamlit run app/streamlit_app.py`.

## How we work
Branches `name/topic`, small pull requests into `main`, describe what changed and how you checked it.
Before committing pipeline changes: `python -m pytest -q`.

## Real-file inspection recorded during RSN implementation

The 28 June primary GCOV file was opened through authenticated ASF access.
Report: `data/crops/inspection_2026-06-28_T034_4005_DHDH.json`.
Frequency-A `HHHH` and `HVHV` are float32 arrays of 33,768 rows by 34,344
columns, on EPSG:32643 with +10 m x spacing and -10 m y spacing. The file
identifies track 34, frame 79, descending, left-looking, starting at
2026-06-28T13:42:39. The frequency-A mask is uint8 with fill value 255.
Nine small mask patches within the study box contained values 0, 1 and 255;
this sampling is not a measurement of whole-box coverage. Cropped valid
fractions must be taken from the crop manifest.


## Real processing and source quality

Authenticated remote reads succeeded for all five configured GCOV dates and the
28 June–10 July GUNW pair. Source files are inspected and streamed as windows;
full HDF5 downloads are also queued locally to fulfill R2/R7. Use `pipeline.acquire` for real
acquisition, including quality checks; `pipeline.preflight --require-crops`
checks the primary quality stamps before `pipeline.run_all`.

The real GCOV mask description defines 0 as invalid or partially focused and
255 as outside acquisition. GUNW mask bits 0–7 encode the water flag and reference/
secondary subswath digits; a zero subswath digit is invalid. Bits 8–15 and 16–23
are secondary/reference RSLC anomalies. The quality pass excludes those anomalies
and requires full valid native support for each retained 40 m output pixel.
The chosen coherence is float32 at 20 m, with NaN fill, under the wrapped
interferogram HH path stated above. Zero coherence remains a valid measurement.

Real results and their interpretation limits are recorded in
`docs/REAL-DATA-RUN.md`; actual coverage is in `data/crops/manifest.json`.
The current global linear-power threshold is +30.2092 dB and classifies nearly the entire
scene as dark. The app withholds water estimates and flood matches, without substituting
synthetic results or the earlier method. Zero slide candidates at the brief thresholds does
not mean there were no slides. Zone polygons were refined using WorldCover 2021;
2026 land cover and control stability remain unverified. Supplied rainfall is
NASA POWER/MERRA-2; do not label it IMERG unless the input is actually replaced.
