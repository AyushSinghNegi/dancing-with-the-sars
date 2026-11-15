# MonsoonLens: What NISAR Radar Saw in the 2026 Pune Monsoon

NASA Space Apps Challenge 2026 · **Dancing with the SARs** · GDG Ahlen (virtual) · Team iGenfinity

[![Tests](https://github.com/AyushSinghNegi/dancing-with-the-sars/actions/workflows/tests.yml/badge.svg)](https://github.com/AyushSinghNegi/dancing-with-the-sars/actions/workflows/tests.yml)

Clouds hide the ground during the monsoon, which is exactly when people need to see it.
NASA-ISRO's **NISAR** L-band radar sees through cloud and rain. MonsoonLens uses two NISAR passes
over Pune (28 June and 10 July 2026), bracketing the 3-8 July floods and landslides, to map:

- **New water**, split into reservoirs and rivers rising and flooding where no water was recorded 1984 to 2021
- **Likely slide zones** on the Western Ghats slopes, from lost radar coherence and vegetation loss
- **What radar could not see** (dense city streets, water that drained, slides smaller than a pixel),
  checked against reported events

And it turns them into things people can use:

- **Check a place**: pick any of 431 villages, towns and suburbs (or click the map) and see what NISAR found
  within 2, 5 or 10 km, with a link you can share
- **Three languages, light and dark**: English, Marathi (मराठी) and German (Deutsch), in light or dark mode
  (open a page in a language with `?lang=mr` or `?lang=de`)
- **Field check list**: every likely slide zone ranked, with NISAR image chips of the spot, why it was flagged and
  which independent checks it passed; as a printable page, KML for Google Earth and phones, CSV and GeoJSON
- **Season slider**: open water on five NISAR passes of the same orbit, 28 June to 14 October
- **Animated overview**: NISAR passes over Pune and its radar clears the monsoon cloud to show the real 10 July
  radar image and findings (the cloud is drawn as an illustration and labelled as one)
- **Every number checked**: 18 reported events, a second NISAR orbit, a second elevation map (NASA NASADEM), and
  the water threshold moved by 1 dB either way

> Live app: **https://monsoonlens.streamlit.app** (real NISAR results for Pune).
> Results: 8.5 km² of reservoirs and rivers rising, 0.36 km² of flood water still standing on 10 July,
> 50 likely slide zones, checked against 18 reported events and a second NISAR orbit. Every number is
> explained on the app's Method page.

## Quick start
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Rebuild the results from NISAR (needs a free NASA Earthdata login):
```bash
pip install -r requirements-pipeline.txt
python -m pipeline.ancillary          # JRC water + DEM slope (public, no login)
python -m pipeline.crop --primary     # streams only the Pune box from the 3 NISAR files
python -m pipeline.crop --granule ... # optional: the second-orbit pair and timeline dates (see pipeline/config.py)
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
| `plotholes.md` | Open points: unverified claims, inconsistencies and limits to fix or state before submission |
| `pipeline/` | NISAR reading, cropping, water, slide zones, validation, timeline, rendering |
| `app/` | Streamlit app (overview, story, explore map, check a place, field check list, method) |
| `data/reference/` | Scene list, rainfall, reported events |
| `data/crops/` | Pune-box crops of NISAR files and public context layers |
| `data/derived/` | Everything the app shows (small files, each traceable to a NISAR file ID) |
| `content/` | Story text and style |

## Use of AI
Following the Space Apps rules on AI disclosure:
- Most of the pipeline and app code, the tests, the first drafts of the story text (English, Marathi and German) and the
  first pass of the reported-events research were written with **Claude (Anthropic)**, directed and reviewed by the
  team. So were the source checks on the reported events, the style guide, the slide outline, the validation
  table, the "couldn't see" text and `plotholes.md`.
- Many of these commits carry a `Co-Authored-By: Claude` line or a "Claude" author name, but not all of them.
  The commits on the `urvashi/content` branch (reference data, event checks, story, style, slide outline and
  validation text) were made with Claude and carry no such line. The commit history therefore understates the
  AI use; this section is the full statement.
- **ChatGPT (OpenAI)** was used by one team member for data analysis.
- No measurement is AI-generated. Every number in the app is computed by `pipeline/` from the NISAR files listed on
  the Method page, or comes from a linked source. Map images are rendered from radar data by our code.
- `data/demo/` holds **synthetic** radar data in NISAR's file format, used only for development and tests; the app
  labels it and never mixes it with real results.

## Data and credits
NISAR L2 GCOV and GUNW provisional products, NASA/JPL-Caltech and ISRO, via ASF DAAC.
JRC Global Surface Water (Pekel et al., 2016). Copernicus GLO-30 DEM (ESA); NASADEM (NASA/USGS) for the elevation-map check. GPM IMERG Late Run daily precipitation (GPM_3IMERGDL v07, NASA GES DISC, via Giovanni; see
`data/reference/SOURCES.md`). NASA Worldview / GIBS daily true-colour imagery for the cloud check
(`content/cloud_check.md`).
Method, limits and validation: see the app's Method page and `CONTEXT.md`.

## Licence
Code: see `LICENSE`. Data products keep their providers' terms.
