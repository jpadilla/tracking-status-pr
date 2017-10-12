import os
import csv
import datetime

import pymongo
from flask import Flask, Response, jsonify, json


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = JSONEncoder
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()


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


def get_stats(path):
    return db.stats.find({'path': path}).sort('created_at')

@app.route('/')
def index():
    pipeline = [{'$group': {'_id': '$path'}}]
    paths = db.stats.aggregate(pipeline)
    data = {}

    for path in paths:
        data[path['_id']] = {
            'json': '/stats/{}.json'.format(path['_id']),
            'csv': '/stats/{}.csv'.format(path['_id'])
        }

    return jsonify({'data': data})


@app.route('/stats/<path>.json')
def stats_json(path):
    data = []

    for stat in get_stats(path):
        data.append({
            'date': stat['created_at'],
            'value': stat['value']
        })

    return jsonify(data)


@app.route('/stats/<path>.csv')
def stats_csv(path):
    writer = csv.DictWriter(Echo(), fieldnames=['date', 'value'])
    writer.writeheader()

    def generate():
        for stat in get_stats(path):
            yield writer.writerow({
                'date': stat['created_at'],
                'value': stat['value']
            })

    return Response(generate(), mimetype='text/csv')
