# -*- coding: utf-8 -*-
import json
import os

from starlette.testclient import TestClient

from app.main import app

test_dirname = os.path.dirname(os.path.abspath(__file__))
asset_dirname = os.path.join(test_dirname, 'assets')

geojson_test_file = os.path.join(asset_dirname, 'gis_osm_transport_a_free_1.geojson')
with open(geojson_test_file, 'rb') as json_file:
    geojson_test_content = json.load(json_file)

shp_test_file = os.path.join(asset_dirname, 'gis_osm_transport_a_free_1.shp')
shx_test_file = os.path.join(asset_dirname, 'gis_osm_transport_a_free_1.shx')
dbf_test_file = os.path.join(asset_dirname, 'gis_osm_transport_a_free_1.dbf')
prj_test_file = os.path.join(asset_dirname, 'gis_osm_transport_a_free_1.prj')
cpg_test_file = os.path.join(asset_dirname, 'gis_osm_transport_a_free_1.cpg')


class ShpTestFiles(object):
    def __init__(self):
        self.shp_file = open(shp_test_file, 'rb')
        self.shx_file = open(shx_test_file, 'rb')
        self.dbf_file = open(dbf_test_file, 'rb')
        self.prj_file = open(prj_test_file, 'rb')
        self.cpg_file = open(cpg_test_file, 'rb')

    def __enter__(self):
        return {'shp_file': self.shp_file,
                'shx_file': self.shx_file,
                'dbf_file': self.dbf_file,
                'prj_file': self.prj_file,
                'cpg_file': self.cpg_file}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shp_file.close()
        self.shx_file.close()
        self.dbf_file.close()
        self.prj_file.close()
        self.cpg_file.close()


client = TestClient(app)
