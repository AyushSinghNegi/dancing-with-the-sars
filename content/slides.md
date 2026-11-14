# Slide outline: 8 slides (U4, built in U7)

One message per slide, few words, real screenshots where marked `[IMG]`. Style: `content/style.md`.

**Before building the deck:** every number below was read from `data/derived/metrics.json`
(generated 2026-11-14T13:38Z) and `data/derived/validation.csv`, or from a source that was opened.
RSN's final run (R9) may change them, so recheck each number against the files on Sunday.
Lines marked `[VERIFY]` come from the game plan and their source has not been opened yet:
open the link before the line goes on a slide, or drop the line.

---

## 1. Problem

**Headline:** Floods and landslides, hidden under monsoon cloud

- Early July 2026: days of extreme rain over Pune and the Western Ghats.
- 6 July: a landslide buried a house in Patan village, Maval; landslides blocked the
  Mumbai-Pune railway and expressway.
- Ordinary satellite cameras saw only cloud.

`[IMG]` Rainfall chart from the Story page (step 1).

| Fact | Source |
|---|---|
| Heaviest rain 5 to 8 July, peak about 180 mm/day on 5 July (box average) | `data/reference/rainfall.csv` (GPM IMERG Late Run) |
| House buried at Patan village, Maval, 6 July; two killed | Siasat / PTI (E001, E017 source) |
| Railway landslide between Khandala and Monkey Hill; expressway Missing Link landslide at Tunnel 2 exit, 6 July | News Arena India (E003); Free Press Journal (E002) |
| 1,880 residents moved to shelters in Pimpri-Chinchwad, 6 July | Free Press Journal (E015 source) |
| `[VERIFY]` 22 landslides, 4 dead and 2 missing in Pune district by 7 July | Punekar News (game plan); site blocked the check |
| `[VERIFY]` 6,000+ people evacuated | game plan; source not opened |

## 2. Why radar

**Headline:** NISAR sees what monsoon clouds hide

- NISAR's L-band radar sends its own pulses, 24 cm long, through cloud and rain.
- Smooth water looks dark. Rough ground, trees and buildings look bright.
- Passes on 28 June and 10 July 2026 bracket the storm.

`[IMG]` Before/after radar swipe (Story step 3).

| Fact | Source |
|---|---|
| L-band SAR, 24 cm wavelength | NASA Science, NISAR mission page (science.nasa.gov/mission/nisar) |
| Pass dates 28 Jun and 10 Jul 2026, track 034 | `data/derived/timeline.csv`, NISAR file IDs in `content/style.md` |

## 3. What we built

**Headline:** MonsoonLens: one storm, mapped and checked

- A 5-step story for the public, an explore map for experts, a method page with every file ID.
- New water: 8.9 km² (8.5 km² reservoirs and rivers rising, 0.36 km² flooding on ground never wet before).
- 50 likely slide zones on steep slopes, 8 of them high confidence.
- Open code, free data, runs on a laptop.

`[IMG]` Explore map with flood, slide-zone and reported-event layers on.

| Fact | Source |
|---|---|
| New water 8.888 km²; rise 8.523 km²; flood 0.365 km² in 30 patches | `metrics.json` → `water` |
| 50 zones, 8 high, 15 medium | `metrics.json` → `slides` |
| Data: NISAR GCOV and GUNW; GPM IMERG; JRC Global Surface Water v1.4; Copernicus GLO-30 DEM | `CONTEXT.md`, `data/reference/SOURCES.md` |

Note for the project page: the game plan lists NASADEM for slope, but the pipeline uses the
Copernicus GLO-30 DEM. List what was actually used.

## 4. Demo

**Headline:** See it in one minute

- Live app: `[LINK: live app, from Ayush]`
- Path to show: rain chart → swipe → slide zones → what radar could not see.

`[IMG]` Full-width screenshot of the Story page, step 4.

The 3-minute script is written in U7 from the game plan's table, with the real counts from slide 5.

## 5. Validation

**Headline:** We publish our hits and our misses

- 18 reported events, each with a linked source.
- Floods: 4 of 10 that radar could observe had a detection nearby.
- Landslides: 2 of 4.
- A second NISAR track (106, 3 to 15 July) found 2 of 12 zones again: about 8 times chance.

`[IMG]` Validation table (event, date, detected, reason if missed).

| Fact | Source |
|---|---|
| 18 events; floods 11 reported, 10 observable, 4 hits; landslides 7 reported, 4 observable, 2 hits | `validation_summary.json` |
| 6 flood misses: dense buildings hide street flooding | `validation.csv`, `reason` column |
| 2 landslide misses: ground near the report gentler than the 15° slide search | `validation.csv` |
| 2 not scored (location too vague), 1 outside the radar box, 1 after the radar pair | `validation.csv` |
| Second track: 12 zones scored, 16.7% confirmed, lift 7.9, p = 0.026 | `metrics.json` → `crosstrack` |

Open points before this slide is final:

- 7 events cite Punekar News, which blocked our link check; open them by hand.
- E016 (Pune-Nashik highway) counts as a hit on a town-centre point; the source places the
  flooding near Waki Khurd. Confirm the location or say so on the slide.
- Small samples: say "4 of 10" and "2 of 4", not percentages.

## 6. Impact

**Headline:** Changed ground, found without field access

- NISAR came back on 10 July, two days after the heaviest rain.
- Who it helps: district disaster office (where to send teams), road and rail operators on
  ghat sections, residents and trekkers.
- We show the blind spots, so nobody over-trusts the map.
- The same method runs on any NISAR pair, for any district.

`[IMG]` "What radar could not see" panel.

| Fact | Source |
|---|---|
| Heavy rain ended 8 July; pass on 10 July | `rainfall.csv`; `timeline.csv` |
| Users and needs | game plan, "Who it helps" |

## 7. Business model

**Headline:** Free and open core, paid services on top

| Customer | Offer | How it pays |
|---|---|---|
| State and district disaster authorities | Dashboard refreshed after every NISAR pass | Pilot grant or CSR funding, then annual contract |
| Road, rail and pipeline operators in the Ghats | Corridor watch report per route | Subscription per route |
| Insurers and rural lenders | Flood-extent data per area and event | Pay per use |
| NGOs, schools, researchers | Free app, open data and code | Free |

- NISAR data is free and the pipeline runs on a laptop, so running costs stay low.
- No revenue numbers: we have none we can back.

Source: game plan, "Business model and sustainability".

## 8. Roadmap and team

**Headline:** From one storm to every monsoon pass

- Now: one district, one storm, precomputed layers.
- Next three months: run automatically on each new NISAR pass over the Western Ghats.
- Later: ISRO's S-band data, alerts for subscribed users, more regions.

Team iGenfinity:

- Ayush: app, integration, team lead
- RSN: data and science
- Urvashi: validation, story, pitch

Code: MIT licence, `[LINK: public repo]`

Source: game plan, "Scalability in three phases" and "Team roles"; `LICENSE`; `README.md`.
