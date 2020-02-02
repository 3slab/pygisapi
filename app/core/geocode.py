import inspect

from geopy import get_geocoder_for_service
from geopy.exc import GeocoderServiceError


class GeocodeException(Exception):
    pass


def build_geocode_service(provider, api_key=None):
    geocode_service_cls = get_geocoder_for_service(provider)

    geocode_service_args = inspect.signature(geocode_service_cls.__init__)

    if 'api_key' in geocode_service_args.parameters and not api_key:
        raise GeocodeException("Provider {} needs an api key".format(provider))
    elif 'api_key' in geocode_service_args.parameters:
        geocode_service = geocode_service_cls(api_key)
    else:
        geocode_service = geocode_service_cls()

    return geocode_service
