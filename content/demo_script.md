# Demo scripts (U7)

Two scripts: the 30-second video that goes on the project page, and a 3-minute live walk-through.
Every number is from `data/derived/` (metrics.json generated 2026-11-14T19:01Z, `timeline.csv`,
`dem_check.json`) or from a source the team opened. Recheck them after any new pipeline run.
Open points are in `plotholes.md`; the "Do not say" list at the end comes from it.

**Corrected (plotholes.md P07, P46):** the pipeline was re-run on 15 November with E016 at its real location. Floods are **3 of 10** (7 misses). Every match is to a "possible water under cover" patch, and places nobody reported match about as often (3.8 of 10), so the flood count is a limit, not evidence: say "no better than chance", never "flood detected".

## What the 2026 Project Submission Guide allows

Read on spaceappschallenge.org/resources/project-submission-guide (dated 13 Nov 2026):

- The project demo is **either** a video of **30 seconds or less**, **or** a slide deck of **at most
  7 slides** including title and intro. Going over either limit makes the project ineligible for
  Global Judging.
- The demo is hosted elsewhere (for example YouTube) behind a public link with no login.
- English only. A video may be spoken in another language if it has English subtitles.
- No images, video or audio of anyone under 18.

So the 3-minute script below is **not** a submission format. Use it only if GDG Ahlen's local
judging has a live pitch; check with the Local Lead.

## 1. The 30-second video (the submission demo)

Timings follow the guide's suggested structure. 64 spoken words.

| Time | On screen | Voice-over and caption |
|---|---|---|
| 0:00 | Title card: team name | "We are Team iGenfinity." |
| 0:02 | Challenge name over the cloud contact sheet | "Our challenge: Dancing with the SARs." |
| 0:05 | Project title and tagline | "MonsoonLens: NISAR sees what monsoon clouds hide." |
| 0:10 | Rain chart, then the before/after radar swipe | "July 2026: floods and landslides hit Pune under solid cloud. NISAR's radar saw through it." |
| 0:15 | Map with new water and slide zones, then the validation table | "We mapped new water and 50 likely slide zones, checked them against 18 reported events, and published every miss." |
| 0:22 | Timeline chart, then the live app address | "It runs on any NISAR pass, for any district. Free data, open code." |

Captions repeat the voice-over word for word.

## 2. The 3-minute live walk-through (local judging only)

Ayush drives the live app; one person speaks. About 330 words, which leaves time for clicks.

| Time | Show | Say |
|---|---|---|
| 0:00-0:25 | Story step 1: rain chart | "Early July 2026. Days of extreme rain over Pune and the Western Ghats. Local news counted 22 landslides across the district; four people died. And for six days, 3 to 8 July, every one of NASA's daily satellite images of this area showed only cloud." |
| 0:25-1:05 | Story steps 2 and 3: cloud check, then the swipe | "NISAR carries an L-band radar. Its 24-centimetre pulses pass through cloud and rain. Smooth water looks dark; rough ground looks bright. NISAR passed on 28 June and again on 10 July. Drag the slider: the dark patches that appear are new water. 8.5 square kilometres where reservoirs and rivers rose, and 0.36 square kilometres of flood water still standing on ground that was never recorded wet between 1984 and 2021." |
| 1:05-1:45 | Story step 4, then Explore: slide zones | "On the steep slopes the radar signal changed in 50 places: likely slide zones, 8 of them high confidence. These are leads to check, not confirmed landslides: 46 have no reported event within 2 kilometres. So we tested them twice. A second NISAR orbit saw 12 of the zones and found 2 again, about 8 times what chance gives. And re-running with NASA's own elevation map finds 35 of the 50 again, including 7 of the 8 high-confidence ones." |
| 1:45-2:30 | Method page: validation table; Overview: "What radar could not see" | "Then we checked against the ground. 18 reported events, each linked to its source. Floods: radar could observe 10, and 3 had a possible-water patch nearby, which is no better than chance. The 7 we missed were all in or near towns, where radar echoes off walls can hide flooded streets. Landslides: of the 7 we could locate, radar could observe 4. We matched 2, both to a single zone, and that match does not hold when we switch elevation maps. The Patan landslide, which buried a house, we missed. All of that is on screen, not hidden." |
| 2:30-3:00 | Story step 5: the weeks after; then the repo | "The radar kept coming back. Open water grew from 153 square kilometres on 28 June to 191 by 14 October as the reservoirs filled. The same code runs on any pair of NISAR passes, for any district. The data is free and the code is open." |

## Where each spoken number comes from

| Said | Value | Source |
|---|---|---|
| 22 landslides; four died | 22; 4 dead in two days, 2 missing | Punekar News, 7 July 2026 (`?p=239349`), opened by the team on 15 Nov; see `plotholes.md` P01 |
| Six days of cloud, 3 to 8 July | 22 of 24 images available, all cloud | `content/cloud_check.md`, `data/reference/cloud_check.json` |
| 24-centimetre pulses | L-band SAR, 24 cm | NASA Science, NISAR mission page |
| Pass dates | 28 Jun, 10 Jul 2026 | `data/derived/timeline.csv` |
| Reservoirs and rivers rose | 8.5 km² (8.523) | `metrics.json` → `water.rise_km2` |
| Flood water still standing | 0.36 km² (0.365), 30 patches | `metrics.json` → `water.flood_km2` |
| Likely slide zones; high confidence | 50; 8 | `metrics.json` → `slides` |
| No reported event within 2 km | 46 of 50 | `metrics.json` → `validation.unreported_slide_zones` |
| Second orbit | 12 zones seen, 2 found again, lift 7.9, p = 0.026 | `metrics.json` → `crosstrack` (track 106, 3 to 15 July) |
| NASA elevation map check | 35 of 50 found again; 7 of 8 high confidence | `data/derived/dem_check.json` (NASADEM) |
| Reported events | 18 | `validation_summary.json` |
| Floods | 10 observable, 3 matched to a possible-water patch (chance: 3.8 of 10), 7 missed, all in or near towns | `validation.csv`, `flood_baseline.json` |
| Landslides | 7 located, 4 observable, 2 matched, both to zone SZ030 | `validation.csv`, `dem_check.json` |
| Match fails with the other elevation map | 0 of 4 with NASADEM | `dem_check.json`, `plotholes.md` P40 |
| Open water over the season | 153.0 km² (28 Jun) to 190.99 km² (14 Oct) | `data/derived/timeline.csv` |

## Do not say

- "Here's the Patan slide." We did not detect it (P08).
- "22 reported landslides" as the number we checked. We could locate 7 (P09).
- "6,000 evacuated." The source gives about 5,000 moved in Pimpri Chinchwad and "thousands" overall (P01).
- "We detected 3 of 10 floods." Each match is to a possible-water patch, not to mapped flood water, and random places match as often (P07, P46).
- Percentages or "accuracy". Say "3 of 10" and "2 of 4" (P11).
- "Most flood water had drained." We know the rain stopped, not how much water drained (P06).
- "Satellites could not see." Say "NASA's daily satellite images", and only for 3 to 8 July (P34).
- "Landslide" for a radar zone. Say "likely slide zone".
- That the second orbit or the elevation check confirms the whole map (P13).
