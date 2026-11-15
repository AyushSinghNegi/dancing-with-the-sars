# Slide outline: 7 slides (U4, cut to the Submission Guide limit in U7)

The 2026 Project Submission Guide allows a deck of **at most 7 slides, including the title and
intro slides**; a longer deck is not eligible for Global Judging. The deck must be in English and
must show the team name, the names of the team members and the challenge. This outline has exactly
7 slides. Do not add an eighth: fold new material into an existing slide.

One message per slide, few words, real screenshots where marked `[IMG]`. Style: `content/style.md`.

**Before building the deck:** every number below was read from `data/derived/` (metrics.json
generated 2026-11-14T19:01Z, `timeline.csv`, `dem_check.json`, `validation.csv`) or from a source the
team opened. Recheck each number against the files after any new pipeline run. Open points are in
`plotholes.md`.

**Corrected (plotholes.md P07, P46):** the pipeline was re-run on 15 November with E016 at its real location. Floods are **3 of 10** (7 misses). Every match is to a "possible water under cover" patch, and places nobody reported match about as often (3.8 of 10), so the flood count is a limit, not evidence: say "no better than chance", never "flood detected".

What changed from the 8-slide version: a title slide was added (the guide requires team and
challenge), "Why radar" and "What we built" became one slide, "Demo" now carries the findings, and
"Business model" and "Roadmap and team" became one slide.

---

## 1. Title

**Headline:** MonsoonLens: NISAR sees what monsoon clouds hide

- NASA Space Apps Challenge 2026, challenge "Dancing with the SARs"
- Team iGenfinity, GDG Ahlen (virtual)
- Ayush Singh Negi, Urvashi Negi, Rajendra Singh Negi

`[IMG]` Before/after radar swipe, full width, behind the title.

| Fact | Source |
|---|---|
| Team name, local event, challenge | `README.md` |

## 2. Problem

**Headline:** Floods and landslides, hidden under monsoon cloud

- Early July 2026: days of extreme rain over Pune and the Western Ghats.
- 22 landslides across Pune district; 4 people dead and 2 missing.
- About 5,000 people moved to safety in Pimpri Chinchwad alone.
- From 3 to 8 July, NASA's daily satellite images of the area showed only cloud.

`[IMG]` Rain chart (`content/img/rain_chart.png`) beside the cloud contact sheet.

| Fact | Source |
|---|---|
| Heaviest rain 5 to 8 July, peak about 180 mm/day on 5 July (box average) | `data/reference/rainfall.csv` (GPM IMERG Late Run) |
| 22 landslides, 4 dead, 2 missing; about 5,000 moved in Pimpri Chinchwad | Punekar News, 7 July 2026 (`?p=239349`), opened by the team; `plotholes.md` R22 |
| Only cloud on 3 to 8 July: all 22 available images | `content/cloud_check.md`, `data/reference/cloud_check.json` |

## 3. Why radar, and what we built

**Headline:** Radar sees through cloud. We mapped one storm.

- NISAR's L-band radar sends its own pulses, 24 cm long, through cloud and rain.
- Smooth water looks dark. Rough ground, trees and buildings look bright.
- Two passes, 28 June and 10 July 2026, bracket the storm.
- MonsoonLens: a story for the public, an explore map for experts, a method page with every file ID.

`[IMG]` Before/after radar swipe (Story step 3).

| Fact | Source |
|---|---|
| L-band SAR, 24 cm wavelength | NASA Science, NISAR mission page (science.nasa.gov/mission/nisar) |
| Pass dates 28 Jun and 10 Jul 2026, track 034 | `data/derived/timeline.csv`; NISAR file IDs in `content/project_page.md` |
| Data: NISAR GCOV and GUNW; GPM IMERG; JRC Global Surface Water v1.4; Copernicus GLO-30 DEM; NASADEM (check only) | `CONTEXT.md`, `data/reference/SOURCES.md` |

## 4. Demo: what the radar found

**Headline:** New water and 50 likely slide zones

- 8.5 km² of new water where reservoirs and rivers rose.
- 0.36 km² of flood water still standing on 10 July, on ground never recorded wet between 1984 and 2021.
- 50 likely slide zones on steep slopes, 8 of them high confidence: leads to check, not confirmed landslides.
- Through the season, open water grew from 153 km² (28 June) to 191 km² (14 October).
- Try it: https://monsoonlens.streamlit.app

