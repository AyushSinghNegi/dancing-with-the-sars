"""Outside figures used in the reports and slides, each with its source, plus the planning assumptions of the
business plan (clearly marked as assumptions). Pipeline numbers are NOT here: they are read from
data/derived/metrics.json at build time.

Checked on 15 November 2026.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = json.loads((ROOT / "data" / "derived" / "metrics.json").read_text())

# ---------------------------------------------------------------- sources
SOURCES = {
    "froude": ("Froude, M. J. and Petley, D. N. (2018). Global fatal landslide occurrence from 2004 to 2016. "
               "Natural Hazards and Earth System Sciences 18, 2161-2181.", "https://doi.org/10.5194/nhess-18-2161-2018"),
    "rentschler": ("Rentschler, J., Salhab, M. and Jafino, B. A. (2022). Flood exposure and poverty in 188 countries. "
                   "Nature Communications 13, 3527.", "https://doi.org/10.1038/s41467-022-30727-4"),
    "ndma_lrms": ("National Disaster Management Authority (2019). National Landslide Risk Management Strategy. "
                  "Government of India.", "https://gidm.gujarat.gov.in/sites/default/files/educate_your_self_document/6National%20Landslide%20Risk%20Management%20Strategy.pdf"),
    "gsi_wghats": ("Geological Survey of India, as reported by PTI / The News Minute: landslide-prone area by region.",
                   "https://www.thenewsminute.com/news/126-india-vulnerable-landslides-geological-survey-india-43288"),
    "malin": ("Deccan Herald (2023). Irshalgad landslide a repeat of Malin, Taliye.",
              "https://www.deccanherald.com/india/irshalgad-landslide-a-repeat-of-malin-taliye-1238981.html"),
    "wayanad": ("Down To Earth (2026). Two years after the Mundakkai-Chooralmala catastrophe.",
                "https://www.downtoearth.org.in/climate-change/two-years-after-the-mundakkai-chooralmala-catastrophe-wayanad-and-kerala-are-at-a-crossroads"),
    "nisar_overview": ("NASA JPL. NISAR press kit, mission overview.", "https://jpl.nasa.gov/press-kits/nisar/mission-overview"),
    "nisar_asf": ("Alaska Satellite Facility DAAC. NISAR mission page.", "https://asf.alaska.edu/?p=22999"),
    "nisar_s3": ("ASF NISAR documentation. S3 access overview (Earthdata Cloud, AWS us-west-2).",
                 "https://nisar-docs.asf.alaska.edu/aws-s3-access/"),
    "nisar_open": ("NASA Earthdata (2025). Now that NISAR launched, here's what you can expect from the data.",
                   "https://www.earthdata.nasa.gov/news/now-that-nisar-launched-heres-what-you-can-expect-from-the-data"),
    "wef": ("World Economic Forum with Deloitte (2024). Amplifying the Global Value of Earth Observation.",
            "https://www3.weforum.org/docs/WEF_Amplifying_the_Global_Value_of_Earth_Observation_2024.pdf"),
    "gca": ("Global Commission on Adaptation (2019). Adapt Now, as summarised by Grist.",
            "https://grist.org/article/5-ways-we-need-to-adapt-to-climate-change-or-pay-the-price/"),
    "ew4all": ("WMO. Early Warnings for All (EW4All).", "https://community.wmo.int/node/38285"),
    "wmo_15": ("Down To Earth (2025). 'No one should die for lack of warning': WMO issues call to action.",
               "https://www.downtoearth.org.in/climate-change/no-one-should-die-for-lack-of-warning-wmo-issues-call-to-action"),
    "fc15": ("Rajya Sabha question on disaster risk financing, 20 July 2022 (15th Finance Commission allocations).",
             "https://indiaenvironmentportal.org.in/reports-and-documents/question-raised-in-rajya-sabha-on-disaster-risk-financing-20072022"),
    "sdmf": ("Press Information Bureau, 15 March 2023: SDMF allocation 2021-22 to 2025-26.",
             "https://pib.gov.in/PressReleasePage.aspx?PRID=1907163"),
    "sdrf": ("ANI / Chini Mandi (2022): SDRF corpus for 2021-26.", "https://chinimandi.com/?p=233875"),
    "aws": ("Vantage instance pricing: c7g.xlarge, 4 vCPU, 8 GiB, on-demand.", "https://instances.vantage.sh/aws/ec2/c7g.xlarge"),
    "pekel": ("Pekel, J.-F., Cottam, A., Gorelick, N. and Belward, A. S. (2016). High-resolution mapping of global surface "
              "water and its long-term changes. Nature 540, 418-422. JRC Global Surface Water v1.4.",
              "https://global-surface-water.appspot.com/"),
    "copdem": ("Copernicus GLO-30 Digital Elevation Model (ESA / Airbus), AWS Open Data.",
               "https://registry.opendata.aws/copernicus-dem/"),
    "nasadem": ("NASA JPL (2020). NASADEM Merged DEM Global 1 arc second V001 (NASADEM_HGT).",
                "https://doi.org/10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001"),
    "imerg": ("Huffman, G. J. et al. GPM IMERG Late Precipitation L3 1 day V07 (GPM_3IMERGDL), via NASA Giovanni.",
              "https://giovanni.gsfc.nasa.gov/"),
    "osm": ("OpenStreetMap contributors (ODbL): places, roads and railways, via Overpass and Nominatim.",
            "https://www.openstreetmap.org/copyright"),
    "worldview": ("NASA Worldview Snapshots (GIBS): true-colour daily imagery from MODIS and VIIRS.",
                  "https://worldview.earthdata.nasa.gov"),
    "kittler": ("Kittler, J. and Illingworth, J. (1986). Minimum error thresholding. Pattern Recognition 19(1), 41-47.",
                "https://doi.org/10.1016/0031-3203(86)90030-0"),
    "cia_land": ("CIA World Factbook: World, area.", "https://www.cia.gov/the-world-factbook/about/archives/2021/countries/world"),
}

# ---------------------------------------------------------------- the problem
LANDSLIDE_DEATHS_2004_2016 = 55_997          # froude
LANDSLIDE_EVENTS_2004_2016 = 4_862           # froude
FLOOD_EXPOSED_BN = 1.81                      # rentschler: people exposed to 1-in-100-year floods
FLOOD_EXPOSED_INDIA_M = 390                  # rentschler
INDIA_PRONE_KM2 = 420_000                    # ndma_lrms (GSI): 0.42 million km2, 12.6% of land
INDIA_PRONE_SHARE = 12.6
WGHATS_PRONE_KM2 = 90_000                    # gsi_wghats: Western Ghats and Konkan hills
MALIN_DEATHS, TALIYE_DEATHS = 151, 85        # malin
WAYANAD_DEATHS = 298                         # wayanad (official toll)

# ---------------------------------------------------------------- the opportunity
EO_VALUE_2023_BN, EO_VALUE_2030_BN, EO_GDP_2023_2030_TN = 266, 700, 3.8   # wef
WARNING_24H_DAMAGE_CUT = 30                  # gca: 24 h warning can cut damage by 30%
EW_SPEND_M, EW_AVOIDED_BN = 800, (3, 16)     # gca: $800 M in developing countries avoids $3-16 bn a year
WMO_DOLLAR_SAVES = 15                        # wmo_15: every dollar in early warnings saves up to 15
SDRF_CR, SDMF_CR, NDRMF_CR = 128_122, 32_031, 68_463   # sdrf, sdmf, fc15 (₹ crore, 2021-26)
SDRMF_CR = 160_153                                     # fc15

# ---------------------------------------------------------------- what it costs to run (measured + cited)
PIPELINE_SECONDS = 130          # measured 15 Nov 2026: `python -m pipeline.run_all`, 2 vCPU, from the cropped files
INSTANCE_USD_PER_H = 0.145      # aws: c7g.xlarge on-demand, us-west-2 (where NISAR data sits)
OVERHEAD = 3                    # assumption: x3 for streaming the NISAR crops, retries and idle time
TILE_KM2 = round(2127 * 2091 * 0.04 * 0.04)            # our study box on the 40 m grid
COST_PER_TILE_RUN_USD = PIPELINE_SECONDS / 3600 * INSTANCE_USD_PER_H * OVERHEAD
RUNS_PER_YEAR = round(365 / 12 * 2)                     # nisar_overview: twice every 12 days
EARTH_LAND_KM2 = 148_940_000                            # cia_land


def yearly_cost(area_km2):
    return max(1, area_km2 / TILE_KM2) * COST_PER_TILE_RUN_USD * RUNS_PER_YEAR


# ---------------------------------------------------------------- business plan: ASSUMPTIONS, not facts
PRICES = {   # USD per year (planning assumptions)
    "Public": (0, "Free forever: the open app, maps and code, for anyone"),
    "District": (6_000, "One district: custom area, alert after every pass, field app, training, support"),
    "State": (60_000, "All districts of a state, a state dashboard, API, and on-call analyst support"),
    "Infrastructure": (25_000, "A rail line, highway, dam or mine portfolio: corridor watch and change reports"),
    "Data and API": (50_000, "Insurers, reinsurers and humanitarian agencies: API, history, bulk export"),
}
PLAN = [   # year, districts, coverage (M km2), revenue, grants, cost (USD thousand): planning assumptions
    dict(year="2027", districts="3 pilot districts", coverage_mkm2=0.021, revenue_k=0, grants_k=120, cost_k=110),
    dict(year="2028", districts="25 districts", coverage_mkm2=0.09, revenue_k=175, grants_k=150, cost_k=260),
    dict(year="2029", districts="120 districts, 2 states", coverage_mkm2=0.42, revenue_k=980, grants_k=200, cost_k=720),
    dict(year="2030", districts="India + 3 countries", coverage_mkm2=5.0, revenue_k=2_600, grants_k=250, cost_k=1_650),
    dict(year="2031", districts="All land, open layer", coverage_mkm2=148.94, revenue_k=5_400, grants_k=300, cost_k=3_200),
]
ROADMAP_TICKS = ["Q4 2026", "H1 2027", "H2 2027", "2028", "2029", "2030"]
ROADMAP = [  # lane, label, start, end, colour
    ("Product", "Prototype: Pune", 0, 0.95, "cyan"),
    ("", "Runs on every new NISAR pass, alerts", 1, 2.9, "blue"),
    ("", "Both orbit directions, InSAR motion, S-band", 3, 4.9, "deep"),
    ("Validation", "Field checks with district teams", 1, 2.9, "blue"),
    ("", "Accuracy study over 3 monsoons", 3, 5.5, "deep"),
    ("Coverage", "Western Ghats and Konkan", 1.6, 3.1, "blue"),
    ("", "All landslide-prone India", 3.1, 4, "deep"),
    ("", "Monsoon Asia, then all land", 4, 5.5, "orange"),
    ("Business", "Grants and pilots", 0.5, 2.5, "cyan"),
    ("", "District and state subscriptions", 2.5, 5.5, "blue"),
    ("", "Infrastructure and insurance API", 3.4, 5.5, "deep"),
]
