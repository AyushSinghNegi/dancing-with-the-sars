# CONTEXT.md: read this first (humans and AI assistants)

Paste this file at the start of every Claude / ChatGPT chat about this project.
Then read **`plotholes.md`**: the list of claims and results that are still unverified, inconsistent
or open to challenge. Paste it too whenever the chat is about story text, slides, the video, the
README or the project page.

## What we are building
**MonsoonLens**: an open web app that shows what NASA-ISRO **NISAR** L-band radar saw
around **Pune, India** during the **July 2026 monsoon**: new flood water, likely
landslide zones on the Western Ghats slopes, and what radar could *not* see,
checked against reported events. NASA Space Apps Challenge 2026, challenge
"Dancing with the SARs", local event GDG Ahlen (virtual). Team: Ayush
(app, integration, lead), RSN (data and science), Urvashi Negi (validation, story, pitch).

## Non-negotiable rules
1. **Every number on screen comes from our pipeline output or a cited source.** No invented,
   estimated or "illustrative" numbers, ever. If a value is missing, show "not available".
2. **Synthetic data stays in `data/demo/`** and the app shows a DEMO banner whenever it uses it.
   `MONSOONLENS_DEMO=1` is the only way to touch it. Never copy demo outputs into `data/derived/`.
3. Compare backscatter only between dates with the **same track, radar mode and polarisation**
   (`config.same_mode`). Mode is field 9 of a GCOV file name (`4005`); pol is field 10 (`DHDH`).
4. Never commit `.h5` files, `.netrc`, tokens, or anything over 20 MB.
5. Say "likely slide zone", never "landslide", for radar detections that no report confirms.
6. **Check `plotholes.md` before any public text ships.** Do not repeat a claim listed there as open.
   When you fix a point, move it to "Resolved"; when you find a new one, add it.

## Data (all real except `data/demo/`)
| What | Where | Notes |
|---|---|---|
| NISAR GCOV 28 Jun 2026 (before) | `config.PRIMARY["before"]` | track 034 D, frame 079, mode 4005, DHDH |
| NISAR GCOV 10 Jul 2026 (after) | `config.PRIMARY["after"]` | same track, mode, pol |
| NISAR GUNW 28 Jun to 10 Jul | `config.PRIMARY["pair"]` | coherence for slide zones |
| Candidate NISAR scenes (49 Pune, 146 Brahmaputra backup) | `data/reference/candidate_scenes.csv` | from NASA CMR |
| JRC Global Surface Water occurrence v1.4 | `data/crops/aux_jrc_occurrence.tif` | permanent water = occurrence >= 50% |
| Copernicus GLO-30 DEM: elevation, slope | `data/crops/aux_elevation.tif`, `aux_slope.tif` | public, no login |
| NASADEM (NASA/USGS): elevation, for the elevation-map check only | `data/crops/aux_nasadem_elevation.tif` | RSN, from `rsn/pipeline`; `nasadem_provenance.json` |
| Daily rainfall (GPM IMERG Late Run daily, GPM_3IMERGDL v07, via Giovanni) | `data/reference/rainfall.csv` | Urvashi, U2; details in `data/reference/SOURCES.md` |
| Reported events | `data/reference/events.geojson` | Urvashi, U3 (schema below) |

Project box (WGS84): lon 73.30 to 74.10, lat 18.15 to 18.90. Analysis grid: UTM 43N (EPSG:32643), 40 m.

NISAR file layout (confirmed from ASF docs, check with `pipeline.inspect_h5` on the real file):
- GCOV: `/science/LSAR/GCOV/grids/frequencyA/` holds `HHHH`, `HVHV` (gamma0, linear power),
  `mask` (1..N valid subswath, 0 invalid, 255 fill), `numberOfLooks`, `rtcGammaToSigmaFactor`, `xCoordinates`,
  `yCoordinates`, `projection` (EPSG code). Full-frame layers are ~5 GB each, so we stream the box only.
- GUNW: coherence at `.../frequencyA/unwrappedInterferogram/HH/coherenceMagnitude`
  (the code finds the finest coherence layer automatically). GUNW `mask` is a 3-digit WRS code
  (water flag, reference subswath, secondary subswath): valid where both subswath digits are non-zero
  and mask != 255. The GUNW grid is about 80 m.

## Pipeline (python -m pipeline.<step>)
| Step | Module | Output |
|---|---|---|
| Inspect a file | `inspect_h5` | paths, EPSG, spacing, mask values |
| Cut to the box (streams from ASF) | `crop --primary`, `crop --timeline` | `data/crops/*_HH.tif`, `_HV.tif`, `_COH.tif`, `manifest.json` |
| JRC water + DEM | `ancillary` | `data/crops/aux_*.tif` |
| New water | `water` | `water_stats.csv`, `new_water.geojson` |
| Slide zones | `slide_zones` | `slide_zones.geojson` |
| Validation | `validate` | `validation.csv`, `validation_summary.json` |
| Timeline | `timeline` | `timeline.csv` |
| Everything + map images | `run_all` | `overlays/`, `geotiff/`, `bounds.json`, `metrics.json` |

Crops are stored as int16 GeoTIFF (dB x 100); coherence as uint8 (x 250).

### Method in one paragraph
Lee-filtered HH in dB. Water threshold per date = Kittler-Illingworth (minimum error) on a balanced sample of
JRC reservoir/river cores (occurrence >= 90%) and never-water land, clipped to -20..-11 dB. In the real Pune
crops open water sits near -16 dB, dry land near -5 dB, nothing darker than about -19 dB. New water =
water on 10 Jul, not on 28 Jun, at least 3 dB darker, outside permanent water, slope <= 5 deg,
patch >= 4 px. "Possible water under cover" = >= 3 dB brighter on flat vegetated or built ground
(L-band double bounce); shown, never counted. Slide zones = slope >= 15 deg AND coherence < 0.35
AND coherence < 0.6 x its 1 km local median AND (HV drop >= 3 dB OR HH rise >= 3 dB); scored 0-1.

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
Before committing pipeline changes: `python -m pytest -q`. App packages: `requirements.txt`; pipeline: `requirements-pipeline.txt`.
