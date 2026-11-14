# Plot holes: open points in the story, data and pitch

Everything found so far that is unverified, inconsistent or could be challenged by a judge.
Last updated 14 Nov 2026 (Urvashi on `urvashi/content`; Claude for Ayush on `claude/plotholes`).

**How to use this file**

- Read it before writing or changing story text, slides, the video, the README or the project page.
- When you fix a point, move it to "Resolved" with one line on what was done. Do not delete it.
- When you find a new one, add it with the next free number.
- Priority: **High** = a wrong or unsupported claim judges will see; **Medium** = weakens the
  result or is inconsistent; **Low** = polish.

## A. Claims without a source

| # | Priority | Open point | Next step |
|---|---|---|---|
| P01 | High | **Slide 1 figures, half checked.** Punekar News (7 July 2026, `?p=239349`, opened 15 Nov) says "22 landslides of varying intensity have been reported across Pune district", four people died in two days and two are missing. It does **not** give "6,000+ evacuated": it gives about 5,000 residents shifted by Pimpri Chinchwad, 300 evacuated by Pune city, 568 rescued, and "thousands" shifted overall. | Use "22 landslides, 4 dead, 2 missing" with the link; replace "6,000+ evacuated" with "thousands moved to safety (about 5,000 in Pimpri Chinchwad alone)". |
| P05 | Medium | **Other game-plan facts not yet opened:** "schools closed in seven talukas" and "500-600 mm of rain in a few days". | Open the source before either is used anywhere. |
| P06 | Medium | **"Flood water had two days to drain" is an inference.** We know the rain stopped; we have no measurement of how much water drained. On 8 July a source said dam discharge might be increased, so river flooding did not simply follow the rain. | Keep the wording modest; do not write "most flood water had drained" (the video still does, see P24). |

## B. Validation and data

