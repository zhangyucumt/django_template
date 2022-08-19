import re
import functools
import pickle
from django.core.cache import caches


def save_result_to_cache(key, expire, cache_backend='default'):
    def deco(missing_func):
        @functools.wraps(missing_func)
        def wrapper(*args, **kwargs):
            cache_key = key
            if re.search(r'{\w*}', key):
                cache_key = key.format(*args, **kwargs)
            cache = caches[cache_backend]
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return pickle.loads(cached_value)
            else:
                v = missing_func(*args, **kwargs)
                cache.set(cache_key, pickle.dumps(v), expire)
                return v

        return wrapper

    return deco
