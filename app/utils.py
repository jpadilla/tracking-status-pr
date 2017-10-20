import datetime

from flask import json


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
