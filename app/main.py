# -*- coding: utf-8 -*-
from fastapi import FastAPI

from .api import geojson, shapefile

app = FastAPI()

app.include_router(geojson.router, prefix="/geojson", tags=["geojson"])
app.include_router(shapefile.router, prefix="/shapefile", tags=["shapefile"])
