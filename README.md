# MonsoonLens: what NISAR radar saw in the 2026 Pune monsoon

NASA Space Apps Challenge 2026 · **Dancing with the SARs** · GDG Ahlen (virtual) · Team iGenfinity

Clouds hide the ground during the monsoon, which is exactly when people need to see it.
NASA-ISRO's **NISAR** L-band radar sees through cloud and rain. MonsoonLens uses two NISAR passes
over Pune (28 June and 10 July 2026), bracketing the 3-8 July floods and landslides, to map:

- **New flood water** on flat ground, separated from rivers and reservoirs that are always wet
- **Likely slide zones** on the Western Ghats slopes, from lost radar coherence and vegetation loss
- **What radar could not see** (dense city streets, water that drained, slides smaller than a pixel),
  checked against reported events

> Status: pipeline and app are being built during the hackathon (14-15 Nov 2026).
> Until the real NISAR crops are in, the app runs on clearly labelled **synthetic** data.

## Quick start
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Rebuild the results from NISAR (needs a free NASA Earthdata login):
```bash
python -m pipeline.ancillary          # JRC water + DEM slope (public, no login)
python -m pipeline.crop --primary     # streams only the Pune box from the 3 NISAR files
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
JRC Global Surface Water (Pekel et al., 2016). Copernicus GLO-30 DEM (ESA). GPM IMERG (NASA GES DISC).
Method, limits and validation: see the app's Method page and `CONTEXT.md`.

## Licence
Code: see `LICENSE`. Data products keep their providers' terms.
