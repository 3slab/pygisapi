# -*- coding: utf-8 -*-
from . import client, ShpTestFiles, geojson_test_content


def test_shapefile_to_geojson():
    with ShpTestFiles() as shp_test_files:
        response = client.post("/geojson/convert-from-shapefile", files=shp_test_files)
        assert response.status_code == 200
        assert response.json() == geojson_test_content
