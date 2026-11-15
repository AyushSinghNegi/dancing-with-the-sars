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
- **Four languages, light and dark**: English, Hindi (हिन्दी), Marathi (मराठी) and German (Deutsch), in light or
  dark mode (open a page in a language with `?lang=hi`, `?lang=mr` or `?lang=de`)
- **Field check list**: every likely slide zone ranked, with NISAR image chips of the spot, why it was flagged and
  which independent checks it passed; as a printable page, KML for Google Earth and phones, CSV and GeoJSON
- **App tour**: "Take the tour" walks a first-time visitor through all six pages in twelve short steps, in any of
  the four languages, on desktop and phone
- **3D view**: the study area as a relief model (Copernicus elevation, heights ×2) with the findings painted on it
  and 3D pins for slide zones, flood patches and reported events; "Fly over the findings" flies to each one with a
  one-line explanation (deck.gl, files made by `pipeline/terrain3d.py`)
- **Season slider**: open water on five NISAR passes of the same orbit, 28 June to 14 October
- **Animated overview**: NISAR passes over Pune and its radar clears the monsoon cloud to show the real 10 July
  radar image and findings (the cloud is drawn as an illustration and labelled as one)
- **Every number checked**: 18 reported events, a second NISAR orbit, a second elevation map (NASA NASADEM), and
  the water threshold moved by 1 dB either way

> Live app: **https://monsoonlens.streamlit.app** (real NISAR results for Pune).
> Demo video (30 s): https://youtu.be/gMXD7zp72yY. Full walkthrough (2 min): https://youtu.be/GY2MDmud-Q4.
> Results: 8.5 km² of reservoirs and rivers rising, 0.36 km² of flood water still standing on 10 July,
> 50 likely slide zones, checked against 18 reported events and a second NISAR orbit. Every number is
> explained on the app's Method page.

## Team iGenfinity

What each of us decided, led or did. The tools we used, AI included, are listed under [Use of AI](#use-of-ai).

- **Ayush Singh Negi**, team lead (app and integration). Set the project's direction with the team: the
  challenge, Pune and the July 2026 event. Decided what the app shows and how, reviewed and merged every pull
  request, recorded the voice-over for both demo videos, and published the videos, deck and reports.
- **Rajendra Singh Negi (RSN)**, data and science. Built his own NISAR pipeline on the `rsn/pipeline` branch
  (draft PR #9): verified raw downloads, NISAR's native quality masks, and a scientific check that showed a
  single global water threshold fails on this scene. His 14 October crop feeds the season timeline, and his
  NASADEM elevation feeds the second-elevation-map check.
- **Urvashi Negi**, validation, story and pitch. Replaced NASA POWER rainfall with GPM IMERG; checked the
  reported events against their sources and moved one (E016) to where its source places the flooding; added the
  chance-level test that shows the flood matches are no better than chance, and the roads, railways and
  settlements near each slide zone; built the season and pass-by-pass map controls; kept the list of open points
  (`plotholes.md`); read the Submission Guide and cut the deck to its 7-slide limit; wrote the project page text
  and demo scripts; corrected the German.

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
| `data/demo/` | **Synthetic** radar data in NISAR's file format, for development and tests only; the app labels it and never mixes it with real results |
| `content/` | Story text in four languages, style guide, validation table, cloud check, project page, demo script |
| `deliverables/` | Code that builds the deck and reports from the pipeline outputs, and their PowerPoint and PDF files |
| `video/` | Code that renders the demo videos from the app and the NISAR layers, and mixes the voice-over |
| `tests/` | pytest suite (pipeline, outputs, translations) |

## Data and credits
NISAR L2 GCOV and GUNW provisional products, NASA/JPL-Caltech and ISRO, via ASF DAAC.
JRC Global Surface Water (Pekel et al., 2016). Copernicus GLO-30 DEM (ESA); NASADEM (NASA/USGS) for the elevation-map check. GPM IMERG Late Run daily precipitation (GPM_3IMERGDL v07, NASA GES DISC, via Giovanni; see
`data/reference/SOURCES.md`). NASA Worldview / GIBS daily true-colour imagery for the cloud check
(`content/cloud_check.md`).
Method, limits and validation: see the app's Method page and `CONTEXT.md`.

## Use of AI
We used AI tools, and the Space Apps rules ask us to say how:
- **Claude (Anthropic)** wrote most of the pipeline and app code, the tests, and the first drafts of the story
  text and its translations (Hindi, Marathi, German) and the first pass of the reported-events research, directed
  and reviewed by the team. It also helped build the deck, reports, figures and video code, check the reported
  events against their sources, and draft the style
  guide, slide outline, validation table, "couldn't see" text and `plotholes.md`.
- **ChatGPT (OpenAI)** was used by one team member for data analysis.
- Commits made with Claude carry a `Co-Authored-By: Claude` line or a "Claude" author name. Some on the
  `urvashi/content` branch do not, so the commit history understates the AI use; this section is the full statement.
- No measurement is AI-generated: every number in the app is computed by `pipeline/` from the NISAR files listed
  on the Method page, or comes from a linked source. No image, video or audio is AI-generated: map images and the
  videos are rendered by our code, the voice-over is our own recording, and the music and sound effects are
  synthesised by our code (`video/audio.py`).

## Licence
Code: see `LICENSE`. Data products keep their providers' terms.
