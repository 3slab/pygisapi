# -*- coding: utf-8 -*-
from . import client, ShpTestFiles, geojson_test_content


def test_shapefile_to_geojson():
    with ShpTestFiles() as shp_test_files:
        response = client.post("/geojson/convert-from-shapefile", files=shp_test_files)
        assert response.status_code == 200
        assert response.json() == geojson_test_content


def test_centroid_no_geojson():
    response = client.post("/geojson/centroid")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}


def test_centroid_invalid_geojson():
    response = client.post("/geojson/centroid", json={'invalid': 'geojson'})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'type'], 'msg': 'field required',
                                           'type': 'value_error.missing'}]}


def test_centroid_multiple_valid_invalid_polygon():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                1.845703125,
                                48.40003249610685
                            ],
                            [
                                2.4169921874999996,
                                48.17341248658084
                            ],
                            [
                                2.30712890625,
                                48.531157010976706
                            ],
                            [
                                1.845703125,
                                48.40003249610685
                            ]
                        ]
                    ]
                }
            },
            {
                "invalid": "geojson"
            }
        ]
    })
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'features', 1, 'type'], 'msg': 'field required',
                                           'type': 'value_error.missing'}]}


def test_centroid_valid_single_polygon():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                1.845703125,
                                48.40003249610685
                            ],
                            [
                                2.4169921874999996,
                                48.17341248658084
                            ],
                            [
                                2.30712890625,
                                48.531157010976706
                            ],
                            [
                                1.845703125,
                                48.40003249610685
                            ]
                        ]
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{'x': 2.18994140625, 'y': 48.3682006645548}]


def test_centroid_valid_single_polygon_with_hole():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                        [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{"x": 100.50000000000001, "y": 0.5}]


def test_centroid_valid_single_feature_polygon():
    response = client.post("/geojson/centroid",
                           json={
                               "type": "Feature",
                               "properties": {},
                               "geometry": {
                                   "type": "Polygon",
                                   "coordinates": [
                                       [
                                           [
                                               1.845703125,
                                               48.40003249610685
                                           ],
                                           [
                                               2.4169921874999996,
                                               48.17341248658084
                                           ],
                                           [
                                               2.30712890625,
                                               48.531157010976706
                                           ],
                                           [
                                               1.845703125,
                                               48.40003249610685
                                           ]
                                       ]
                                   ]
                               }
                           })
    assert response.status_code == 200
    assert response.json() == {'x': 2.18994140625, 'y': 48.3682006645548}


def test_centroid_valid_single_point():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        3.218994140625,
                        47.56911375866714
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{"x": 3.218994140625, "y": 47.56911375866714}]


def test_centroid_valid_single_multipoint():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiPoint",
                    "coordinates": [[100.0, 0.0], [101.0, 1.0]]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{"x": 100.5, "y": 0.5}]


def test_centroid_valid_single_linestring():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            0.791015625,
                            47.338822694822
                        ],
                        [
                            2.724609375,
                            46.619261036171515
                        ]
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{"x": 1.7578125, "y": 46.979041865496754}]


def test_centroid_valid_single_multilinestring():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [[100.0, 0.0], [101.0, 1.0]],
                        [[102.0, 2.0], [103.0, 3.0]]
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{"x": 101.50000000000001, "y": 1.5}]


def test_centroid_valid_single_multipolygin():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
                        [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                         [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{"x": 101.71951219512191, "y": 1.7195121951219483}]


def test_centroid_valid_multiple_polygon():
    response = client.post("/geojson/centroid", json={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                1.845703125,
                                48.40003249610685
                            ],
                            [
                                2.4169921874999996,
                                48.17341248658084
                            ],
                            [
                                2.30712890625,
                                48.531157010976706
                            ],
                            [
                                1.845703125,
                                48.40003249610685
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                3.548583984375,
                                48.56024979174329
                            ],
                            [
                                3.878173828125,
                                47.68757916850813
                            ],
                            [
                                5.03173828125,
                                48.63290858589535
                            ],
                            [
                                4.515380859375,
                                49.21759710517596
                            ],
                            [
                                4.053955078125,
                                48.99463598353405
                            ],
                            [
                                3.93310546875,
                                48.647427805533546
                            ],
                            [
                                3.548583984375,
                                48.56024979174329
                            ]
                        ]
                    ]
                }
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [{'x': 2.18994140625, 'y': 48.3682006645548},
                               {'x': 4.253404608479556, 'y': 48.50501625650114}]
