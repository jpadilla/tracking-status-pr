import os
import time
import datetime
from io import BytesIO

import pymongo
from pytz import timezone
from PIL import Image, ImageDraw, ImageFont
from flask import (Flask, Response, request, redirect, jsonify,
                   render_template, send_file, send_from_directory)

from .stats import STATS
from .utils import JSONEncoder, cached

pr = timezone('America/Puerto_Rico')
utc = timezone('UTC')

app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
app.config['PREFERRED_URL_SCHEME'] = 'http' if app.debug else 'https'
app.config['now'] = int(round(time.time() * 1000))
app.config['version'] = os.getenv('SOURCE_VERSION', app.config['now'])

client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()


@app.before_request
def before_request():
    if not app.debug and not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url)


def get_stats(path=None):
    pipeline = [{'$sort': {'created_at': -1}}]

    if path:
        pipeline.append({'$match': {'path': path}})

    pipeline.append({
        '$group': {
            '_id': '$path',
            'label': {
                '$last': '$label'
            },
            'data': {
                '$push': {
                    'value': '$value',
                    'date': '$created_at'
                }
            }
        }
    })

    return db.stats.aggregate(pipeline)


def process_stats(results):
    paths = []

    for result in results:
        path = result['_id']
        label = result['label']

        # Convert stat date from UTC to PR timezone
        for stat in result['data']:
            stat['date'] = stat['date'].replace(tzinfo=utc).astimezone(pr)

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

        if not stats:
            stats = [last_stat]
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
        else:
            stats = sorted(stats, key=lambda k: k['date'])

            if first_stat['value'] != stats[0]['value']:
                stats.insert(0, first_stat)
            else:
                stats[0] = first_stat

            if last_stat['value'] != stats[-1]['value']:
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
@cached()
def index():
    results = get_stats()
    stats = sorted(process_stats(results), key=lambda k: k['label'])
    return render_template('index.html', stats=stats)


@app.route('/embed/<path>')
def embed(path):
    results = get_stats(path)
    stats = process_stats(results)

    if not stats:
        return redirect('/')

    return render_template('embed.html', stat=stats[0])


@app.route('/stats/<stat>')
def stat_details(stat):
    results = get_stats(stat)
    stats = process_stats(results)

    if not stats:
        return redirect('/')

    return render_template('details.html', stat=stats[0])


@app.route('/stats/<stat>.json')
def stats_json(stat):
    data = []
    stats = db.stats.find({'path': stat}).sort('created_at')

    for stat in stats:
        data.append({'date': stat['created_at'], 'value': stat['value']})

    return jsonify(data)


@app.route('/stats/<stat>.csv')
def stats_csv(stat):
    def generate(stat):
        stats = db.stats.find({'path': stat}).sort('created_at')
        yield f"Date,Value\n"

        for stat in stats:
            created_at = stat['created_at']
            value = stat['value']
            yield f"{created_at},{value}\n"

    return Response(generate(stat), mimetype='text/plain')


@app.route('/stats/<stat>.png')
def stat_image(stat):
    results = get_stats(stat)
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
    draw.text(
        position, stat['last_value'], font=font, align='center', fill='#000')

    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')


@app.route('/digest/<date>')
@app.route('/digest/<date>/<end_date>')
def digest(date, end_date=None):
    created_at = datetime.datetime.strptime(date, '%Y-%m-%d').astimezone(pr)
    created_at = created_at - datetime.timedelta(days=1)
    start_date = created_at + datetime.timedelta(hours=23, minutes=59)

    if not end_date:
        end_date = created_at + datetime.timedelta(
            days=1, hours=23, minutes=59)
    else:
        end_date = datetime.datetime.strptime(end_date,
                                              '%Y-%m-%d').astimezone(pr)
        end_date = end_date + datetime.timedelta(days=1, microseconds=-1)

    date_range = [start_date, end_date]

    results = db.stats.aggregate([{
        '$sort': {
            'created_at': 1
        }
    }, {
        '$match': {
            'created_at': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
    }, {
        '$group': {
            '_id': '$path',
            'first': {
                '$first': '$$ROOT'
            },
            'last': {
                '$last': '$$ROOT'
            }
        }
    }, {
        '$project': {
            '_id': '$_id',
            'first': '$first',
            'last': '$last',
            'change': {
                '$subtract': ['$last.value', '$first.value']
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }])

    data = []

    for result in results:
        path = result['_id']

        if STATS.get(path):
            label = STATS[path]['label']

        if result['change'] > 0:
            sign = '+'
        else:
            sign = ''

        if STATS[path]['percent']:
            percent = '%'
        else:
            percent = ''

        change = '{sign}{change:0.2f}{percent}'.format(
            sign=sign, change=result['change'], percent=percent)

        data.append({
            '_id': path,
            'label': label,
            'first': result['first'],
            'last': result['last'],
            'change': result['change'],
            'display_change': change
        })

    return render_template('digest.html', date_range=date_range, results=data)
