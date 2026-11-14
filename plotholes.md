# Plot holes: open points in the story, data and pitch

Everything found so far that is unverified, inconsistent or could be challenged by a judge.
Last updated 14 Nov 2026, on branch `urvashi/content`.

**How to use this file**

- Read it before writing or changing story text, slides, the video, the README or the project page.
- When you fix a point, move it to "Resolved" with one line on what was done. Do not delete it.
- When you find a new one, add it with the next free number.
- Priority: **High** = a wrong or unsupported claim judges will see; **Medium** = weakens the
  result or is inconsistent; **Low** = polish.

## A. Claims without a source

| # | Priority | Open point | Next step |
|---|---|---|---|
| P01 | High | **Two unverified figures on slide 1.** "22 landslides, 4 dead and 2 missing" and "6,000+ evacuated" come from the game plan. Their sources could not be opened (Punekar News blocks the browser used for the check). They are marked `[VERIFY]` in `content/slides.md`. | Urvashi: open the links by hand, or drop the lines. |
| P02 | High | **Seven events rest on unchecked Punekar News links:** E001, E007, E009, E010, E012, E013, E014 (five links). Other opened articles partly back E001, E009 and E010; nothing opened backs E007, E012, E013 or E014. | Urvashi: open the five links; fix or remove any event the article does not support. |
| P03 | Medium | **E010 note says "About 100 families shifted".** No opened source says this. | Urvashi: confirm in the Punekar News article or remove the phrase. |
| P04 | Medium | **"No water had been recorded since 1984".** The JRC record used covers 1984 to 2021, so "between 1984 and 2021" is exact. The phrase is in `content/story.md`, `content/story.mr.md` and `app/lib/ui.py`. | Urvashi and Ayush: change all three together. |
| P05 | Medium | **Other game-plan facts not yet opened:** "schools closed in seven talukas" and "500-600 mm of rain in a few days". | Open the source before either is used anywhere. |
| P06 | Medium | **"Flood water had two days to drain" is an inference.** We know the rain stopped; we have no measurement of how much water drained. On 8 July a source said dam discharge might be increased, so river flooding did not simply follow the rain. | Keep the wording modest; do not write "most flood water had drained" (the video still does, see P24). |

## B. Validation and data

| # | Priority | Open point | Next step |
|---|---|---|---|
| P07 | High | **E016 may not be a real hit.** It counts as detected on the Chakan town-centre point, 1,465 m from the detection with a 1,500 m tolerance. The source places the flooding near Waki Khurd village, which OpenStreetMap does not list. | Urvashi: find Waki Khurd on a map and move the point if needed. RSN: re-run validation. Floods would be 3 of 10 if it fails. |
| P08 | High | **The Patan landslide is a miss, but the demo script points at it.** E001 (the house buried at Patan, the best-known event of the storm) is scored "not detected". The game plan's script says "Here's the Patan slide". | Rewrite that demo line, or find the exact slide location and re-run validation. |
| P09 | High | **"22 reported landslides" versus 7 in our file.** The game plan promises a hit/miss table "against 22 reported landslides". We could locate 7, of which 4 were observable and 2 detected. | Say "the 7 we could locate" everywhere. |
| P10 | Medium | **`validation.csv` is out of step with `events.geojson`.** It still has the old E016 place name. `pipeline.validate` did not run standalone on Urvashi's machine (the water layers were missing). | RSN: re-run validation, then run `python content/build_validation_table.py`. |
| P11 | Medium | **Small samples.** Floods 4 of 10, landslides 2 of 4, second track 2 of 12 zones (p = 0.026). | Always give counts, never percentages or "accuracy". |
| P12 | Medium | **46 of the 50 likely slide zones have no reported event within 2 km.** They are unverified leads, not confirmed slides. | Say so wherever "50 zones" appears. |
| P13 | Medium | **The second track covers little.** Track 106 sees 38% of the box; 38 of the 50 zones are not covered by it, and its water result is flagged unreliable in `metrics.json`. | Do not present it as confirming the whole map. |
| P14 | Medium | **Our water test misses known water.** Only 70% of permanent water looks dark enough to pass the threshold (`water.permanent_water_seen_dark`). New-water areas are therefore likely underestimates. | State it on the Method page or in the limits. |
| P15 | Medium | **The flood finding is small.** Of 8.9 km² new water, 8.5 km² is reservoirs and rivers rising; flooding on ground never wet before is 0.36 km² in 30 patches. A judge may set that against thousands evacuated. | Lead with the honest framing: radar came back two days late and cannot see between buildings. |
| P16 | Medium | **Only two timeline dates.** The game plan promises a five-date monsoon timeline; `timeline.csv` has 28 June and 10 July only. | RSN: add the dates, or drop "five dates" from slides and the checklist. |
| P17 | Low | **E006 date and place are loose.** The source gives no event date (7 July is the report date) and says "Velhe village"; the point is Pabe village, about 4 km away. | Accept, or find a better source. |
| P18 | Low | **E018 is outside the storm window** (31 July). It is kept for context and not scored. | Decide whether to keep it. |
| P19 | Low | **Regenerating the context layers gives a slightly different slope file** on another machine (1 pixel differs by 1 degree). | Do not commit regenerated `data/crops/aux_*.tif`. |

