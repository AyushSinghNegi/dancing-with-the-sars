# Superseded context-method run

Historical comparison only; these are not the current app results.

# MonsoonLens real-data run

Completed real processing and timeline update: 2026-11-14T17:33:02+00:00.
Primary map run: 2026-11-14T12:53:19+00:00; pipeline 0.4.0.

Earthdata Login and authenticated ranged HDF5 access succeeded. Five GCOV scenes
and the primary GUNW pair were inspected and cropped by streaming the study
window. No full-frame HDF5 download was required. All outputs described here are
real-data outputs in `data/derived/`; `demo` is false in their metadata.

## Results

| Output | Observed result |
|---|---|
| New open water, 28 June to 10 July | 6.8208 km² in 350 patches |
| After-threshold ±1 dB sensitivity | 3.1344–10.3440 km² |
| Possible water under cover, excluded from new-water total | 23.8768 km² |
| Likely slide zones | 4 zones, 2.4 ha total; 0 high, 3 medium, 1 low |
| Valid common radar/auxiliary coverage | 95.81% of the analysis grid |
| Compatible timeline dates | 2026-06-28, 2026-07-10, 2026-07-22, 2026-08-15, 2026-10-14 |
| Zone series | Four footprints × two polarizations × five dates = 40 rows |

Both HH thresholds are -14 dB, at the configured upper
bound of the JRC-balanced Otsu range. Only 59.3% of
valid JRC permanent-water pixels were dark enough on the before date. These are
material interpretation limits: the water output is a method-dependent radar
candidate layer, not a confirmed or exhaustive flood inventory. The sensitivity
range is not a confidence interval. Heuristic slide confidence is not a probability.

## Comparison with supplied reports

The supplied reference set contains 18 events. Of 11
flood reports, 10 met the coverage, timing and location
criteria: 0 nearby detections and 10 misses.
Of 7 slide reports, 4 were observable:
2 nearby detections and 2 misses. The exact
buffers, dates, distances and exclusion reasons are in `validation.csv`.
Nearby detections do not establish that a reported event caused that radar change.
These counts are not accuracy estimates; reference reports have not been
independently field-verified here. Three candidate slide zones have no observable
slide report within the separate 2 km unreported-zone check.

The provisional central-Pune control contains 2935 valid
pixels and 0 slide-candidate pixels. Its median HV
change is +0.151 dB and median coherence is
0.632. This flat urban control is not independent proof
of performance on steep vegetated slopes. All four footprint labels remain
explicitly unreviewed until RSN confirms land cover and control stability.

## Input coverage and masks

Analysis grid: EPSG:32643, 40 m, 2,091 rows × 2,127 columns. GCOV frequency A is
10 m native; the selected wrapped GUNW HH coherence is 20 m native. Each scene's
JSON inspection report records the actual dataset paths, EPSG, spacing and fill.
GCOV masks exclude 0 and 255. GUNW masks require valid reference and secondary
subswaths, with RSLC anomaly bits 8–23 clear. Every retained grid cell requires
full valid native mask support. Geometric box coverage alone is not usable coverage.

| Crop | Usable grid fraction | Quality rule |
|---|---:|---|
| 2026-06-28_2026-07-10_T034_4000 | 96.00% | valid-subswaths-no-rslc-anomalies-v1 |
| 2026-06-28_T034_4005_DHDH | 95.86% | fully-focused-native-support-v1 |
| 2026-07-10_T034_4005_DHDH | 95.84% | fully-focused-native-support-v1 |
| 2026-07-22_T034_4005_DHDH | 95.90% | fully-focused-native-support-v1 |
| 2026-08-15_T034_4005_DHDH | 95.87% | fully-focused-native-support-v1 |
| 2026-10-14_T034_4005_DHDH | 95.86% | fully-focused-native-support-v1 |

Exact source granule IDs:

- `NISAR_L2_PR_GUNW_024_034_D_079_025_4000_SH_20260628T134239_20260628T134314_20260710T134239_20260710T134313_P05023_N_F_J_001`
- `NISAR_L2_PR_GCOV_024_034_D_079_4005_DHDH_A_20260628T134239_20260628T134314_P05023_N_F_J_001`
- `NISAR_L2_PR_GCOV_025_034_D_079_4005_DHDH_A_20260710T134239_20260710T134313_P05023_N_F_J_001`
- `NISAR_L2_PR_GCOV_026_034_D_079_4005_DHDH_A_20260722T134238_20260722T134313_P05023_N_F_J_001`
- `NISAR_L2_PR_GCOV_028_034_D_079_4005_DHDH_A_20260815T134237_20260815T134311_P05023_N_F_J_001`
- `NISAR_L2_PR_GCOV_033_034_D_079_4005_DHDH_A_20261014T134237_20261014T134311_P05023_N_F_J_001`

## Verification and hand-off

- 30 regression tests passed; real-mode Overview, Story, Explore and Method passed
  Streamlit AppTest, including every Story step and real/demo provenance checks.
- The live app rendered real imagery and the detection/reference layers over Pune.
- Exported GeoTIFF CRS, dimensions and transforms match the 40 m grid. Raster
  class codes and nodata are valid; raster new-water area agrees with metrics.
- PNG/WebP files decode; polygon geometries are valid; eligible files are each
  below 20 MB. Raw HDF5 and credential files are excluded from version control.
- Editable diagrams are `docs/rsn-pipeline.drawio` and `docs/radar-clouds.drawio`.
  The Story diagram is an SVG exported from draw.io with its model embedded.

Run commands, methods, retained repository choices and the short video explainer
are in [RSN-HANDOFF.md](RSN-HANDOFF.md). Exact tested dependencies are in
`requirements-tested.txt`. The supplied rainfall is NASA POWER/MERRA-2, not IMERG.
Changes and outputs are local on branch `rsn/pipeline`; no commit or push has been made.
