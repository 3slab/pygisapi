# -*- coding: utf-8 -*-
import fiona.crs
import pyproj


def from_crs(value):
    if not value:
        return None

    try:
        return fiona.crs.from_epsg(int(value))
    except ValueError:
        return fiona.crs.from_string(value)


def convert_coordinates(x, y, source_crs, dest_crs):
    source_crs = from_crs(source_crs)
    if not source_crs:
        raise ValueError('Invalid source_crs provided')

    dest_crs = from_crs(dest_crs)
    if not dest_crs:
        raise ValueError('Invalid dest_crs provided')

    proj = pyproj.Transformer.from_crs(source_crs, dest_crs, always_xy=True)
    return proj.transform(x, y)
