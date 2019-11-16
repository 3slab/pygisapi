# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .shared import route_convert_shop_to_geojson

router = APIRouter()


@route_convert_shop_to_geojson(router, "/convert-from-shapefile")
def geojson_to_shp():
    raise Exception('this method should not execute as it is replaced by the one from the decorator')
