# -*- coding: utf-8 -*-
from fastapi import APIRouter
from pydantic.typing import Union, List
from shapely.geometry import shape, GeometryCollection

from .shared import route_convert_shop_to_geojson, CoordinatesResponse, StandardErrorResponse, GeoJSON

router = APIRouter()


@route_convert_shop_to_geojson(router, "/convert-from-shapefile")
def geojson_to_shp():
    raise Exception('this method should not execute as it is replaced by the one from the decorator')


@router.post('/centroid', summary="Get the centroid of a geojson",
             description="This endpoint returns the coordinates of the centroid of the geojson",
             response_description="Coordinates response (x, y)",
             response_model=Union[CoordinatesResponse, List[CoordinatesResponse]],
             responses={400: {"description": "Shape handler query error", "model": StandardErrorResponse},
                        500: {"description": "Internal server error", "model": StandardErrorResponse}})
def centroid(geojson: GeoJSON):
    # handle multiple features geojson
    if geojson.features and not geojson.geometry:
        features = geojson.features
    else:
        features = [geojson]

    geo_col = GeometryCollection([shape(feature.geometry) for feature in features])
    centroids = [{'x': geom.centroid.x, 'y': geom.centroid.y} for geom in geo_col.geoms]

    if geojson.features and not geojson.geometry:
        return centroids
    else:
        return centroids[0]
