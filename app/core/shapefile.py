# -*- coding: utf-8 -*-
import fiona
import fiona.crs
import fiona.io
import fiona.transform
from shapely.geometry import mapping, shape

from .crs import from_crs


def convert_zipped_shp_to_geojson(zip_file, shp_filename, source_crs=None, dest_crs=None,
                                  source_encoding=None, dest_encoding=None,
                                  simplify_tolerance=None, simplify_preserve_topology=None):
    f_out = fiona.io.MemoryFile()

    source_crs = from_crs(source_crs) if source_crs else source_crs
    dest_crs = from_crs(dest_crs) if dest_crs else from_crs('+proj=latlong +datum=WGS84')

    with fiona.io.ZipMemoryFile(zip_file) as fio_zip:
        with fio_zip.open(shp_filename, encoding=source_encoding) as source:
            # Authorize MultiPolygon because shp file most often only sets Polygon in schema
            if source.schema['geometry'] == 'Polygon':
                source.schema['geometry'] = ('Polygon', 'MultiPolygon')

            # if no custom source crs use the one from schema
            if not source_crs:
                source_crs = source.crs

            # if no destination encoding use the one from parameters or schema
            if not dest_encoding and source.encoding:
                dest_encoding = source_encoding
            elif not dest_encoding and source_encoding:
                dest_encoding = source.encoding

            with fiona.open(
                    f_out,
                    'w',
                    encoding=dest_encoding,
                    driver='GeoJSON',
                    crs=dest_crs,
                    schema=source.schema) as sink:

                for rec in source:
                    # convert coordinates to another reference system
                    if source_crs and dest_crs and source_crs != dest_crs:
                        rec['geometry'] = fiona.transform.transform_geom(source_crs, dest_crs, rec['geometry'])

                    if simplify_tolerance:
                        geo = shape(rec['geometry']).simplify(simplify_tolerance,
                                                              preserve_topology=simplify_preserve_topology)
                        rec['geometry'] = mapping(geo)

                    sink.write(rec)

    # Reset pointer in file handler
    f_out.seek(0)

    return f_out
