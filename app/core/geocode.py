# -*- coding: utf-8 -*-
import inspect
import functools
import hashlib
import time
import threading
from collections import OrderedDict

from geopy import get_geocoder_for_service

from .geocode_cache import cache_get, cache_set, REDIS_ENABLED


class GeocodeException(Exception):
    pass


MAX_CACHED_SERVICES = 20        # nombre max d'instances de géocodeurs en mémoire
CACHE_TTL_SECONDS = 3600        # expiration après 1h d'inactivité

_lock = threading.Lock()
CACHED_GEOCODER = OrderedDict()  # {(provider, cache, hashed_api_key): (geocode_service, last_used_ts)}


def _hash_api_key(api_key):
    if not api_key:
        return "none"
    return hashlib.sha256(api_key.encode()).hexdigest()[:16]


def _evict_expired_and_lru():
    """Supprime les entrées expirées et applique une politique LRU."""
    now = time.time()

    expired_keys = [
        key for key, (_, last_used) in CACHED_GEOCODER.items()
        if now - last_used > CACHE_TTL_SECONDS
    ]
    for key in expired_keys:
        del CACHED_GEOCODER[key]

    while len(CACHED_GEOCODER) > MAX_CACHED_SERVICES:
        CACHED_GEOCODER.popitem(last=False)


def build_geocode_service(provider, api_key=None, cache=0):
    cache_key = (provider, cache, _hash_api_key(api_key))

    with _lock:
        _evict_expired_and_lru()

        if cache_key in CACHED_GEOCODER:
            geocode_service, _ = CACHED_GEOCODER[cache_key]
            CACHED_GEOCODER.move_to_end(cache_key)
            CACHED_GEOCODER[cache_key] = (geocode_service, time.time())
            return geocode_service

        geocode_service_cls = get_geocoder_for_service(provider)
        geocode_service_args = inspect.signature(geocode_service_cls.__init__)

        if 'api_key' in geocode_service_args.parameters and not api_key:
            raise GeocodeException("Provider {} needs an api key".format(provider))
        elif 'api_key' in geocode_service_args.parameters:
            geocode_service = geocode_service_cls(api_key, user_agent="pygisapi")
        else:
            geocode_service = geocode_service_cls(user_agent="pygisapi")

        if not hasattr(geocode_service.geocode, '__wrapped__'):
            setattr(
                geocode_service,
                'geocode',
                functools.lru_cache(maxsize=cache)(geocode_service.geocode)
            )

        CACHED_GEOCODER[cache_key] = (geocode_service, time.time())
        CACHED_GEOCODER.move_to_end(cache_key)

        return geocode_service


def geocode_with_optional_redis(geocode_service, query, provider, ttl=3600):
    """
    Utilise Redis pour cacher le résultat si REDIS_ENABLED, sinon
    repose uniquement sur le lru_cache déjà attaché à geocode_service.geocode.
    """
    if not REDIS_ENABLED:
        return geocode_service.geocode(query)

    cache_key = f"geocode:{provider}:{hashlib.sha256(query.encode()).hexdigest()}"

    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    result = geocode_service.geocode(query)
    result_dict = None
    if result:
        result_dict = {
            "address": result.address,
            "latitude": result.latitude,
            "longitude": result.longitude,
        }

    cache_set(cache_key, result_dict, ttl=ttl)
    return result_dict