"""Apply real GCOV/GUNW validity masks to saved crops without re-reading radar.

Real-file metadata declares mask 0 invalid/partially focused and 255 outside
acquisition. This conservative pass requires full valid native support for each
40 m pixel. It can repair crops made before mask-0 handling was implemented.
"""
from __future__ import annotations
import json
import numpy as np
import rasterio
from . import config as C, nisar_io as io

RULE = 'fully-focused-native-support-v1'
GUNW_RULE = 'valid-subswaths-no-rslc-anomalies-v1'


def valid_values(block):
    mask = block['mask']
    return {'mask': ((mask != 0) & (mask != 255)).astype(np.float32)}


def gunw_valid_values(block):
    # Source mask description: low byte is water/ref-subswath/sec-subswath;
    # bits 8..23 are secondary/reference RSLC anomaly flags.
    mask = block['mask'].astype(np.uint32)
    subswath = mask & 255
    valid = ((subswath != 255) & ((subswath // 10) % 10 != 0) &
             (subswath % 10 != 0) & ((mask & 0x00FFFF00) == 0))
    return {'mask': valid.astype(np.float32)}


def apply(gid, source):
    if C.IS_DEMO:
        raise ValueError('Real quality repair requires real mode')
    name = io.crop_name(gid)
    gunw = C.parse_granule_id(gid)['product'] == 'GUNW'
    rule = GUNW_RULE if gunw else RULE
    quality_path = C.CROPS / f'{name}_QUALITY.tif'
    if quality_path.exists():
        valid = io.load_unit(quality_path) == 1
    else:
        print(f'[quality] {name}: reading native validity mask', flush=True)
        with io.open_h5(source, block_size=1024 * 1024) as f:
            if 'SYNTHETIC' in f.attrs:
                raise ValueError('Synthetic file cannot be used for real quality masks')
            if gunw:
                coherence_path, coord_group, _ = io.find_coherence(f)
                mask_path = coherence_path.rsplit('/', 2)[0] + '/mask'
            else:
                coord_group, mask_path = io.GCOV_GRID, f'{io.GCOV_GRID}/mask'
            arrays, _ = io.read_to_grid(f, {'mask': mask_path}, coord_group,
                                        value_transform=gunw_valid_values if gunw else valid_values)
        valid = np.isclose(arrays['mask'], 1.0, rtol=0, atol=1e-6)
        io.save_unit_uint8(quality_path, valid.astype(np.float32), {'granule_id': gid, 'quality_rule': rule})
    observed = valid.copy()
    for pol in (('COH',) if gunw else ('HH', 'HV')):
        path = C.CROPS / f'{name}_{pol}.tif'
        with rasterio.open(path) as src:
            tags = src.tags()
        tags.pop('scale', None)
        values = (io.load_unit if gunw else io.load_db)(path)
        values[~valid] = np.nan
        observed &= np.isfinite(values)
        (io.save_unit_uint8 if gunw else io.save_db_int16)(path, values, {**tags, 'quality_rule': rule})
    manifest = C.CROPS / 'manifest.json'
    entries = json.loads(manifest.read_text())
    entry = next(m for m in entries if m['granule_id'] == gid)
    entry.update(quality_rule=rule, valid_fraction=round(float(observed.mean()), 4),
                 mask_valid_fraction=round(float(valid.mean()), 4))
    io.update_manifest(entry)
    print(f'[quality] {name}: usable fraction {entry["valid_fraction"]:.4f}', flush=True)
