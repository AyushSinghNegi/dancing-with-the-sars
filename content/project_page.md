# Project page text (U7)

Draft text for the team's Space Apps project page, one section per form field in the 2026 Project
Submission Guide (spaceappschallenge.org/resources/project-submission-guide, dated 13 Nov 2026).

Rules from the guide that affect this page:

- Every required field must be filled, all in English.
- Images (JPG, PNG, GIF up to 10 MB) can be uploaded; videos and documents cannot, so link them.
- Every link must open with no login, permission or registration. Test each in a private window.
- Submit before Sunday 15 November, 11:59 p.m. in the time zone of the Local Event (GDG Ahlen).
  The page can be edited and resubmitted until then; judges see the last saved version.

Numbers are from `data/derived/` (metrics.json generated 2026-11-15T06:12Z, after the E016 correction). Recheck them after any
new pipeline run. Items in `[SQUARE BRACKETS]` still need a person to fill or confirm them.

**Corrected (plotholes.md P07, P46):** the pipeline was re-run on 15 November with E016 at its real location. Floods are **3 of 10** (7 misses). Every match is to a "possible water under cover" patch, and places nobody reported match about as often (3.8 of 10), so the flood count is a limit, not evidence: say "no better than chance", never "flood detected".

---

## Project Name

MonsoonLens

## High-Level Project Summary

MonsoonLens is an open web app that shows what the NASA-ISRO NISAR radar saw around Pune, India,
during the July 2026 monsoon. From 3 to 8 July, floods and landslides hit the district while NASA's
daily satellite images showed only cloud. NISAR's L-band radar sees through cloud, so we compared
its passes of 28 June and 10 July and mapped new water and likely landslide zones on the Western
Ghats slopes. We then checked the map against 18 reported events and show, on screen, what the radar
missed and why. It addresses the challenge with an interactive NISAR application for one real event,
with time steps, polarisations and physical drivers explained. It matters because cloud hides the
ground exactly when people need to see it.

## Link to Project Demo

https://youtu.be/gMXD7zp72yY (29.9 s, YouTube, unlisted: opens with no login)

The script is in `content/demo_script.md`. The guide allows a video of 30 seconds or less, or a
deck of at most 7 slides; anything longer is not eligible for Global Judging.

## Link to Final Project

- Live app: https://monsoonlens.streamlit.app
- Code and data: https://github.com/AyushSinghNegi/dancing-with-the-sars
- Deck, 7 slides: https://docs.google.com/presentation/d/11K2aK4sSJ06zdtdgaLwk6eT_DAQxki_FIBRZ0UvzuS4/edit?usp=sharing
- Appendix slides (data, method, checks, business, risks, sources): https://docs.google.com/presentation/d/1VKYELFHWinr-5r4WxW0iZY3I1ETU7Ex7iu2_WnkUFzU/edit?usp=sharing
- Business plan and global scale-up: https://docs.google.com/document/d/1DScRRLFX0MUlZeXZapZGP1U-N0dGmdZiMqDdRX-EudQ/edit?usp=sharing
- Technical and validation report: https://docs.google.com/document/d/1oxQSBnIQKd3hy4tiM3YgYng6VkXmFPsn9TbB6NuJqpI/edit?usp=sharing
- Field operations guide: https://docs.google.com/document/d/10gSMM83O0t-ox3mwgSeH6OlVahQl4a0r7GLOxuKpSfs/edit?usp=sharing
- Full walkthrough video (2 min 7 s, captions): https://youtu.be/GY2MDmud-Q4
- PDFs of the deck and reports: `deliverables/deck/` and `deliverables/reports/` in the repository

## Detailed Project Description

**What it does**

MonsoonLens has six pages, a one-minute guided tour, and works in English, Hindi, Marathi and
German, on a phone or a computer. The Overview gives the findings, the checks and a 3D view. The
Story walks through six steps: the rain, why radar, before and after, what changed, the weeks after,
and what radar could not see, with a before-and-after slider on the radar images. The Explore map
lets you switch layers and base maps, filter slide zones by confidence, click any zone or reported
event to see its details and source, and download the results. Check a place lets anyone pick one of
431 villages and towns and see what was found within 2, 5 or 10 km. The Field check list ranks every
likely slide zone with its radar evidence and what is nearby, as a printable list and KML for phones.
The Method page lists every NISAR file, every threshold, every check and every limit.

