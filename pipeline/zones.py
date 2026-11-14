"""Reusable, explicit analysis polygons for R6 controls and R8 timelines.

The checked-in polygons are initial analyst-drawn footprints, not land-cover
truth. Their review status is carried into every output.
"""
from __future__ import annotations
import json
import numpy as np
from rasterio.features import geometry_mask
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform
from . import config as C
from . import nisar_io as io


def masks(path=None):
    path = path or C.REFERENCE / "zones.geojson"
    if not path.exists():
        raise FileNotFoundError(f"Analysis polygons missing: {path}")
    features = json.loads(path.read_text())["features"]
    grid, size = io.analysis_grid()
    project = Transformer.from_crs(4326, C.GRID_EPSG, always_xy=True).transform
    seen = set()
    for feature in features:
        props = feature["properties"]
        if props["id"] in seen:
            raise ValueError(f"Duplicate zone ID: {props['id']}")
        seen.add(props["id"])
        geom = shape(feature["geometry"])
        if geom.geom_type not in {"Polygon", "MultiPolygon"} or not geom.is_valid or geom.is_empty:
            raise ValueError(f"Invalid polygon for {props['id']}")
        mask = geometry_mask([mapping(transform(project, geom))], out_shape=size,
                             transform=grid, invert=True)
        if not np.any(mask):
            raise ValueError(f"Zone {props['id']} contains no analysis-grid cell centres")
        yield props, mask
