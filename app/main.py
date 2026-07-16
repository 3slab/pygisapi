# -*- coding: utf-8 -*-
from .logging_config import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .api import geocode, geojson, shapefile, coords
from fastapi.openapi.docs import get_redoc_html
from .middlewares.access_log import JSONLoggingMiddleware

app = FastAPI(
    title="PyGISAPI",
    description="API géospatiale : géocodage, coords, shapefile, geojson",
    version="1.0.0",
    redoc_url=False,
)
app.add_middleware(JSONLoggingMiddleware)

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="API Docs",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.5.3/bundles/redoc.standalone.js",
    )

app.include_router(geocode.router, prefix="/geocode", tags=["geocode"])
app.include_router(geojson.router, prefix="/geojson", tags=["geojson"])
app.include_router(shapefile.router, prefix="/shapefile", tags=["shapefile"])
app.include_router(coords.router, prefix="/coords", tags=["coords"])

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

