# Implement RSN real-data pipeline, brief contracts and scientific quality checks

Process five compatible NISAR GCOV scenes and the June 28–July 10 GUNW pair into
quality-masked Pune crops, previews, timelines and reported-event comparisons.
Implement the brief's Python 3.11 environment, shared linear-power Otsu, NASADEM
20°/HV-drop/coherence slide screen, fixed 200 m validation, and required filenames.

The scientific check found a degenerate global Otsu split (+30.2092 dB, nearly all
pixels dark). Water outputs are explicitly diagnostic; the app withholds flood
area, overlays and flood matching. The stricter slide screen yields zero qualifying
zones after removing one/two-pixel components. This PR is ready for implementation
review but **does not claim scientific acceptance of a flood product**.

Additional work: resumable local-only raw downloads; source inspection and native
quality masks; WorldCover-reviewed zone footprints with originals preserved;
40-row HH/HV timeline; control statistics; source-review notes; draw.io diagrams;
real/demo separation; reproducible versions and hand-off/video text.

Validation: 33 regression tests on Python 3.11.18; full real and isolated synthetic
pipeline runs; app navigation/quality-warning checks; raster alignment, nodata,
area consistency, image decoding, geometry and file-size checks. Detailed recorded
results are in docs/qa-results.json. Raw HDF5 and credentials are ignored.

Remaining review limitations: R5 water calibration, approximate report locations,
2026 control/land-cover stability, and the optional secondary GUNW. The supplied
rainfall is correctly labeled POWER/MERRA-2; an IMERG replacement is not included.

Review docs/RSN-HANDOFF.md and docs/REAL-DATA-RUN.md before interpreting figures.

## Integration status against current main

This branch was implemented from commit `33d867d`. At publication, `main` had
advanced to `dce5fa0` with app hardening/content integration, IMERG rainfall,
Kittler–Illingworth water classification and a second-track check. Those changes
have not been integrated or tested with this branch. The POWER rainfall limitation
above describes this branch's recorded run, not the current main branch.

Keep this PR in draft until overlapping pipeline, generated data and app changes
are reconciled and the combined implementation is rerun. Do not combine the
scientific results from the two methods or discard upstream content during merging.
All six required raw originals are downloaded locally (31.013 GB); only their
verification inventory and eligible cropped/derived outputs are committed.