## C. Rainfall

| # | Priority | Open point | Next step |
|---|---|---|---|
| P20 | Medium | **Late Run, not Final.** The Final Run did not cover 2026 on the download date, so values may shift when it is released. | Say "IMERG Late Run" wherever rainfall is credited. |
| P21 | Medium | **Days are UTC days.** "5 to 8 July" is in UTC; India is 5.5 hours ahead, so local-day totals differ. | Avoid exact day-by-day claims; "5 to 8 July" is safe. |
| P22 | Medium | **Box average versus station totals.** Our peak is about 180 mm/day averaged over the box; news reports quote single stations (for example 670 mm in 24 hours at Lonavla). | Never put the two side by side without saying which is which. |
| P23 | Medium | **`python -m pipeline.rainfall` overwrites the IMERG file** with NASA POWER data. | Do not run it; consider removing or guarding it. |

## D. App, video and README out of step

| # | Priority | Open point | Next step |
|---|---|---|---|
| P24 | High | **The video is out of date.** `video/make_video.py` labels the rain chart "(NASA POWER)", credits "Rain: NASA POWER", scales the chart to 160 mm/day (IMERG peaks near 180) and says "Most flood water drained before the radar came back". The rendered 30-second video was made with the old rainfall. | Ayush: update the four lines and re-render. |
| P25 | High | **README says every AI-assisted commit carries a `Co-Authored-By: Claude` line.** The commits on `urvashi/content` were made with Claude and deliberately do not carry it. | Urvashi and Ayush: reword the README sentence so the AI disclosure stays true. |
| P26 | Medium | **README credits and status are stale.** It credits "NASA POWER daily precipitation" and says the app runs on synthetic data until real crops are in. | Update to GPM IMERG and the current status. |
| P27 | Medium | **Landing page panel is the old version.** `app/home.py` has a four-point "couldn't see" panel; the new five-point text is in `content/couldnt_see.md`. | Ayush: paste it in at U6. |
| P28 | Medium | **Legends do not name the NISAR file.** The design rule asks for unit, date and file ID on every layer; map legends show labels only, and the page footer shortens the file IDs. | Accept the Method page as the full list, or add IDs to the legends. |
| P29 | Medium | **Slope data is not NASA's.** The game plan lists NASADEM; the pipeline uses the Copernicus GLO-30 DEM (ESA). | Name Copernicus on the project page; do not list it under NASA data. |
| P30 | Low | **Pitch line is not on the landing page.** The title is "What NISAR radar saw in the 2026 Pune monsoon", not "NISAR sees what monsoon clouds hide". | Ayush: decide. |
| P31 | Low | **"What radar could not see" is 99 words**; the file's own limit is 90. | Trim. |
| P32 | Low | **Three pale map colours have low contrast** against the page, and one colour pair separates poorly for blue-yellow colour blindness. Outline, hatch and legend cover it. | Keep those encodings; see `content/style.md`. |

## E. Pitch and submission

| # | Priority | Open point | Next step |
|---|---|---|---|
| P33 | High | **Submission Guide not read yet.** Video length limit, required fields and the rule on declaring AI tools are unknown. | Urvashi: read it before U7. |
| P34 | Medium | **"Cameras saw only cloud" has limits.** Checked for NASA's four daily imagers only (not Sentinel-2 or Landsat). On 10 July, the day NISAR came back, they did see part of the ground. | Say "NASA's daily satellite images" and keep the claim to 3 to 8 July. |
| P35 | Medium | **Marathi text is unchecked.** `content/story.mr.md` and the Marathi strings in `app/lib/ui.py` were drafted by an assistant. | A Marathi speaker reads them before submission. |
| P36 | Medium | **Nothing was viewed in the running app.** The story and landing text changes were checked by tests only, not on screen or on a phone. | Check at U6 with Ayush. |
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
