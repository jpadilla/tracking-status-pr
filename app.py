import os
import csv
import datetime

import pymongo
from flask import Flask, Response, jsonify, json, request, render_template


CHARTED = {
    'flight': '89e4b8e',
    'aaa': 'db5ef87',
    'goverment.mail': 'e66b520',
    'comercios.procesando.pan': '187f5c3',
    'cooperatives': '63c6544',
    'bank': 'f740a32',
    'container': '298d822',
    'atms': 'eb1da4f',
    'pharmacy': 'b988843',
    'dialysis': '0afa169',
    'ama': '527e337',
    'port': '725a5f8',
    'pet': '47c1167',
    'supermarket': 'bd15b67',
    'gas': '5bcaff6',
    'aee': '1a99347',
    'telecomunication': '12d4d4d',
    'antenna': 'bbda136',
    'shelter': '7390428',
    'refugee': 'dae5290',
    'tower': '53287b4',
    'hospital': 'eabacf5'
}


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


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


def get_stats(path):
    return db.stats.find({'path': path}).sort('created_at')


@app.route('/')
def index():
    paths = db.stats.aggregate([
        {
            '$group': {
                '_id': {'path': '$path', 'label': '$label'}
            }
        }
    ])

    if request_wants_json():
        data = {}

        for path_obj in paths:
            path = path_obj['_id']['path']
            data[path] = {
                'json': '/stats/{}.json'.format(path),
                'csv': '/stats/{}.csv'.format(path)
            }

        return jsonify({'data': data})

    data = []

    for path_obj in paths:
        path = path_obj['_id']['path']
        path_obj['charted'] = CHARTED[path]
        data.append(path_obj)

    return render_template('index.html', paths=data, request_url=request.url)


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
