from fastapi import FastAPI

from .routers import geojson

app = FastAPI()

app.include_router(geojson.router, prefix="/geojson", tags=["geojson"])
