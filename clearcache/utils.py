from django.conf import settings
from django.core.cache import caches


def clear_cache(cache_name):
    assert settings.CACHES
    caches[cache_name].clear()


def clear_cache_key(cache_name, cache_key):
    assert settings.CACHES
    return caches[cache_name].delete(cache_key)
