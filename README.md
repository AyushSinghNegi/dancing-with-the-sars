# MonsoonLens: what NISAR radar saw in the 2026 Pune monsoon

NASA Space Apps Challenge 2026 · **Dancing with the SARs** · GDG Ahlen (virtual) · Team iGenfinity

Clouds hide the ground during the monsoon, which is exactly when people need to see it.
NASA-ISRO's **NISAR** L-band radar sees through cloud and rain. MonsoonLens uses two NISAR passes
over Pune (28 June and 10 July 2026), bracketing the 3-8 July floods and landslides, to map:

- **Candidate new water**, with failed classifications clearly withheld from flood reporting
- **Likely slide zones** on the Western Ghats slopes, from lost radar coherence and vegetation loss
- **What radar could not see** (dense city streets, water that drained, slides smaller than a pixel),
  checked against reported events

> Status: real NISAR processing is implemented. The brief's global linear-power Otsu split
> fails on these scenes, so the app withholds flood estimates and flood matching.
> Radar imagery, five-date zone timelines and the slide screen remain available.
> See [the real-data run report](docs/REAL-DATA-RUN.md) for measured results and review limits.
> Synthetic data requires explicit `MONSOONLENS_DEMO=1` and displays a DEMO banner.

## Quick start
```bash
python3.11 -m venv .venv
. .venv/bin/activate
pip install -r requirements-tested.txt
streamlit run app/streamlit_app.py
```

Rebuild the results from NISAR (needs a free NASA Earthdata login):
```bash
python -m pipeline.download_raw       # resumable six-scene download, ignored data/raw/
python -m pipeline.ancillary          # JRC water + NASADEM slope (Earthdata Login)
python -m pipeline.acquire --primary     # streams only the Pune box from the 3 NISAR files
python -m pipeline.acquire --timeline # acquire the compatible monsoon dates and apply quality masks
python -m pipeline.review_zones       # WorldCover 2021 desk review; originals preserved
python -m pipeline.run_all            # water, slide zones, validation, timeline, map images
```

Developer test run on synthetic data (never mixed with real results):
```bash
MONSOONLENS_DEMO=1 python -m pipeline.run_all --synthetic
python -m pytest -q
```

## Repository
| Path | What |
|---|---|
| `CONTEXT.md` | Project brief, rules, data paths, method: read first |
| `pipeline/` | NISAR reading, cropping, water, slide zones, validation, timeline, rendering |
| `app/` | Streamlit app (landing, story, explore map, method) |
| `data/reference/` | Scene list, rainfall, reported events |
| `data/crops/` | Pune-box crops of NISAR files and public context layers |
| `data/derived/` | Everything the app shows (small files, each traceable to a NISAR file ID) |
| `content/` | Story text and style |

## Data and credits
NISAR L2 GCOV and GUNW provisional products, NASA/JPL-Caltech and ISRO, via ASF DAAC.
JRC Global Surface Water (Pekel et al., 2016). [NASADEM_HGT.001](https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001).
Analysis footprints use [ESA WorldCover 2021 v200](https://doi.org/10.5281/zenodo.7254221).
© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.
The supplied rainfall series is NASA POWER/MERRA-2; IMERG remains a planned replacement.
Method, limits and validation: see the app's Method page and `CONTEXT.md`.

## Licence
Code: see `LICENSE`. Data products keep their providers' terms.

## RSN data and science hand-off

See [the run guide](docs/RSN-HANDOFF.md) for R1-R11 commands, outputs, validation
checks and scientific review notes. The additional outputs include water
threshold sensitivity, HH/HV zone timelines, control statistics and JSON source
inspection reports. Exact tested dependencies are in `requirements-tested.txt`.

## Reproducible method and limits

The 40 m EPSG:32643 grid combines quality-masked GCOV HH/HV and GUNW HH coherence.
Lee filtering operates in linear power. Scikit-image Otsu on the filtered 10 July
HH linear image provides one shared threshold for all compatible dates. Candidate
new water is dark after, not dark before, outside JRC occurrence ≥50%, in patches
of ≥4 pixels. The shared threshold is varied by ±1 dB on both dates. The computed
threshold and degeneracy check are in `data/derived/water_threshold.json`.

**Scientific result:** the unconstrained global threshold is +30.2092 dB, with
nearly 100% of the image below it. This fails the ≥95% dark-fraction guard.
Water-area zeros and masks are rejected diagnostics, not evidence of no flooding.
The app suppresses water claims/layers and does not score flood reports. No
parameter was tuned to improve reported-event hits. A usable water classifier
still needs scientific calibration; this limitation is not hidden by substituting
the earlier context method. [Historical baseline](docs/BASELINE-RUN.md).

Likely slide zones require NASADEM slope ≥20°, coherence <0.35 and HV drop ≥3 dB,
with ≥3 connected pixels. HH change and local coherence contrast are diagnostics,
not selection criteria. The current run has zero qualifying zones. This is a
screening result, not evidence of no landslides. The evidence score is not a probability.
Validation counts use a fixed 200 m radius; location precision and an additional
precision-aware comparison are retained separately. Distances are on the 40 m grid.

Primary dates are 28 June and 10 July 2026; additional compatible GCOV dates are
22 July, 15 August and 14 October. Exact IDs, coverage and masks are in
[the run report](docs/REAL-DATA-RUN.md), `data/crops/manifest.json` and
`data/derived/metrics.json`. `timeline.csv` is the required four-zone HH/HV median
series; `zone_timeline.csv` is an alias; `water_timeline.csv` is supplementary.
Python 3.11.18 is tested; exact dependencies are in `requirements-tested.txt`.

Provisional calibration, recording-mode changes, 40 m resolution, urban double
bounce, monsoon vegetation and flooding that drained between passes limit the
interpretation. Footprints are desk-reviewed using a 2021 land-cover reference;
that does not establish their 2026 condition. The urban control is not a control
for steep vegetated slopes. Reports are approximate, incomplete references, not
exhaustive field truth. After regenerating outputs, restart Streamlit to clear
cached tables and images. All editable diagrams are `.drawio` files in `docs/`.
