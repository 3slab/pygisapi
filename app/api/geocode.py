# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Query
from geopy.exc import GeocoderNotFound, GeopyError
from pydantic import BaseModel
from typing import Any

from ..core.geocode import build_geocode_service, GeocodeException

router = APIRouter()


class GeocodeResponse(BaseModel):
    address: str = None
    lat: float = None
    lng: float = None
    raw: Any = None


@router.get('/{provider}', summary="Geocode an address using different providers",
            description="This endpoint sends a geocode query to the specified provider",
            response_description="Geocode response (lat, lng)",
            response_model=GeocodeResponse)
def geocode(provider: str,
            q: str = Query(..., description="The location you want to geocode"),
            api_key: str = Query(None, description="Optional api key mandatory for some services")):
    try:
        geocode_service = build_geocode_service(provider, api_key=api_key)
        location = geocode_service.geocode(q)
    except GeocoderNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GeocodeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GeopyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        'address': location.address,
        'lat': location.latitude,
        'lng': location.longitude,
        'raw': location.raw
    }
