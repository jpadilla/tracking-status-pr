import os
import csv

import pymongo
from flask import (
    Flask, Response, jsonify, render_template, send_from_directory
)

from .utils import JSONEncoder, Echo


app = Flask(__name__)
app.json_encoder = JSONEncoder
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()


STATS_EXTRA = {
   'gas': {
       'label': 'Gas Stations',
       'percent': True
   },
   'supermarket': {
       'label': 'Supermarket',
       'percent': True
   },
   'aee': {
       'label':  'AEE',
       'percent': True
    },
   'telecomunication': {
       'label':  'Telecomm. Services',
       'percent': True
    },
   'aaa': {
       'label':  'AAA',
       'percent': True
    },
   'antenna': {
       'label':  'Cell Phone Antennas',
       'percent': True
    },
   'port': {
       'label':  'Open Ports',
       'percent': True
    },
   'goverment.mail': {
       'label':  'Postal Offices',
       'percent': True
    },
   'ama': {
       'label':  'AMA Routes',
       'percent': True
    },
   'tourism.hotels': {
       'label':  'Tourism / Hotels',
       'percent': True
    },
   'complaint': {
       'label':  'Complaints',
       'percent': False
    },
   'pet': {
       'label':  'Displaced Pets',
       'percent': False
    },
   'barrel.diesel': {
       'label':  'Diesel Barrels Supplied',
       'percent': False
    },
   'flight': {
       'label':  'Comercial Flights',
       'percent': True
    },
   'casinos': {
       'label':  'Tourism / Casinos',
       'percent': True
    },
   'cooperatives': {
       'label':  'Cooperatives',
       'percent': False
    },
   'refugee': {
       'label':  'Shelterees',
       'percent': False
    },
   'shelter': {
       'label':  'Shelters',
       'percent': False
    },
   'milk-industry': {
       'label':  'Milk Industry',
       'percent': True
    },
   'atms': {
       'label':  'ATMs',
       'percent': False
    },
   'pharmacy': {
       'label':  'Online Processing Pharmacies',
       'percent': False
    },
   'container': {
       'label':  'Containers',
       'percent': False
    },
   'comercios.procesando.pan': {
       'label':  'Businesses Processing PAN',
       'percent': False
    },
   'bank': {
       'label':  'Bank Branches',
       'percent': False
    },
   'barrel.gas': {
       'label':  'Gasoline Barrels Supplied',
       'percent': False
    },
   'dialysis': {
       'label':  'Assisted Dialysis Centers',
       'percent': False
    },
   'hospital': {
       'label':  'Assisted Hospitals',
       'percent': False
    },
   'tower': {
       'label':  'Cell Towers',
       'percent': True
    }
}


def get_stats(path):
    return db.stats.find({'path': path}).sort('created_at')


@app.route('/favicon.ico')
def favicon():
    directory = os.path.join(app.root_path, 'static')
    return send_from_directory(directory, 'favicon.ico')


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
                'label': {'$last': '$label'},
                'data': {
                    '$push': {
                        'value': '$value',
                        'date': '$created_at'
                    }
                }
            }
        }
    ])

    for result in results:
        path = result['_id']
        label = result['label']
        stats = [result['data'][0]]
        prev = None

        if STATS_EXTRA.get(path):
            label = STATS_EXTRA[path]['label']

        for stat in result['data'][1:-1]:
            if stat['value'] != prev:
                stats.append(stat)

            prev = stat['value']

        stats.append(result['data'][-1])

        paths.append({
            '_id': path,
            'slug': path.replace('.', '-'),
            'label': label,
            'data': stats,
            'percent': STATS_EXTRA[path]['percent'],
            'json_url': '/stats/{}.json'.format(path),
            'csv_url': '/stats/{}.csv'.format(path)
        })

    paths = sorted(paths, key=lambda k: k['label'])

    return render_template('index.html', paths=paths)


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
