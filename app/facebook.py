import os
import requests

from flask import url_for

from .app import app
from .stats import STATS

BASE_URL = 'https://graph.facebook.com/v2.10/'
ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')

if __name__ == '__main__':
    for stat in STATS.keys():
        with app.app_context():
            url = url_for('stat_details', stat=stat, _external=True)

        r = requests.post(BASE_URL, data={
            'id': url,
            'scrape': True,
            'access_token': ACCESS_TOKEN
        })

        print(r.json())
