# -*- coding: utf-8 -*-
import os
import json
import logging

logger = logging.getLogger(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "0")

_redis_client = None
REDIS_ENABLED = False

if REDIS_HOST:
    try:
        import redis

        _redis_client = redis.Redis(
            host=REDIS_HOST,
            port=int(REDIS_PORT),
            db=int(REDIS_DB),
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        # Vérifie que la connexion fonctionne réellement
        _redis_client.ping()
        REDIS_ENABLED = True
        logger.info("Redis cache activé (%s:%s/%s)", REDIS_HOST, REDIS_PORT, REDIS_DB)
    except Exception as e:
        logger.warning(
            "REDIS_HOST défini mais connexion impossible (%s). "
            "Fallback sur le cache en mémoire.", e
        )
        _redis_client = None
        REDIS_ENABLED = False
else:
    logger.info("REDIS_HOST non défini. Utilisation du cache en mémoire (comportement par défaut).")


def cache_get(key: str):
    if not REDIS_ENABLED:
        return None
    try:
        val = _redis_client.get(key)
        return json.loads(val) if val else None
    except Exception as e:
        logger.warning("Erreur lecture Redis (%s), fallback silencieux.", e)
        return None


def cache_set(key: str, value, ttl: int = 3600):
    if not REDIS_ENABLED:
        return
    try:
        _redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.warning("Erreur écriture Redis (%s), ignorée.", e)