| # | Priority | Open point | Next step |
|---|---|---|---|
| P07 | High | **E016 may not be a real hit.** It counts as detected on the Chakan town-centre point, 1,465 m from the detection with a 1,500 m tolerance. The source places the flooding near Waki Khurd village, which OpenStreetMap does not list. | Urvashi: find Waki Khurd on a map and move the point if needed. RSN: re-run validation. Floods would be 3 of 10 if it fails. |
| P08 | High | **The Patan landslide is a miss, but the demo script points at it.** E001 (the house buried at Patan, the best-known event of the storm) is scored "not detected". The game plan's script says "Here's the Patan slide". | Rewrite that demo line, or find the exact slide location and re-run validation. |
| P09 | High | **"22 reported landslides" versus 7 in our file.** The game plan promises a hit/miss table "against 22 reported landslides". We could locate 7, of which 4 were observable and 2 detected. | Say "the 7 we could locate" everywhere. |
| P11 | Medium | **Small samples.** Floods 4 of 10, landslides 2 of 4, second track 2 of 12 zones (p = 0.026). | Always give counts, never percentages or "accuracy". |
| P13 | Medium | **The second track covers little.** Track 106 sees 38% of the box; 38 of the 50 zones are not covered by it, and its water result is flagged unreliable in `metrics.json`. | Do not present it as confirming the whole map. |
| P15 | Medium | **The flood finding is small.** Of 8.9 km² new water, 8.5 km² is reservoirs and rivers rising; flooding on ground never wet before is 0.36 km² in 30 patches. A judge may set that against thousands evacuated. | Lead with the honest framing: radar came back two days late and cannot see between buildings. |
| P17 | Low | **E006 date and place are loose.** The source gives no event date (7 July is the report date) and says "Velhe village"; the point is Pabe village, about 4 km away. | Accept, or find a better source. |
| P18 | Low | **E018 is outside the storm window** (31 July). It is kept for context and not scored. | Decide whether to keep it. |
| P19 | Low | **Regenerating the context layers gives a slightly different slope file** on another machine (1 pixel differs by 1 degree). | Do not commit regenerated `data/crops/aux_*.tif`. |
| P40 | High | **Both landslide matches rest on one zone.** E002 and E003 are both matched to SZ030, 1.6 and 1.9 km away (inside the reports' 2 km location uncertainty). With NASADEM that zone falls in radar layover/shadow and the matches drop to 0 of 4. The Story and Method pages now say so. | Deck, video and project page: say "2 of 4, both to one zone, and not robust to the elevation map", or lead with the second-track result instead. |

## C. Rainfall

| # | Priority | Open point | Next step |
|---|---|---|---|
| P20 | Medium | **Late Run, not Final.** The Final Run did not cover 2026 on the download date, so values may shift when it is released. | Say "IMERG Late Run" wherever rainfall is credited. |
| P21 | Medium | **Days are UTC days.** "5 to 8 July" is in UTC; India is 5.5 hours ahead, so local-day totals differ. | Avoid exact day-by-day claims; "5 to 8 July" is safe. |
| P22 | Medium | **Box average versus station totals.** Our peak is about 180 mm/day averaged over the box; news reports quote single stations (for example 670 mm in 24 hours at Lonavla). | Never put the two side by side without saying which is which. |

## D. App, video and README out of step

| # | Priority | Open point | Next step |
|---|---|---|---|
| P24 | High | **The video is out of date.** `video/make_video.py` labels the rain chart "(NASA POWER)", credits "Rain: NASA POWER", scales the chart to 160 mm/day (IMERG peaks near 180) and says "Most flood water drained before the radar came back". The rendered 30-second video was made with the old rainfall. | Ayush: update the four lines and re-render. |
| P28 | Medium | **Legends do not name the NISAR file.** The design rule asks for unit, date and file ID on every layer; map legends show labels only, and the page footer shortens the file IDs. | Accept the Method page as the full list, or add IDs to the legends. |
| P30 | Low | **Pitch line is not on the landing page.** The title is "What NISAR radar saw in the 2026 Pune monsoon", not "NISAR sees what monsoon clouds hide". | Ayush: decide. |
| P31 | Low | **"What radar could not see" is 99 words**; the file's own limit is 90. | Trim. |
| P32 | Low | **Three pale map colours have low contrast** against the page, and one colour pair separates poorly for blue-yellow colour blindness. Outline, hatch and legend cover it. | Keep those encodings; see `content/style.md`. |

## E. Pitch and submission

| # | Priority | Open point | Next step |
|---|---|---|---|
| P33 | High | **Submission Guide not read yet.** Video length limit, required fields and the rule on declaring AI tools are unknown. | Urvashi: read it before U7. |
| P34 | Medium | **"Cameras saw only cloud" has limits.** Checked for NASA's four daily imagers only (not Sentinel-2 or Landsat). On 10 July, the day NISAR came back, they did see part of the ground. | Say "NASA's daily satellite images" and keep the claim to 3 to 8 July. |
| P35 | Medium | **Marathi text is unchecked.** `content/story.mr.md` and the Marathi strings in `app/lib/ui.py` were drafted by an assistant. | A Marathi speaker reads them before submission. |
| P37 | Low | **Slide links are placeholders.** `[LINK: live app]` and `[LINK: public repo]` in `content/slides.md`. | Ayush supplies them. |
| P38 | Low | **Cloud contact sheet is low resolution**, and NASA's acknowledgement wording has not been checked. | Remake it for the slide; add the credit. |
| P39 | Low | **Slide numbers are a snapshot** of `metrics.json` from 14 Nov 13:38 UTC. | Recheck every number after RSN's final run. |

## Resolved

| # | What it was | What was done |
|---|---|---|
| R01 | Story said the heaviest rain fell on 5 to 7 July. | IMERG shows 5 to 8 July; story, Marathi story and landing page corrected. |
| R02 | Story said Mutha dam releases stopped on 9 July; no source says so. | Claim removed from the story, the landing page and the E008 note. |
| R03 | "Ordinary satellite cameras saw only cloud" had no evidence. | Checked NASA daily imagery: all 22 available images for 3 to 8 July are fully cloud-covered. See `content/cloud_check.md` and P34 for the limits. |
| R04 | Rainfall was NASA POWER, not GPM IMERG. | Replaced; see `data/reference/SOURCES.md`. |
| R05 | "NISAR passes on 4 and 10 July" looked wrong. | It is right: track 113 passed on 4 July (`data/reference/candidate_scenes.csv`). |
| R06 | E008 and E016 text did not match their sources. | Notes and place name corrected (E016's location itself is still open, P07). |
| R07 | P25: README said every AI-assisted commit carries a `Co-Authored-By: Claude` line; the commits on `urvashi/content` were made with Claude and do not. | README "Use of AI" reworded: it now lists the content work as AI-assisted and says the commit history understates AI use. Recheck against the Submission Guide's AI rule (P33). |
| R08 | P04: "No water had been recorded since 1984" (JRC covers 1984 to 2021). | Now "between 1984 and 2021" in `app/lib/ui.py` (finding and map legend), `app/lib/maps.py`, `content/story.md` and `content/story.mr.md`. |
| R09 | P10: `validation.csv` out of step with `events.geojson`. | Validation re-run on the corrected events (PR #6); `content/validation.md` regenerated with `build_validation_table.py` (no change). |
| R10 | P12: "50 zones" shown without saying most are unverified. | The Overview finding now says they are leads to check and how many have no reported event within 2 km (number from `metrics.json`); the Method page limits say it too. |
| R11 | P14: water test misses known water. | Method page limits: "Water areas may be underestimates", with the share of permanent water seen dark (from `metrics.json`) and both causes: reservoirs drawn down before the monsoon (the share rises to 86% by 22 July as they fill, `timeline.csv`) and wind- or rain-roughened water. |
| R12 | P23: `python -m pipeline.rainfall` overwrote the IMERG file. | It now writes `data/reference/rainfall_power.csv` and never touches `rainfall.csv`. |
| R13 | P26: README credited NASA POWER and said the app ran on synthetic data. | README credits GPM IMERG Late Run and the NASA Worldview cloud check, links the live app and gives the current results. |
| R14 | P27: landing page had the old four-point panel. | The five-point text from `content/couldnt_see.md` is on the Overview (PR #7), every number computed from the pipeline output, with Marathi. |
| R15 | P36: nothing was viewed in the running app. | All four pages checked on screen in English and Marathi at desktop and phone width, with screenshots; zero errors (PR #6, #7). |
| R16 | P16: only two timeline dates. | Same-orbit, same-mode crops added for 22 July and 15 August (14 October pending); `timeline.csv` now also gives water inside the JRC extent and the share of permanent water seen dark per date. New Story step "The weeks after" and the Explore timeline chart use it. |
| R17 | P02: seven events rested on unopened Punekar News links. | All five links opened on 15 Nov and they support the events: ?p=239157 (E001: landslide hit a house in Patan village near the Bhaja Caves, Maval, early on 6 July), ?p=238883 (E007: Varandha Ghat landslide in Shirgaon limits, Bhor, 3 July), ?p=239453 (E009: flooding in Bhimnagar, Shivane, 8 July; Khadakwasla releasing 27,203 cusecs), ?p=239170 (E010, E012, E013: Chikhli Defence Colony flooded, Ravet barrage overflowed, water entered houses in Akurdi, 6 July), ?p=239208 (E014: "Rahatani bridge closed due to flooding", 6 July). E001's place text now follows its source ("near the Bhaja Caves"; the article does not mention Lohagad). |
| R18 | P03: "About 100 families shifted" (E010) had no opened source. | Punekar News ?p=239170: about 100 families from Chikhli Defence Colony and 10 from Keshavnagar were moved to municipal schools. |
| R19 | P29: slope data is not NASA's. | Main run still uses Copernicus GLO-30 (credited as ESA everywhere). NASA's NASADEM (from RSN's branch, PR #9) now runs as a second-map check (`pipeline/dem_check.py`): 35 of 50 zones found again, 7 of 8 high confidence; 15 drop out because NASADEM puts them over 45°, under 15° or in radar layover/shadow; NASADEM adds 33 of its own. On the Method page, in the zone popups and in `dem_check.json`. |
