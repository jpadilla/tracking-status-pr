import os
import csv

import pymongo
from flask import (
    Flask, Response, request, redirect, jsonify,
    render_template, send_from_directory
)

from .utils import JSONEncoder, Echo


app = Flask(__name__)
app.json_encoder = JSONEncoder
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()


@app.before_request
def before_request():
    if not app.debug and not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url)


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


def process_stats(results):
    paths = []

    for result in results:
        path = result['_id']
        label = result['label']
        data = sorted(result['data'], key=lambda k: k['date'], reverse=True)
        first_stat = data[-1]
        last_stat = data[0]
        stats = []
        prev_value = None

        if STATS_EXTRA.get(path):
            label = STATS_EXTRA[path]['label']

        for stat in data[1:-1]:
            if stat['value'] != prev_value:
                stats.append(stat)

            prev_value = stat['value']

        if first_stat['value'] != stats[-1]['value']:
            stats.insert(0, first_stat)
        else:
            stats[0] = first_stat

        if last_stat['value'] != stats[0]['value']:
            stats.append(last_stat)
        else:
            stats[-1] = last_stat

        # This prevents graphs with just one point
        if len(stats) == 1:
            stats = [first_stat, last_stat]

        paths.append({
            '_id': path,
            'slug': path.replace('.', '-'),
            'label': label,
            'data': data,
            'graph_data': stats,
            'percent': STATS_EXTRA[path]['percent'],
            'json_url': '/stats/{}.json'.format(path),
            'csv_url': '/stats/{}.csv'.format(path)
        })

    return paths

@app.route('/favicon.ico')
def favicon():
    directory = os.path.join(app.root_path, 'static')
    return send_from_directory(directory, 'favicon.ico')


@app.route('/embed.js')
def embed_js():
    directory = os.path.join(app.root_path, 'static', 'js')
    return send_from_directory(directory, 'embed.js')


@app.route('/')
def index():
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

    stats = sorted(process_stats(results), key=lambda k: k['label'])
    return render_template('index.html', stats=stats)


@app.route('/embed/<path>')
def embed(path):
    results = db.stats.aggregate([
        {
            '$match': {
                'path': path
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

    stats = process_stats(results)

    if not stats:
        return redirect('/')

    return render_template('embed.html', stat=stats[0])


@app.route('/stats/<stat>')
def stats_details(stat):
    results = db.stats.aggregate([
        {
            '$match': {
                'path': stat
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

    stats = process_stats(results)

    if not stats:
        return redirect('/')

    return render_template('details.html', stat=stats[0])


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
