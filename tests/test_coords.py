# -*- coding: utf-8 -*-

from . import client


def test_coords_without_query():
    response = client.get("/coords/convert")
    assert response.status_code == 422
    assert response.json() == {'detail': [
        {'loc': ['query', 'x'], 'msg': 'field required', 'type': 'value_error.missing'},
        {'loc': ['query', 'y'], 'msg': 'field required', 'type': 'value_error.missing'}
    ]}


def test_coords_with_invalid_coordinates_query():
    response = client.get("/coords/convert", params={'x': 'not_coordinates', 'y': 'not_coordinates'})
    assert response.status_code == 422
    assert response.json() == {'detail': [
        {'loc': ['query', 'x'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
        {'loc': ['query', 'y'], 'msg': 'value is not a valid float', 'type': 'type_error.float'}
    ]}


def test_coords_with_invalid_source_crs_query():
    response = client.get("/coords/convert", params={'x': 2.48, 'y': 48.6, 'source_crs': 'invalid_crs'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid source_crs provided'}


def test_coords_with_invalid_dest_crs_query():
    response = client.get("/coords/convert", params={'x': 2.48, 'y': 48.6, 'dest_crs': 'invalid_crs'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid dest_crs provided'}


def test_coords_default_crs_query():
    response = client.get("/coords/convert", params={'x': 2.48, 'y': 48.6})
    assert response.status_code == 200
    assert response.json() == {'x': 2.48, 'y': 48.6}


def test_coords_custom_dest_crs_query():
    response = client.get("/coords/convert", params={'x': 2.48, 'y': 48.6, 'dest_crs': 2154})
    assert response.status_code == 200
    assert response.json() == {'x': 661658.0529747768, 'y': 6833437.094585511}


def test_coords_custom_source_crs_query():
    response = client.get("/coords/convert", params={'x': 661658.0529747768, 'y': 6833437.094585511,
                                                     'source_crs': 2154})
    assert response.status_code == 200
    assert response.json() == {'x': 2.4799999999999995, 'y': 48.599999999985734}
