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


def is_float(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


def normalize_value(value):
    if isinstance(value, str):
        value = (
            value
            .strip()
            .replace('%', '')
            .replace(',', '')
        )

    try:
        if is_int(value):
            return int(value)
    except:
        pass

    try:
        if is_float(value):
            return float(value)
    except:
        pass

    return value


def normalize_path(path):
    return (
        path
        .strip()
        .replace('card.', '')
        .replace('nav.', '')
        .replace('.title', '')
        .replace(' ', '.').strip()
    )


def normalize_label(label):
    return strip_accents(label).strip()


def normalize_last_updated(last_updated):
    if last_updated:
        return last_updated.strip().replace(': ', '')


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
                label = card.css('.card-header h2::text').extract_first()

            if not path:
                path = card.css(
                    '.card-header h2::attr(data-i18n)').extract_first()

            if not label:
                label = card.css('.card-header h3.grey::text').extract_first()

            if not value:
                value = card.css('.card-header h3.success::text').extract_first()

            last_updated_text = card.css(
                '.p-small-spacing > .text-muted::text').extract()

            if not last_updated_text:
                last_updated_text = card.css(
                    '.list-inline li .text-muted::text').extract()

            if len(last_updated_text) > 1:
                last_updated = last_updated_text[1]
            else:
                last_updated = None

            if not path and label:
                path = label.lower()

            if not path or not value or not label:
                list_items = card.css('.list-inline li')

                for list_item in list_items:
                    list_item_label = list_item.css('span.info::text').extract_first()
                    list_item_path = list_item.css('span.info::attr(data-i18n)').extract_first()
                    list_item_value = list_item.css('h1::text').extract_first()

                    if not list_item_path and list_item_label:
                        list_item_path = list_item_label.lower()

                    if label and list_item_label:
                        label = normalize_label(label)
                        list_item_label = '{} - {}'.format(label, list_item_label)

                    yield {
                        'label': normalize_label(list_item_label),
                        'path': normalize_path(list_item_path),
                        'value': normalize_value(list_item_value),
                        'last_updated_at': normalize_last_updated(last_updated)
                    }

            if value:
                yield {
                    'label': normalize_label(label),
                    'path': normalize_path(path),
                    'value': normalize_value(value),
                    'last_updated_at': normalize_last_updated(last_updated)
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
        'LOG_ENABLED': True,
        'FEED_URI': 'stdout:',
        'FEED_FORMAT': 'json',
        'ITEM_PIPELINES': {
            'scraper.MongoDBPipeline': 0
        },
        'MONGODB_URI': os.getenv('MONGODB_URI')
    })
    process.crawl(StatusPRSpider)
    process.start()
