# -*- coding: utf-8 -*-
import pytest

from . import client, app
from app.api.geocode import build_geocode_service, GeocoderQueryError


def test_geocode_without_query():
    response = client.get("/geocode/nominatim")
    assert response.status_code == 422
    assert response.json() == {"detail": [{"loc": ["query", "q"], "msg":"field required",
                                           "type":"value_error.missing"}]}


def test_geocode_unknown_provider():
    response = client.get("/geocode/unknown", params={'q': '38 rue du président wilson 78230 le pecq'})
    assert response.status_code == 400
    assert response.json() == {'detail': "Unknown geocoder 'unknown'; options are: dict_keys(['arcgis', 'azure', "
                                         "'baidu', 'banfrance', 'bing', 'databc', 'geocodeearth', 'geocodefarm', "
                                         "'geonames', 'google', 'googlev3', 'geolake', 'here', 'ignfrance', 'mapbox', "
                                         "'opencage', 'openmapquest', 'pickpoint', 'nominatim', 'pelias', 'photon', "
                                         "'liveaddress', 'tomtom', 'what3words', 'yandex'])"}


def test_geocode_provider_with_api_key():
    response = client.get("/geocode/bing", params={'q': '38 rue du président wilson 78230 le pecq'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Provider bing needs an api key'}


class FakeGeocodeResponse(object):
    address = "38, Rue du Président Wilson, Le Pecq, Saint-Germain-en-Laye, Yvelines, " \
              "Île-de-France, France métropolitaine, 78230, France"
    latitude = 48.8905833
    longitude = 2.1140494
    raw = {"place_id": 16859956, "osm_type": "node", "osm_id": 1604987399}


class FakeGeocodeService(object):
    def geocode(self, query):
        if query == 'pere noel, pole nord':
            raise GeocoderQueryError('Unable to locate the address : "pere noel, pole nord"')
        else:
            return FakeGeocodeResponse()


def override_build_geocode_service(provider: str, api_key: str = None):
    return FakeGeocodeService()


@pytest.fixture(scope="session")
def override_geocode_depends():
    app.dependency_overrides[build_geocode_service] = override_build_geocode_service
    yield None
    app.dependency_overrides = {}


def test_geocode_provider_address_not_found(override_geocode_depends):
    response = client.get("/geocode/nominatim", params={'q': 'pere noel, pole nord'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Unable to locate the address : "pere noel, pole nord"'}


def test_geocode_provider_success(override_geocode_depends):
    response = client.get("/geocode/nominatim", params={'q': '38 rue du président wilson 78230 le pecq'})
    assert response.status_code == 200
    assert response.json() == {"address": "38, Rue du Président Wilson, Le Pecq, Saint-Germain-en-Laye, Yvelines, "
                                          "Île-de-France, France métropolitaine, 78230, France",
                               "lat": 48.8905833,
                               "lng": 2.1140494,
                               "raw": {"place_id": 16859956, "osm_type": "node", "osm_id": 1604987399}}
