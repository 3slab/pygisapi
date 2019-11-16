# -*- coding: utf-8 -*-
import fiona.crs


def from_crs(value):
    if not value:
        return None

    try:
        return fiona.crs.from_epsg(int(value))
    except ValueError:
        return fiona.crs.from_string(value)
