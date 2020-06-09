# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Query, Depends, Path
from geopy.geocoders.base import Geocoder
from geopy.exc import GeocoderNotFound, GeocoderQueryError, GeopyError
from pydantic import BaseModel
from typing import Any

from ..core.geocode import build_geocode_service as base_build_geocode_service, GeocodeException

router = APIRouter()


class GeocodeErrorResponse(BaseModel):
    detail: str = None


class GeocodeResponse(BaseModel):
    address: str = None
    lat: float = None
    lng: float = None
    raw: Any = None


def build_geocode_service(provider: str = Path(..., description="A geocode service code supported by geopy library"),
                          api_key: str = Query(None, description="Optional api key mandatory for some services"),
                          cache: int = Query(0, description="Size of an in memory cache for geocode result "
                                                            "(0 = disabled)")):
    try:
        return base_build_geocode_service(provider, api_key=api_key, cache=cache)
    except GeocoderNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GeocodeException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{provider}', summary="Geocode an address using different providers",
            description="This endpoint sends a geocode query to the specified provider",
            response_description="Geocode response (lat, lng)",
            response_model=GeocodeResponse,
            responses={400: {"description": "Geocoder query error", "model": GeocodeErrorResponse}})
def geocode(q: str = Query(..., description="The location you want to geocode"),
            geocode_service: Geocoder = Depends(build_geocode_service)):
    try:
        location = geocode_service.geocode(q)
    except GeocoderQueryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GeopyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if location is None:
        raise HTTPException(status_code=400, detail="No result found for query \"{}\"".format(q))

    return {
        'address': location.address,
        'lat': location.latitude,
        'lng': location.longitude,
        'raw': location.raw
    }