`[IMG]` Explore map with flood, slide-zone and reported-event layers on.

| Fact | Source |
|---|---|
| Rise 8.523 km²; flood 0.365 km² in 30 patches | `metrics.json` → `water` |
| 50 zones, 8 high confidence | `metrics.json` → `slides` |
| 46 of 50 zones have no reported event within 2 km | `metrics.json` → `validation.unreported_slide_zones` |
| Open water 153.0, 175.84, 183.19, 187.4, 190.99 km² on five passes | `data/derived/timeline.csv` |
| Live app address | `README.md` |

## 5. Validation

**Headline:** We publish our hits and our misses

- 18 reported events, each with a linked source.
- Floods: 3 of 10 that radar could observe had a possible-water patch nearby, no better than chance (random places: 3.8 of 10). All 7 misses were reported in or near towns, where buildings can hide flooded streets from radar: a likely reason, not a measured one.
- A second NISAR orbit (3 to 15 July) found 2 of 12 zones again: about 8 times chance.
- With NASA's NASADEM elevation map, 35 of 50 zones are found again, 7 of the 8 high-confidence ones.
- Landslides: 2 of the 4 radar could observe, both matched to one zone; that match does not hold with NASADEM.

`[IMG]` Validation table (event, date, detected, reason if missed).

| Fact | Source |
|---|---|
| 18 events; floods 11 reported, 10 observable, 4 hits; landslides 7 reported, 4 observable, 2 hits | `validation_summary.json` |
| 7 flood misses, all reported in or near towns | `validation.csv`, `place` column. The `reason` column ("dense buildings") is a radar-brightness test, not a map of buildings (plotholes.md P53) |
| 2 landslide misses: ground near the report gentler than the 15° slide search (one is Patan) | `validation.csv` |
| Second orbit: 12 zones scored, 16.7% confirmed, lift 7.9, p = 0.026 | `metrics.json` → `crosstrack` |
| NASADEM check: 35 of 50 found, 7 of 8 high; landslide matches 2 → 0 of 4 | `data/derived/dem_check.json` |

Keep in mind for this slide:

- Lead with floods and the second orbit; the landslide match is the weakest result (`plotholes.md` R23).
- E016 (Pune-Nashik highway) counts as a flood hit on a town-centre point; its true location is unconfirmed (P07). Floods would be 3 of 10 without it.
- Small samples: say "3 of 10" and "2 of 4", never percentages (P11).
- We located 7 of the 22 reported landslides; do not say we checked all 22 (P09).

## 6. Impact, and what radar could not see

**Headline:** Changed ground, found without field access

- NISAR came back on 10 July, two days after the heaviest rain.
- Who it helps: the district disaster office (where to send teams), road and rail operators on
  ghat sections, residents and trekkers.
- What radar could not see: flooded streets between buildings, water that came and went between
  passes, slides smaller than a 40 m pixel.
- We show these blind spots on the first page, so nobody over-trusts the map.

`[IMG]` "What radar could not see" panel from the Overview page.

| Fact | Source |
|---|---|
| Heavy rain ended 8 July; pass on 10 July | `rainfall.csv`; `timeline.csv` |
| Limits | `content/couldnt_see.md` |
| Users and needs | game plan, "Who it helps" |

## 7. What comes next

**Headline:** From one storm to every monsoon pass

- Next: run automatically on each new NISAR pass over the Western Ghats.
- Later: ISRO's S-band data, alerts for subscribed users, more regions.
- Free and open core. Paid services for those who must act after a storm: disaster authorities,
  road and rail operators, insurers.
- Free NASA data and code that runs on a laptop keep running costs low.
- Code (MIT licence): https://github.com/AyushSinghNegi/dancing-with-the-sars

`[IMG]` Season timeline chart (Story step 5), small.

| Fact | Source |
|---|---|
| Roadmap phases | game plan, "Scalability in three phases" |
| Customers and offers | game plan, "Business model and sustainability" |
| Licence, repository | `LICENSE`, `README.md` |

No revenue numbers: we have none we can back.