**What we found**

- 8.5 km² of new water where Pune's reservoirs and rivers rose between 28 June and 10 July.
- 0.36 km² of flood water, in 30 patches, still standing on 10 July on ground where no water was
  recorded between 1984 and 2021.
- 50 likely slide zones on steep slopes, 8 of them high confidence. They are leads to check, not
  confirmed landslides: 46 have no reported event within 2 km.
- Over the season, open water grew from 153 km² on 28 June to 191 km² on 14 October as the
  reservoirs filled (five NISAR passes on the same track and mode).

**How it works**

A Python pipeline reads only the Pune box from each NISAR file, on a 40 m grid.

- New water: pixels that are dark in HH on 10 July but not on 28 June, at least 3 dB darker, on flat
  ground, outside permanent water. The dark/bright threshold is learned for each date from known
  reservoirs and known dry land.
- Likely slide zones: slopes of 15° to 45° where radar coherence between the two passes is low and
  the brightness changed (HH up by 3 dB or more, or HV down by 2 dB or more).
- Rainfall (GPM IMERG) shows the cause; permanent water and slope come from public maps.
- The app reads only small precomputed files, so it loads quickly on a phone.

**How we checked it**

- Against reports: 18 events from news sources, each linked. Of 10 floods radar could observe, 3 had
  a "possible water" patch nearby, which is no better than chance: places nobody reported match about
  3.8 of 10 under the same rule. The 7 misses were all reported in or near towns, where radar echoes off
  walls can hide street flooding; that is a likely reason, not one we measured. Of 7 landslides we could locate, radar could observe 4; we matched 2, both to the
  same zone.
- Against a second orbit: NISAR track 106 (3 to 15 July) saw 12 of the zones and found 2 again,
  about 8 times what chance gives (p = 0.026).
- Against a second elevation map: re-run with NASA's NASADEM, 35 of the 50 zones are found again,
  7 of the 8 high-confidence ones. The two landslide matches do not hold in that run, and we say so.
- Against cloud: all 22 available NASA daily true-colour images of the area for 3 to 8 July are
  fully cloud-covered.

**What radar could not see**

Flooded streets between buildings; water that came and went between passes; slides smaller than a
40 m pixel or on gentle ground; the 2% of steep ground hidden from the radar; and the fact that
NISAR products are still provisional. These limits are on the Overview page, not in a footnote.

**Benefits and what we hope to achieve**

A district disaster office could see where the ground changed within days of a storm, without field
access, and know how far to trust the map. Road and rail operators on the ghat sections get a list
of slopes to inspect. The same code runs on any pair of NISAR passes for any district, so the next
step is to run it automatically for each new pass over the Western Ghats.

**Tools**

Python (h5py, rasterio, pyproj, shapely, SciPy, NumPy, pandas, earthaccess), Streamlit, folium,
Plotly, Pillow, pytest, GitHub, Streamlit Community Cloud. Code licence: MIT.

## Use of Super Intelligence (SI)

Yes.

- Most of the pipeline and app code, the tests, and the first drafts of the story text and its
  translations (Hindi, Marathi and German) were written with Claude (Anthropic), directed and
  reviewed by the team.
- Claude also helped build the deck, the reports, the figures and the demo videos; every figure is
  drawn by our code from the pipeline outputs, and the videos show the real app and NISAR layers.
- Claude was also used to check each reported event against its news source, to draft the style
  guide, the slide outline, the validation table text and this page, and to keep the list of open
  points (`plotholes.md`).
- ChatGPT (OpenAI) was used by one team member for data analysis.
- No measurement is SI-generated. Every number is computed by our code from the NISAR files listed
  below, or comes from a linked source.
- No image, video or audio is SI-generated. Map images and the demo videos are rendered by our code
  from the radar data and screenshots of the app; the videos' music and sound effects are synthesised
  by our code (`video/audio.py`, written with Claude), with no AI audio model and no samples.
