import os
import datetime
from functools import wraps

import pylibmc
from flask import json, request
from werkzeug.contrib.cache import SimpleCache
from werkzeug.contrib.cache import MemcachedCache

try:
    mc = pylibmc.Client(
        servers=[os.getenv('MEMCACHEDCLOUD_SERVERS')],
        username=os.getenv('MEMCACHEDCLOUD_USERNAME'),
        password=os.getenv('MEMCACHEDCLOUD_PASSWORD')
    )

    cache = MemcachedCache(mc)
except Exception:
    cache = SimpleCache()


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        return json.JSONEncoder.default(self, obj)


# https://docs.djangoproject.com/en/1.8/howto/outputting-csv/
class Echo(object):
    """
    An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """
        Write the value by returning it, instead of storing
        in a buffer.
        """
        return value


# http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
def cached(timeout=5 * 60, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv

        return decorated_function

    return decorator
