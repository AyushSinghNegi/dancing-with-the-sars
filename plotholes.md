# Plot holes: open points in the story, data and pitch

Everything found so far that is unverified, inconsistent or could be challenged by a judge.
Last updated 15 Nov 2026 (Urvashi on `urvashi/nearby-baseline`; earlier: Urvashi on `urvashi/content`,
Claude for Ayush on `claude/plotholes`).

**How to use this file**

- Read it before writing or changing story text, slides, the video, the README or the project page.
- When you fix a point, move it to "Resolved" with one line on what was done. Do not delete it.
- When you find a new one, add it with the next free number.
- Priority: **High** = a wrong or unsupported claim judges will see; **Medium** = weakens the
  result or is inconsistent; **Low** = polish.

## A. Claims without a source

| # | Priority | Open point | Next step |
|---|---|---|---|
| P05 | Medium | **Other game-plan facts not yet opened:** "schools closed in seven talukas" and "500-600 mm of rain in a few days". | Open the source before either is used anywhere. |
| P06 | Medium | **"Flood water had two days to drain" is an inference.** We know the rain stopped; we have no measurement of how much water drained. On 8 July a source said dam discharge might be increased, so river flooding did not simply follow the rain. | Keep the wording modest; do not write "most flood water had drained" (the video still does, see P24). |

## B. Validation and data

