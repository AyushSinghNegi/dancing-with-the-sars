# MonsoonLens real-data run — brief method

Generated 2026-11-14T18:18:36+00:00; pipeline 0.5.0; Python 3.11.18.
Real NISAR products (`demo: false`). All five compatible GCOV dates and the primary
GUNW pair are inspected, quality-masked and processed on the 40 m EPSG:32643 grid.

## Scientific outcome

**No flood-area estimate is approved from this run.** Global linear-power Otsu
returns 30.2092 dB (1049.3385 linear power),
classifying 99.99955% of valid pixels as dark. This exceeds
the configured 95% guard. The app withholds water-area claims, water overlays and
flood matching. The diagnostic new-water/sensitivity values are zero after cleanup;
that is a failed classification, not evidence of no flood. The test uses no event
labels and does not silently clip the threshold or substitute the historical method.

The slope/HV-drop/coherence intersection contains 120
pixels. Every connected component is one or two pixels, below the configured
3-pixel minimum; therefore 0 slide zones survive.
This screening result does not establish absence of landslides.

| Deliverable | Result |
|---|---|
| Shared water threshold | 30.2092 dB; classification rejected |
| Common radar/auxiliary support | 95.81% |
| Likely slide zones | 0 after component cleanup |
| Eligible slide reports | 4; 0 hits, 4 misses at 200 m |
| Flood reports | 11 supplied; 10 not scored due classifier failure, 1 outside pair timing |
| Timeline | 5 compatible dates; 40 zone/polarization/date rows |
| Central-Pune control | 2935 valid pixels, 0 candidate pixels |
| Control median HV change / coherence | +0.151 dB / 0.632 |

## What changed from the preserved context-method run

| Choice | Historical context method | Current brief method |
|---|---|---|
| Runtime | Python 3.12.14 | Python 3.11.18 |
| Water threshold | per-date balanced JRC Otsu in dB, clipped −24…−14 dB | one after-date scikit-image Otsu in linear power; no clipping |
| New water | additional ≥3 dB drop and ≤5° slope | dark after, not dark before, not permanent, ≥4 pixels |
| Sensitivity | vary after threshold only | vary shared threshold on both dates |
| Slope/slide | Copernicus, 15°, HV drop OR HH rise, local coherence anomaly | NASADEM, 20°, HV drop AND low coherence |
| Validation | 500/750 m enlarged for location precision | fixed 200 m, precision-aware secondary result |
| timeline.csv | water-area series | required zone HH/HV medians |

The historical method produced 6.8208 km² of candidate
new water and 4 slide zones. Those figures are **not current
brief outputs** and were not field-confirmed. Its own clipping/sensitivity limits
are retained in [BASELINE-RUN.md](BASELINE-RUN.md). The local complete baseline,
including its source code, is under ignored `data/runs/context-baseline/`.

## Zone and report desk review

The initial forest footprint was 61.87% tree cover, farmland 44.77% cropland, and
river only 5.34% permanent water in WorldCover 2021. Forest/cropland/river polygons
were refined to the largest connected target-class patch within their original
boundaries. Their reference-class share is now 100% at the 10 m reference posting;
this is by construction, not an independent accuracy assessment. The city control
keeps its original boundary and is 83.4% built-up. Original polygons are preserved.

The resulting analysis footprints contain 3,553 / 1,735 / 2,935 / 8 cell centres
(forest / farmland / city / river). The narrow river is especially sensitive to
40 m boundary mixing. The 2021 reference does not establish 2026 land cover or
stability. The urban control does not test the steep-vegetation slide criteria.

Publisher text corroborated date/place context for 11 of 18 supplied reports,
including two through alternative supplied publisher articles. Seven remain
uncorroborated in this review because source text was unavailable. Supplied
approximate coordinates are not field-verified; Patan has a Lohagad/Visapur naming
difference. See `data/reference/event_source_review.csv`. The report set is not
complete ground truth and the hit/miss counts are not accuracy percentages.

## Input coverage and quality

Grid: 2,091 × 2,127, EPSG:32643, 40 m. GCOV frequency A is native 10 m;
selected wrapped HH coherence is native 20 m. Inspection JSONs record real paths,
CRS, fill values and masks. GCOV excludes mask 0/255; GUNW requires valid
reference/secondary subswaths and no RSLC anomaly bits 8–23. Full valid native
support is required for each retained output cell; zero coherence is valid.

| Crop | Usable fraction | Quality rule |
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

33 regression tests passed under Python 3.11.18. Real and isolated synthetic runs
completed; Overview, all five Story steps, Explore and Method passed AppTest.
The live app visibly displays the water-quality warning and suppresses failed
water estimates. Raster/image/geometry/contract checks are recorded in
`qa-results.json`. All eligible repository files are under 20 MB; raw files,
credentials and preserved intermediate arrays are ignored.

All six full HDF5 files are downloaded (31.013 GB total): the three primary
files and three additional timeline GCOV files. Cropped timeline data is also
complete. Byte counts, HDF5 signatures and readable HDF5 metadata were checked;
no independent checksum was available. Local receipts are in ignored `data/raw/`;
`data/crops/raw_download_status.json` records the verified inventory.

The hand-off and video wording are in [RSN-HANDOFF.md](RSN-HANDOFF.md).
Implementation is reviewable; scientific clearance of R5 and GitHub publishing
remain outstanding. Optional secondary GUNW is not processed; supplied rainfall
remains correctly labelled NASA POWER/MERRA-2, not IMERG.
