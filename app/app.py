import os
import csv
import time
from io import BytesIO

import pymongo
from PIL import Image, ImageDraw, ImageFont
from flask import (
    Flask, Response, request, redirect, jsonify,
    render_template, send_file, send_from_directory
)

from .stats import STATS
from .utils import JSONEncoder, Echo


app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
app.config['PREFERRED_URL_SCHEME'] = 'http' if app.debug else 'https'
app.config['version'] = os.getenv(
    'SOURCE_VERSION', int(round(time.time() * 1000))
)

client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()


@app.before_request
def before_request():
    if not app.debug and not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url)


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

        if STATS.get(path):
            label = STATS[path]['label']

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

        last_stat = stats[-1]
        formatted_value = "{:,}".format(last_stat['value'])

        if STATS[path]['percent']:
            formatted_value = '{}%'.format(formatted_value)

        paths.append({
            '_id': path,
            'slug': path.replace('.', '-'),
            'label': label,
            'data': data,
            'graph_data': stats,
            'last_value': formatted_value
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
def stat_details(stat):
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


@app.route('/stats/<stat>.json')
def stats_json(stat):
    data = []

    for stat in get_stats(stat):
        data.append({
            'date': stat['created_at'],
            'value': stat['value']
        })

    return jsonify(data)


@app.route('/stats/<stat>.csv')
def stats_csv(stat):
    writer = csv.DictWriter(Echo(), fieldnames=['date', 'value'])
    writer.writeheader()

    def generate(stat):
        for stat in get_stats(stat):
            yield writer.writerow({
                'date': stat['created_at'],
                'value': stat['value']
            })

    return Response(generate(stat), mimetype='text/csv')


@app.route('/stats/<stat>.png')
def stat_image(stat):
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

    stat = stats[0]
    width = 1200
    height = 630
    image = Image.open('./app/static/share-template.png', 'r')
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('./fonts/SourceCodePro-Bold.otf', 100)
    text_width, text_height = draw.textsize(stat['label'], font=font)
    position = ((width - text_width) / 2, (height - text_height - 400) / 2)
    draw.text(position, stat['label'], font=font, align='center', fill='#000')

    font = ImageFont.truetype('./fonts/SourceCodePro-Regular.otf', 80)
    text_width, text_height = draw.textsize(stat['last_value'], font=font)
    position = ((width - text_width) / 2, (height - text_height) / 2)
    draw.text(position, stat['last_value'], font=font, align='center', fill='#000')

    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')