| # | Priority | Open point | Next step |
|---|---|---|---|
| P07 | Done | **E016 moved; validation re-run on 15 Nov: E016 is a miss, floods 3 of 10 (7 misses).** Urvashi located Waki Kh. on Google Maps (18.7824 N, 73.8725 E), about 2.5 km north-north-east of Chakan town centre, and the E016 point in `events.geojson` has been moved there. The old "hit" was a patch 1,465 m south-east of Chakan, on the opposite side. From the published map layers, the nearest detection to the new point is 2,400 m away, beyond the 1,500 m tolerance (the same calculation reproduces the pipeline's 1,465 m and 126 m exactly). `validation.csv`, `metrics.json`, `content/validation.md` and the app still show the old result. | RSN or Ayush: re-run the pipeline, then `python content/build_validation_table.py`. If E016 is a miss, change "4 of 10" to "3 of 10" and "6 misses" to "7" in the app text, video, deck, `content/slides.md`, `content/demo_script.md` and `content/project_page.md`. Do not publish "4 of 10" before the re-run. |
| P46 | High | **The flood matches are no better than chance, and every one is to "possible water under cover".** The validation rule counts a reported flood as detected if new water *or* a "possible water under cover" patch is within range. For all 10 observable floods the nearest mapped new water is 7 to 16 km away; every match is to a "possible water" patch, which the app says is shown but never counted as flood. The chance level is now computed (`pipeline/flood_baseline.py`, `data/derived/flood_baseline.json`): with E016 at its corrected place 3 of 10 reports match, while the same rule gives 3.8 of 10 on random flat ground and 3.4 of 10 at random OpenStreetMap settlements (probability of 3 or more by chance: 0.82 and 0.73). The old 4 of 10 would not beat chance either. | Do not present the flood count as evidence that the map finds reported floods. Wherever it is quoted, say "matched to a possible-water patch, no more often than chance". The Method page and the checks band now say so; the video, deck and content files do not yet (P47). |
| P47 | High | **The pitch still leads with the flood count.** After R23 the video, the deck, `content/slides.md`, `content/demo_script.md` and `content/project_page.md` lead the validation with "floods 4 of 10". That count is at chance level (P46), so leading with it invites the question it cannot answer. | Urvashi and Ayush: lead with what holds up (reservoir and river rise of 8.5 km², the second-orbit check, the NASADEM check) and state the flood result as a limit: radar came back two days late, could not see between buildings, and the matches are no more than chance. |
| P48 | Medium | **No chance level for the landslide matches.** Landslides are 2 of 4, both matched to one zone (SZ030) 1.6 and 1.9 km away, with a 2 km tolerance and 50 zones on the map. The same question applies as for floods (P46) and has not been computed. | RSN or Urvashi: run the same calculation with `slide_zones.tif` and steep ground as the reference set before the landslide count is quoted as support. |
| P49 | Medium | **"What is nearby" has limits.** `pipeline/nearby.py` lists roads and railway lines within 1 km and settlements within 2 km of each zone (19, 1 and 20 of 50 zones; 19 have none). Distances are straight lines from the zone's edge, not paths downhill; OpenStreetMap leaves out small roads, tracks and hamlets, and many rural roads have no name. The printable field list, KML and field-list CSV do not carry these columns yet (they are in `nearby.csv`). | Say "near", never "at risk" or "affected". RSN or Ayush: add the columns to `pipeline/evidence.py`'s field list on the next full run if wanted. |
| P51 | Closed | **The pass-by-pass view showed pictures, not findings.** It was removed from "Check a place" (judge pass, 15 Nov): only the 28 Jun to 10 Jul pair is analysed for change, and later-date differences mix in crops and forest greening. `pipeline/pass_images.py` still runs but the app no longer shows its images. | None. |
| P50 | Medium | **`run_all.py` was changed but not run end to end.** The new steps (flood chance level, what is nearby, pass images) were run on their own on Urvashi's PC, which cannot run the full pipeline. In `run_all` they sit after render inside a try/except, so a failure prints "skipped" and cannot stop the run. | RSN or Ayush: on the next full run, check that `flood_baseline.json`, `nearby.json` and `pass_images.json` are rewritten and that "skipped" is not printed. |
| P09 | High | **"22 reported landslides" versus 7 in our file.** The game plan promises a hit/miss table "against 22 reported landslides". We could locate 7, of which 4 were observable and 2 detected. | Say "the 7 we could locate" everywhere. |
| P11 | Medium | **Small samples.** Floods 3 of 10, landslides 2 of 4, second track 2 of 12 zones (p = 0.026). | Always give counts, never percentages or "accuracy". |
| P13 | Medium | **The second track covers little.** Track 106 sees 38% of the box; 38 of the 50 zones are not covered by it, and its water result is flagged unreliable in `metrics.json`. | Do not present it as confirming the whole map. |
| P15 | Medium | **The flood finding is small.** Of 8.9 km² new water, 8.5 km² is reservoirs and rivers rising; flooding on ground never wet before is 0.36 km² in 30 patches. A judge may set that against thousands evacuated. | Lead with the honest framing: radar came back two days late and cannot see between buildings. |
| P17 | Low | **E006 date and place are loose.** The source gives no event date (7 July is the report date) and says "Velhe village"; the point is Pabe village, about 4 km away. | Accept, or find a better source. |
| P18 | Low | **E018 is outside the storm window** (31 July). It is kept for context and not scored. | Decide whether to keep it. |
| P19 | Low | **Regenerating the context layers gives a slightly different slope file** on another machine (1 pixel differs by 1 degree). | Do not commit regenerated `data/crops/aux_*.tif`. |

## C. Rainfall

| # | Priority | Open point | Next step |
|---|---|---|---|
| P20 | Medium | **Late Run, not Final.** The Final Run did not cover 2026 on the download date, so values may shift when it is released. | Say "IMERG Late Run" wherever rainfall is credited. |
| P21 | Medium | **Days are UTC days.** "5 to 8 July" is in UTC; India is 5.5 hours ahead, so local-day totals differ. | Avoid exact day-by-day claims; "5 to 8 July" is safe. |
| P22 | Medium | **Box average versus station totals.** Our peak is about 180 mm/day averaged over the box; news reports quote single stations (for example 670 mm in 24 hours at Lonavla). | Never put the two side by side without saying which is which. |
| P52 | Low | **Rain between passes is a description, not a link.** The season map on Explore now shows, for each pass, the IMERG rain since the previous pass next to the change in open water (871 mm and +36 km², 208 mm and +10, 459 mm and +7, 231 mm and +3). Four intervals of different length; reservoirs are also filled and released by dam operators. Rain is the box average in UTC days from the day after one pass to the day of the next (P20 to P22 apply). | Say "the reservoirs rose most after the July storm and little after", never that rain "explains" or "predicts" the water. |

## D. App, video and README out of step

| # | Priority | Open point | Next step |
|---|---|---|---|
| P28 | Medium | **Legends do not name the NISAR file.** The design rule asks for unit, date and file ID on every layer; map legends show labels only, and the page footer shortens the file IDs. | Accept the Method page as the full list, or add IDs to the legends. |
| P30 | Low | **Pitch line is not on the landing page.** The title is "What NISAR Radar Saw in the 2026 Pune Monsoon", not "NISAR sees what monsoon clouds hide". | Ayush: decide. |
| P31 | Low | **"What radar could not see" is 99 words**; the file's own limit is 90. | Trim. |
| P32 | Low | **Three pale map colours have low contrast** against the page, and one colour pair separates poorly for blue-yellow colour blindness. Outline, hatch and legend cover it. | Keep those encodings; see `content/style.md`. |

## E. Pitch and submission

| # | Priority | Open point | Next step |
|---|---|---|---|
| P41 | High | **The built deck must also have 7 slides or fewer.** The 2026 Submission Guide allows a video of 30 seconds or less, or a deck of at most 7 slides including title and intro; going over makes the project ineligible for Global Judging. `content/slides.md` is now a 7-slide outline, but the deck built from the earlier 8-slide outline (in the team's Submission folder) has not been checked against it. The 3-minute script is not a submission format. | Ayush: count the slides in the built deck; if it is linked as the demo it must be 7 or fewer. Ask the Local Lead whether GDG Ahlen has a live pitch. |
| P42 | High | **SI (AI) labelling rules.** The guide requires SI-generated images and videos to carry a visible watermark, and SI-generated code and data to be acknowledged in descriptive text and metadata. Our demo video is drawn by code from radar data, but that code was written with an AI assistant. | Ayush: decide whether the video needs a visible note. The README "Use of AI" section covers the code; check it still matches `content/project_page.md`. |
| P43 | Medium | **English-only rule.** The guide says the project page and any linked materials must be in English. The live app has a Marathi option. | Keep English as the default language of the app, and say on the project page that Marathi is an extra. |
| P44 | Medium | **The project page still needs the demo link.** `content/project_page.md` has one `[SQUARE BRACKET]` item left: the public link to the 30-second video. | Urvashi: add it once the video is uploaded. |
| P45 | Low | **Deadline is in the Local Event's time zone:** Sunday 15 Nov, 11:59 p.m. for GDG Ahlen. Local judging may have its own times. | Confirm with the Local Lead; the 10 PM IST target is earlier and safe. |
| P35 | Medium | **Marathi text is unchecked.** `content/story.mr.md` and the Marathi strings in `app/lib/ui.py` were drafted by an assistant. So were the new ones of 15 Nov: the "What is nearby" lines in `app/lib/evidence.py`, the nearby sentence and column names in `app/views/5_Field.py`, and the chance sentence in `app/lib/checks.py` (German for the same strings is in `app/lib/i18n_de.py`). | A Marathi speaker reads them before submission. |
| P38 | Low | **Cloud contact sheet is low resolution**, and NASA's acknowledgement wording has not been checked. | Remake it for the slide; add the credit. |
| P39 | Low | **Slide and script numbers are a snapshot** of `metrics.json` from 14 Nov 19:01 UTC (`content/slides.md`, `content/demo_script.md`, `content/project_page.md`). | Recheck every number after any new pipeline run. |

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
| R20 | P24: the video was out of date. | Re-rendered (`video/make_video.py`): rain chart is GPM IMERG Late Run with the scale set from the data (peak 180 mm on 5 July), end card credits IMERG, Worldview, JRC, Copernicus and NASADEM, and the "most flood water drained" line is gone (P06). New output is in the team's Submission folder. |
| R21 | P34: "cameras saw only cloud" overreached. | Video, deck and project page now say "NASA's daily satellite images" and keep the claim to 3 to 8 July. The video draws the 3 to 8 July band from `cloud_check.json`. |
| R22 | P01: slide 1 figures half checked. | Deck slide 2 and the project page use "22 landslides across Pune district, 4 dead and 2 missing" and "about 5,000 moved to safety in Pimpri Chinchwad alone", from Punekar News ?p=239349. "6,000+ evacuated" is not used anywhere. |
| R23 | P40: both landslide matches rest on one zone. | The video, deck (validation slide and notes) and project page now lead with floods (4 of 10) and the second orbit, and say the 2 landslide matches point to one zone that NASADEM does not keep. |
| R24 | P08: the demo script pointed at the Patan miss. | Our video and deck do not show Patan as a hit; the app lists it as a miss with its reason (ground gentler than 15°). |
| R25 | P33: Submission Guide not read. | Read on the evening of 14 Nov, European time (spaceappschallenge.org/resources/project-submission-guide, dated 13 Nov 2026). Form fields, demo limits, language and SI rules are summarised in `content/project_page.md` and `content/demo_script.md`; what they change for us is P41 to P45. |
| R26 | P37: slide links were placeholders. | `content/slides.md` now gives the live app and repository addresses from `README.md`. One placeholder remains on the title slide: the members' full names. |
| R27 | `content/slides.md` had 8 slides, over the guide's limit (part of P41). | Cut to 7 including a title slide with team and challenge: "Why radar" and "What we built" merged, "Business model" and "Roadmap and team" merged. Slide 2 uses the figures from R22; no `[VERIFY]` lines remain. |
| R29 | Part of P46: there was no chance baseline for the flood matches. | Computed on 15 Nov by `pipeline/flood_baseline.py` from the published map layers, exactly (no random draws), against two reference sets: flat ground and OpenStreetMap settlements. Shown on the Method page with a chart and a per-report table, and in the checks band. The result is unfavourable and stays open as P46 and P47. The same calculation reproduces the pipeline's distances for E012 (126 m) and gives 2,400 m for the moved E016. |
| R28 | Part of P44: three confirmations were missing. | Urvashi confirmed on 14 Nov: ChatGPT was used by one team member; the idea and choice of event were the team's own; members are Ayush Singh Negi, Urvashi Negi and Rajendra Singh Negi. Filled into `content/project_page.md`, `content/slides.md` and the README "Use of AI" section. |
