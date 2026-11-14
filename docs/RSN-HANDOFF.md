# RSN data and science hand-off

Branch: `rsn/pipeline`. Current specification: Brief RSN — Data and Science.
Python 3.11.18; pipeline 0.5.0. The app reads real outputs in `data/derived/`.

## Current result and release status

The required processing and file contracts are implemented, but **R5 is not
scientifically cleared**. Global linear-power Otsu on 10 July yields +30.2092 dB
and labels nearly all valid pixels as dark. The app therefore withholds water
estimates, water overlays and flood-report matches. Diagnostic CSVs/rasters remain
available with their failed quality status. A zero diagnostic area is not evidence
of no flooding. No alternative algorithm is silently substituted.

The independent NASADEM/20°/HV-drop/coherence slide screen has 120 candidate
pixels before cleanup, all in one- or two-pixel components. No component reaches
the configured three-pixel minimum. Zero zones does not mean no landslides occurred.
Four eligible slide reports consequently miss at the fixed 200 m distance.

All five radar dates are processed. `timeline.csv` has 40 zone/polarization/date
rows. Historical context-method results are documented in `BASELINE-RUN.md`;
the complete local baseline is preserved under ignored `data/runs/context-baseline/`.
Do not combine baseline figures with current maps or validation counts.

## Reproduce

```bash
python3.11 -m venv .venv
. .venv/bin/activate
pip install -r requirements-tested.txt
# Configure Earthdata locally; never commit or share credentials.
python -c "import earthaccess; earthaccess.login(strategy='interactive', persist=True)"
python -m pipeline.download_raw       # six files; resume retained .part files
python -m pipeline.ancillary          # JRC + NASADEM, metric-grid slope
python -m pipeline.acquire --primary  # local originals when present; otherwise ranged reads
python -m pipeline.acquire --timeline
python -m pipeline.review_zones       # small WorldCover windows; original footprints preserved
python -m pipeline.preflight --require-crops
python -m pipeline.run_all
python -m pytest -q
streamlit run app/streamlit_app.py
```

This checkout's tested interpreter is `.venv311/bin/python`. The original `.venv`
remains available for the resumable download job; it is not the tested app runtime.
Raw downloads are ignored by Git, checked for HTTP byte count and HDF5 signature,
and have local receipts. These are transport checks, not independent checksums.
`data/crops/inspection_*.json` records actual dataset paths, shape, CRS and fill.

## Deliverables for Ayush and Urvashi

| Brief | Output / status |
|---|---|
| R1 | Earthdata authenticated; Python 3.11.18 and exact dependency freeze tested |
| R2 | Three full primary files downloaded locally; cropped products already available |
| R3 | Six source inspection reports and observed paths/quality flags in CONTEXT.md |
| R4 | Four HH/HV PNGs, coherence PNG, GeoTIFFs, bounds.json; all source masks applied |
| R5 | water_new_20260710.png, new_water.geojson, GeoTIFF, water_stats.csv, water_sensitivity.csv, water_threshold.json; diagnostic only, QC failed |
| R6 | NASADEM elevation/slope/provenance, slide_zones.geojson/PNG, control_stats.csv; zero qualifying zones |
| R7 | Remaining three full GCOV downloads queued; all five scene crops already processed; extra GUNW is optional |
| R8 | timeline.csv: four zones × HH/HV × five dates; zone_timeline.csv alias; water_timeline.csv is supplementary |
| R9 | validation.csv: fixed 200 m primary result, separate precision-aware result, distances/reasons; rejected water not scored |
| R10 | README, CONTEXT, source IDs, versions, this guide and REAL-DATA-RUN.md |
| R11 | App checks, quality warning, unit/date review, and video wording below |

WorldCover desk review refined the forest/cropland/river polygons to connected
patches of their target 2021 class, preserving the initial footprints. The city
control remains 83.4% built-up in that reference. The river footprint contains
only eight 40 m cell centres; boundary mixing limits its median's interpretation.
A historical land-cover classification does not establish 2026 land cover or
control stability. The urban control cannot validate performance on vegetated slopes.

`event_source_review.csv` distinguishes publisher-text corroboration from reports
that could not be independently read. All coordinates remain approximate supplied
locations. The Patan report has an unresolved Lohagad/Visapur naming difference.
Neither nearby detections nor missing detections establish a cause or absence of damage.

The supplied rainfall is NASA POWER/MERRA-2. IMERG replacement is Urvashi's input
work and has not been represented as complete. The optional 10–22 July GUNW is not
required for the primary case and is not part of this run.

## Method details

Lee filtering operates in linear power; scikit-image Otsu uses all finite positive
10 July HH power values, 256 bins, no clipping or event-based tuning. One threshold
is applied to both dates and varied by ±1 dB on both for sensitivity. Candidate
new water is dark after, not dark before, outside JRC occurrence ≥50%, ≥4 pixels.
The water-quality guard rejects a split with ≥95% of valid pixels classed dark.
It flags the failure; it does not alter Otsu or create a replacement flood estimate.

Slides require NASADEM slope ≥20°, HV drop ≥3 dB, coherence <0.35 and ≥3 connected
pixels. HH rise/local coherence contrast are diagnostics. A 0–1 heuristic score
is an evidence ranking, not a probability. All thresholds live in config.py and
are exported in metrics.json. Matching distances use the 40 m metric grid;
reported point precision is exported separately from the fixed 200 m test.

GCOV quality excludes 0 and 255. GUNW quality decodes reference/secondary subswaths
in bits 0–7 and excludes RSLC anomaly flags in bits 8–23. Retained 40 m cells need
full valid native support. Unknown coverage is nodata, not a negative detection.

## Short science explanation for the video

We compare NISAR radar observations before and after the reported monsoon events.
The requested water threshold failed its quality check on these scenes, so we do
not claim a flood-area estimate. Our independent slide screen found no patches
large enough to pass all three criteria, which does not mean no slides occurred.
The app shows the radar observations, five-date zone changes, reported events and
these limits so viewers can see what the data supports.

## Team delivery

`data/derived/` is the app hand-off; `docs/PULL_REQUEST.md` contains the prepared
review description. GitHub push/PR requires local write authentication, requested
from the user. No direct team message or email has been sent.

Editable diagrams: [pipeline](rsn-pipeline.drawio), [radar through cloud](radar-clouds.drawio).
The Story SVG is exported from draw.io with the editable model embedded:

```bash
drawio --no-sandbox --export --format svg --embed-diagram \
  --output app/static/radar-clouds.svg docs/radar-clouds.drawio
```
