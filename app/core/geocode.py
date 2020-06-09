import inspect
import functools

from geopy import get_geocoder_for_service


class GeocodeException(Exception):
    pass


CACHED_GEOCODER = {}


def build_geocode_service(provider, api_key=None, cache=0):
    if (provider, cache) in CACHED_GEOCODER:
        return CACHED_GEOCODER[(provider, cache)]

    for cache_key in list(CACHED_GEOCODER):
        if cache_key[0] == provider:
            del CACHED_GEOCODER[cache_key]

    geocode_service_cls = get_geocoder_for_service(provider)

    geocode_service_args = inspect.signature(geocode_service_cls.__init__)

    if 'api_key' in geocode_service_args.parameters and not api_key:
        raise GeocodeException("Provider {} needs an api key".format(provider))
    elif 'api_key' in geocode_service_args.parameters:
        geocode_service = geocode_service_cls(api_key, user_agent="pygisapi")
    else:
        geocode_service = geocode_service_cls(user_agent="pygisapi")

    if not hasattr(geocode_service.geocode, '__wrapped__'):
        setattr(geocode_service, 'geocode', functools.lru_cache(maxsize=cache)(geocode_service.geocode))

    CACHED_GEOCODER[(provider, cache)] = geocode_service

    return geocode_service
