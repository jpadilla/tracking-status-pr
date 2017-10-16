import os
import csv

import pymongo
from flask import Flask, Response, jsonify, render_template

from .utils import JSONEncoder, Echo, request_wants_json


app = Flask(__name__)
app.json_encoder = JSONEncoder
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()


def get_stats(path):
    return db.stats.find({'path': path}).sort('created_at')


@app.route('/')
def index():
    paths = []
    results = db.stats.aggregate([
        {
            '$sort': {
                'created_at': -1
            }
        },
        {
            '$group': {
                '_id': '$path',
                'label': {'$last': '$label'}
            }
        }
    ])

    for result in results:
        path = result['_id']

        paths.append({
            '_id': path,
            'slug': path.replace('.', '-'),
            'label': result['label'],
            'json_url': '/stats/{}.json'.format(path),
            'csv_url': '/stats/{}.csv'.format(path)
        })

    if request_wants_json():
        data = {}

        for path in paths:
            data[path['_id']] = {
                'json_url': path['json'],
                'csv_url': path['csv']
            }

        return jsonify({'data': data})

    return render_template('index.html', paths=list(paths))


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
