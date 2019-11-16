# -*- coding: utf-8 -*-
import io
import json
import zipfile

from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel
from typing import Dict, List, Any

from ..core.shapefile import convert_zipped_shp_to_geojson


class GeoJSONCrs(BaseModel):
    type: str = None
    properties: Dict[str, Any] = None


class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: List = None


class GeoJSONFeature(BaseModel):
    type: str
    properties: Dict[str, Any] = None
    geometry: GeoJSONGeometry = None


class GeoJSON(BaseModel):
    type: str
    crs: GeoJSONCrs = None
    features: List[GeoJSONFeature] = None
    properties: Dict[str, Any] = None
    geometry: GeoJSONGeometry = None


def route_convert_shop_to_geojson(router: APIRouter, path: str):
    def decorator_route_convert_shop_to_geojson(func):
        @router.post(path, summary="Convert an ESRI Shapefile to Geojson",
                     description="This endpoint takes at least the three mandatory files that defines an ESRI shapefile"
                                 " and returns the corresponding geojson file in its body",
                     response_description="A valid Geojson",
                     response_model=GeoJSON)
        async def shp_to_geosjon(
                shp_file: UploadFile = File(..., description=".shp — shape format, the feature geometry itself"),
                shx_file: UploadFile = File(..., description=".shx — shape index format, a positional index of the "
                                                             "feature geometry to allow seeking forwards and backwards "
                                                             "quickly"),
                dbf_file: UploadFile = File(..., description="dbf — attribute format, columnar attributes for each "
                                                             "shape, in dBase IV format"),
                prj_file: UploadFile = File(None, description=".prj — projection description, using a well-known text "
                                                              "representation of coordinate reference systems"),
                sbn_file: UploadFile = File(None, description=".sbn and .sbx — a spatial index of the features"),
                sbx_file: UploadFile = File(None, description=".sbn and .sbx — a spatial index of the features"),
                shp_xml_file: UploadFile = File(None, description=".shp.xml — geospatial metadata in XML format, such "
                                                                  "as ISO 19115 or other XML schema"),
                cpg_file: UploadFile = File(None, description=".cpg — used to specify the code page (only for .dbf) for"
                                                              " identifying the character encoding to be used"),
                source_crs: str = Form(None, description="the shapefile coordinate reference system — Given an integer "
                                                         "code, returns an EPSG-like mapping or turn a PROJ.4 string "
                                                         "into a mapping of parameters.\n\n"
                                                         "Note: it overwrites any data read from the proj file"),
                dest_crs: str = Form(None, description="the geojson coordinate reference system — Given an integer "
                                                       "code, returns an EPSG-like mapping or turn a PROJ.4 string "
                                                       "into a mapping of parameters."),
                source_encoding: str = Form(None, description="source file encoding\n\n"
                                                              "Note: don't specify if source is UTF-8"),
                dest_encoding: str = Form(None, description="destination file encoding file\n\n"
                                                            "Note: most usually in recent python version, you"
                                                            "won't have to specify as default is utf-8"),
                simplify_tolerance: float = Form(None, description="Returns a simplified geometry produced by the "
                                                                   "Douglas-Peucker algorithm. Coordinates of the "
                                                                   "simplified geometry will be no more than the "
                                                                   "tolerance distance from the original"),
                simplify_preserve_topology: bool = Form(False, description="if simplify_tolerance is used, unless the "
                                                                           "topology preserving option is used, the "
                                                                           "algorithm may produce self-intersecting or "
                                                                           "otherwise invalid geometries")):
            # Build an in-memory zip file with all the files needed for conversion
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                zip_file.writestr(shp_file.filename, await shp_file.read())
                zip_file.writestr(shx_file.filename, await shx_file.read())
                zip_file.writestr(dbf_file.filename, await dbf_file.read())
                for optional_file in [prj_file, sbn_file, sbx_file, shp_xml_file, cpg_file]:
                    if optional_file:
                        zip_file.writestr(optional_file.filename, await optional_file.read())

            # Reset pointer in in-memory zip file
            zip_buffer.seek(0)

            # Convert the zipped shapefile to geojson
            f_out = convert_zipped_shp_to_geojson(zip_buffer, shp_file.filename, source_crs, dest_crs,
                                                  source_encoding, dest_encoding,
                                                  simplify_tolerance, simplify_preserve_topology)

            # Returns geojson as json response
            return json.loads(f_out.read())
        return shp_to_geosjon
    return decorator_route_convert_shop_to_geojson
