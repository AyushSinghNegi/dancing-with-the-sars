# Sources for data/reference/

Every entry below is copied from the file itself or from the code that fetched it.

## Rainfall: `rainfall.csv`

| | |
|---|---|
| Product | GPM IMERG Late Run, daily: "Daily mean precipitation rate (combined microwave-IR) estimate - Late Run" |
| Short name and version | GPM_3IMERGDL v07 |
| Variable | `GPM_3IMERGDL_07_precipitation`, mm/day |
| Tool | NASA Giovanni v4.40, plot type "Time Series, Area-Averaged" |
| Dates | 2026-06-15 to 2026-10-31 (UTC days), 139 daily values, none missing |
| Box requested | West 73.3, South 18.15, East 74.1, North 18.9 |
| Box used by the data grid | West 73.35, South 18.15, East 74.05, North 18.85 (as reported by Giovanni) |
| Downloaded | 2026-11-14 |
| Raw download, unedited | `g4.areaAvgTimeSeries.GPM_3IMERGDL_07_precipitation.20260615-20261031.73E_18N_74E_18N.csv` |

Link to reproduce (from the header of the raw file):
https://giovanni.gsfc.nasa.gov/giovanni/#service=ArAvTs&starttime=2026-06-15T00:00:00Z&endtime=2026-10-31T23:59:59Z&bbox=73.3,18.15,74.1,18.9&data=GPM_3IMERGDL_07_precipitation&dataKeyword=IMERG

Why the Late Run: on the download date Giovanni listed the daily Final Run (GPM_3IMERGDF v07) as
ending 2025-09-30, so it does not cover July 2026.

How `rainfall.csv` was made: the `time` and `mean_GPM_3IMERGDL_07_precipitation` columns of the raw
file were renamed to `date` and `precip_mm`, and a `source` column was added. No value was changed
or rounded.

This replaces the earlier interim file from `pipeline/rainfall.py` (NASA POWER PRECTOTCORR, MERRA-2).
Do not run `python -m pipeline.rainfall` unless you mean to overwrite the IMERG data.

## Permanent water: JRC Global Surface Water

Fetched by `pipeline/ancillary.py`, not stored in this folder.

| | |
|---|---|
| Product | JRC Global Surface Water v1.4 (1984-2021), occurrence layer |
| Citation | Pekel et al. (2016) Nature 540:418-422 |
| Tile | `occurrence_70E_20Nv1_4_2021.tif` |
| Cropped to the box | `data/crops/aux_jrc_occurrence.tif` |

## Elevation

Fetched by `pipeline/ancillary.py` (Copernicus) or prepared by RSN (NASADEM); stored in `data/crops/`.

| | Main run | Elevation-map check |
|---|---|---|
| Product | Copernicus GLO-30 DEM (ESA / Airbus), via AWS Open Data | NASADEM_HGT v001 (NASA / USGS), doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001 |
| Tiles | N18 E073, N18 E074 | n18e073, n18e074 |
| On the 40 m grid | `aux_elevation.tif` (bilinear), `aux_slope.tif` | `aux_nasadem_elevation.tif` (bilinear, by RSN on `rsn/pipeline`; whole metres) |
| Slope | central differences on the 40 m grid, whole degrees | same, computed in `pipeline/dem_check.py` |

## Place names: `places_osm.csv`

| | |
|---|---|
| Source | OpenStreetMap (© OpenStreetMap contributors, ODbL) |
| What | every node tagged `place` = city, town, village or suburb inside the study box: 431 places, 244 with a Marathi name (`name:mr`) |
| Fetched | 14 Nov 2026, Overpass API, query in `pipeline/gazetteer.py` |
| Raw download, unedited | `osm_places_raw.json` |
| Used for | the app's "Check a place" search |

## Reported events: `events.geojson`

Each event carries its own `source_name` and `source_url`.