- The idea and the choice of place and event were the team's own.
- The repository's README has a "Use of AI" section stating this.

## NASA Data

**NISAR (NASA-ISRO), L2 provisional products, via NASA's ASF DAAC**

Main pair, track 034:

- `NISAR_L2_PR_GCOV_024_034_D_079_4005_DHDH_A_20260628T134239_20260628T134314_P05023_N_F_J_001` (28 June 2026)
- `NISAR_L2_PR_GCOV_025_034_D_079_4005_DHDH_A_20260710T134239_20260710T134313_P05023_N_F_J_001` (10 July 2026)
- `NISAR_L2_PR_GUNW_024_034_D_079_025_4000_SH_20260628T134239_20260628T134314_20260710T134239_20260710T134313_P05023_N_F_J_001` (coherence, 28 June to 10 July)

Season timeline, track 034:

- `NISAR_L2_PR_GCOV_026_034_D_079_4005_DHDH_A_20260722T134238_20260722T134313_P05023_N_F_J_001` (22 July 2026)
- `NISAR_L2_PR_GCOV_028_034_D_079_4005_DHDH_A_20260815T134237_20260815T134311_P05023_N_F_J_001` (15 August 2026)
- `NISAR_L2_PR_GCOV_033_034_D_079_4005_DHDH_A_20261014T134237_20261014T134311_P05023_N_F_J_001` (14 October 2026)

Second-orbit check, track 106:

- `NISAR_L2_PR_GCOV_024_106_D_079_4005_DHDH_A_20260703T133420_20260703T133454_P05023_N_F_J_001` (3 July 2026)
- `NISAR_L2_PR_GCOV_025_106_D_079_4005_DHDH_A_20260715T133419_20260715T133454_P05023_N_F_J_001` (15 July 2026)
- `NISAR_L2_PR_GUNW_024_106_D_079_025_4000_SH_20260703T133420_20260703T133454_20260715T133419_20260715T133454_P05023_N_F_J_001` (coherence, 3 to 15 July)

**Other NASA data and services**

- GPM IMERG Late Run daily precipitation, GPM_3IMERGDL v07, area-averaged over the study box with
  NASA Giovanni (15 June to 31 October 2026).
- NASADEM_HGT v001 (NASA / USGS), doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001, for the
  elevation-map check.
- NASA Worldview Snapshots / GIBS true-colour imagery from Terra MODIS, Aqua MODIS, Suomi NPP VIIRS
  and NOAA-20 VIIRS, for the cloud check.
- NASA Common Metadata Repository (CMR), to find the NISAR scenes over Pune.
- NASA Earthdata Login, to access the data.

## Space Agency Partner Data and Other References

**Space agency partners**

- ISRO: NISAR is a joint NASA-ISRO mission.
- ESA: Copernicus GLO-30 Digital Elevation Model (ESA / Airbus), used for slope in the main run.

**Other data**

- JRC Global Surface Water v1.4, occurrence layer, 1984 to 2021 (Pekel et al., 2016, Nature
  540:418-422), for permanent water.
- Reported events: Punekar News, Free Press Journal, News Arena India, Deccan Chronicle, ANI via
  Newswav, PTI via Siasat. Each event links to its article in the app and in
  `data/reference/events.geojson`.
- OpenStreetMap (Nominatim) for place coordinates; base maps from Esri and OpenStreetMap
  contributors.

**Software and assets**

- Open-source Python libraries listed under Tools.
- IBM Plex Sans typeface (SIL Open Font License).
- All code in the repository was committed during the hackathon (first code commit 14 Nov 2026, 10:07 UTC).

## Before pressing "Submit for Judging"

- [ ] Demo link opens in a private window, with no login.
- [ ] Demo is 30 seconds or less (or 7 slides or fewer).
- [ ] Live app and repository links open in a private window.
- [ ] Every number above still matches `data/derived/metrics.json`.
- [x] The one remaining `[SQUARE BRACKET]` item is filled: the demo link.
- [ ] Nothing shows a person under 18.
- [ ] Ayush has given the final OK.
