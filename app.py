import os
import csv

import pymongo
from flask import Flask, Response


app = Flask(__name__)
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


@app.route('/stats/<path>.csv')
def stats(path):
    writer = csv.DictWriter(Echo(), fieldnames=['date', 'value'])
    writer.writeheader()

    def generate():
        stats = db.stats.find({
            'path': path
        })

        for stat in stats:
            yield writer.writerow({
                'date': stat['created_at'],
                'value': stat['value']
            })

    return Response(generate(), mimetype='text/csv')
