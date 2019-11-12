import io
import json
import zipfile

from fastapi import APIRouter, File, UploadFile
import fiona
import fiona.crs
import fiona.io
import fiona.transform
from shapely.geometry import mapping, shape

router = APIRouter()


def convert_zipped_shp_to_geojson(zip_file, shp_filename):
    f_out = fiona.io.MemoryFile()

    # TODO : remove hardcoding (handle parameters)
    source_crs = fiona.crs.from_epsg('2154')
    dest_crs = fiona.crs.from_string('+proj=latlong +datum=WGS84')

    with fiona.io.ZipMemoryFile(zip_file) as fio_zip:
        with fio_zip.open(shp_filename) as source:
            # Authorize MultiPolygon because shp file most often only sets Polygon in schema
            if source.schema['geometry'] == 'Polygon':
                source.schema['geometry'] = ('Polygon', 'MultiPolygon')

            with fiona.open(
                    f_out,
                    'w',
                    # TODO : handle encoding issues encoding="iso-8859-1",
                    driver='GeoJSON',
                    crs=dest_crs,
                    schema=source.schema) as sink:

                for rec in source:
                    # convert coordinates to another reference system
                    rec['geometry'] = fiona.transform.transform_geom(source_crs, dest_crs, rec['geometry'])

                    # TODO : handle simplify shape
                    # geo = mapping(shape(rec['geometry']).simplify(0.05))
                    # rec['geometry'] = mapping(geo)

                    sink.write(rec)

    # Reset pointer in file handler
    f_out.seek(0)

    return f_out


@router.post("/convert-from-shp")
async def shp_to_geosjon(
        shp_file: UploadFile = File(...),
        shx_file: UploadFile = File(...),
        dbf_file: UploadFile = File(...),
        prj_file: UploadFile = File(None)):
    # Build an in-memory zip file with all the files needed for conversion
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr(shp_file.filename, await shp_file.read())
        zip_file.writestr(shx_file.filename, await shx_file.read())
        zip_file.writestr(dbf_file.filename, await dbf_file.read())
        if prj_file:
            zip_file.writestr(prj_file.filename, await prj_file.read())

    # Reset pointer in in-memory zip file
    zip_buffer.seek(0)

    # Convert the zipped shapefile to geojson
    f_out = convert_zipped_shp_to_geojson(zip_buffer, shp_file.filename)

    # Returns geojson as json response
    return json.loads(f_out.read())
