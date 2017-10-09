import os
import datetime
import unicodedata

import pymongo
import scrapy
from scrapy.crawler import CrawlerProcess


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def normalize_value(value):
    return value.strip()


def normalize_path(path):
    return (
        path
        .strip()
        .replace('card.', '')
        .replace('nav.', '')
        .replace(' ', '.').strip()
    )


def normalize_label(label):
    return strip_accents(label).strip()


class StatusPRSpider(scrapy.Spider):
    name = 'status-pr'
    start_urls = ['http://status.pr/']

    def parse(self, response):
        for card in response.css('.card'):
            label = card.css('p.text-muted > span::text').extract_first()

            path = card.css(
                'p.text-muted > span::attr(data-i18n)').extract_first()

            value = card.css(
                '.font-large-2.text-bold-300.info::text').extract_first()

            if not path:
                label = card.css('p.text-muted::text').extract_first()

            if not label:
                label = card.css('.card-header > h2::text').extract_first()

            if not value:
                value = card.css('.card-header > h3::text').extract_first()

            if not path:
                path = card.css(
                    '.card-header > h2::attr(data-i18n)').extract_first()

            if value:
                if not path:
                    path = label.lower()

                label = normalize_label(label)
                path = normalize_path(path)
                value = normalize_value(value)

                yield {
                    'label': label,
                    'path': path,
                    'value': value
                }


class MongoDBPipeline(object):
    collection_name = 'stats'

    def __init__(self, mongodb_uri):
        self.mongodb_uri = mongodb_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        db = self.client.get_default_database()
        self.collection = db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        document = dict(item)
        document['created_at'] = datetime.datetime.utcnow()
        self.collection.insert_one(document)
        return item


if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_URI': 'stdout:',
        'FEED_FORMAT': 'json',
        'ITEM_PIPELINES': {
            'scraper.MongoDBPipeline': 0
        },
        'MONGODB_URI': os.getenv('MONGODB_URI')
    })
    process.crawl(StatusPRSpider)
    process.start()
