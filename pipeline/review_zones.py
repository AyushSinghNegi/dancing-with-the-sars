"""Desk-review initial footprints with ESA WorldCover 2021 v200.

Refine forest, farmland and river to the largest connected target-class patch
inside each initial footprint. Keep the city control boundary unchanged.
This checks historical land cover; it does not establish 2026 control stability.
"""
from __future__ import annotations
import json
import shutil
import numpy as np
import rasterio
from rasterio.features import geometry_mask, shapes
from rasterio.windows import from_bounds
from scipy import ndimage
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from . import config as C
from .common import write_json

SOURCE = ("https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
          "ESA_WorldCover_10m_2021_v200_N18E072_Map.tif")
CLASSES = {"Z01": (10, "tree cover"), "Z02": (40, "cropland"),
           "Z03": (50, "built-up"), "Z04": (80, "permanent water")}


def main():
    original = C.REFERENCE / "zones-initial.geojson"
    target = C.REFERENCE / "zones.geojson"
    if not original.exists():
        shutil.copy2(target, original)
    collection = json.loads(original.read_text())
    cache = C.ANCILLARY / "worldcover"
    cache.mkdir(parents=True, exist_ok=True)
    reviews = []
    for feature in collection["features"]:
        props, geometry = feature["properties"], feature["geometry"]
        zone_id = props["id"]
        code, label = CLASSES[zone_id]
        local = cache / f"{zone_id}.tif"
        if not local.exists():
            with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif"):
                with rasterio.open(SOURCE) as src:
                    window = from_bounds(*shape(geometry).bounds, transform=src.transform).round_offsets().round_lengths()
                    values, transform = src.read(1, window=window), src.window_transform(window)
                    with rasterio.open(local, "w", driver="GTiff", width=values.shape[1], height=values.shape[0],
                                       count=1, dtype="uint8", crs=src.crs, transform=transform, nodata=0) as dst:
                        dst.write(values, 1)
        with rasterio.open(local) as src:
            values, transform = src.read(1), src.transform
        mask = geometry_mask([geometry], out_shape=values.shape, transform=transform, invert=True)
        classes, counts = np.unique(values[mask], return_counts=True)
        fractions = {str(k): round(100 * int(v) / int(mask.sum()), 2) for k, v in zip(classes, counts)}
        if zone_id != "Z03":
            components, count = ndimage.label(mask & (values == code))
            sizes = np.bincount(components.ravel()); sizes[0] = 0
            if count == 0:
                raise ValueError(f"No {label} in {zone_id}")
            chosen = components == sizes.argmax()
            polygons = [shape(g) for g, v in shapes(chosen.astype("uint8"), mask=chosen, transform=transform) if v == 1]
            feature["geometry"] = mapping(unary_union(polygons))
        refined = geometry_mask([feature["geometry"]], out_shape=values.shape, transform=transform, invert=True)
        props["review_status"] = "desk-reviewed against WorldCover 2021; 2026 land cover/stability unverified"
        props["source"] = SOURCE
        props["review_reference_year"] = 2021
        props["reference_class"] = label
        props["reference_target_percent"] = round(float(np.mean(values[refined] == code) * 100), 2)
        props["delineation"] = "original city control boundary" if zone_id == "Z03" else "largest connected target-class patch inside initial footprint"
        reviews.append({"zone_id": zone_id, "initial_class_percent": fractions, **props})
        print(zone_id, label, props["reference_target_percent"], flush=True)
    write_json(target, collection)
    write_json(C.REFERENCE / "zone_landcover_review.json", {
        "source": SOURCE, "doi": "https://doi.org/10.5281/zenodo.7254221",
        "attribution": "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium",
        "limitation": "Historical classified reference, not field truth or proof of 2026 stability",
        "zones": reviews})


if __name__ == "__main__":
    main()
