# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query, HTTPException

from ..core.coords import convert_coordinates
from .shared import CoordinatesResponse, StandardErrorResponse

router = APIRouter()


@router.get('/convert', summary="Convert a set of coordinates",
            description="This endpoint converts coordinates from one projection to another",
            response_description="Converted coordinates (x, y)",
            response_model=CoordinatesResponse,
            responses={400: {"description": "Coordinates query error", "model": StandardErrorResponse},
                       500: {"description": "Internal server error", "model": StandardErrorResponse}})
def convert(x: float = Query(..., description="coordinate on the x-axis"),
            y: float = Query(..., description="coordinate on the y-axis"),
            source_crs: str = Query(4326, description="the x,y coordinate reference system — Given an integer "
                                                      "code, returns an EPSG-like mapping or turn a PROJ.4 string "
                                                      "into a mapping of parameters."),
            dest_crs: str = Query(4326, description="the coordinate reference system you want to convert to "
                                                    " Given an integer code, returns an EPSG-like mapping or "
                                                    "turn a PROJ.4 string into a mapping of parameters.")):
    try:
        x2, y2 = convert_coordinates(x, y, source_crs, dest_crs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        'x': x2,
        'y': y2
    }
