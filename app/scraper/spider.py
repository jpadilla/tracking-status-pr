import json

import scrapy

from .utils import strip_accents, is_float, is_int, is_blank


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


def parse_businesses_processing_pan(response):
    for card in response.css('.card'):
        path = card.css(
            'p.text-muted > span::attr(data-i18n)').extract_first()

        if path == 'card.bread.title':
            label = card.css('p.text-muted > span::text').extract_first()
            value = card.css('p.text-muted > span.info::text').extract_first()

            last_updated_text = card.css(
                '.p-small-spacing > .text-muted::text').extract()

            if len(last_updated_text) > 1:
                last_updated = last_updated_text[1]
            else:
                last_updated = None

            return {
                'label': normalize_label(label),
                'path': normalize_path(path),
                'value': normalize_value(value),
                'last_updated_at': normalize_last_updated(last_updated)
            }


CUSTOM_PARSERS = {
    'card.bread.title': parse_businesses_processing_pan
}


def parse(response):
    for card in response.css('.card'):
        label = card.css('p.text-muted > span::text').extract_first()

        path = card.css(
            'p.text-muted > span::attr(data-i18n)').extract_first()

        if is_blank(path):
            path = card.css(
                'p.text-muted::attr(data-i18n)').extract_first()

        if is_blank(path):
            path = card.css(
                '.card-header h2::attr(data-i18n)').extract_first()

        if path in CUSTOM_PARSERS:
            yield CUSTOM_PARSERS[path](response)
            continue

        value = card.css(
            '.font-large-2.text-bold-300.info::text').extract_first()

        if is_blank(path):
            label = card.css('p.text-muted::text').extract_first()

        if is_blank(label):
            label = card.css('p.text-muted::text').extract_first()

        if is_blank(label):
            label = card.css('.card-header h2::text').extract_first()

        if is_blank(label):
            label = card.css('.card-header h3.grey::text').extract_first()

        if is_blank(value):
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


class StatusPRSpider(scrapy.Spider):
    name = 'status-pr'
    start_urls = ['http://estatus.pr/']

    def parse(self, response):
        return parse(response)


class StatusPRJSONSpider(scrapy.Spider):
    name = 'status-pr-json'
    start_urls = ['http://estatus.pr/card-data/card-data.json']

    def parse(self, response):
        stats = json.loads(response.body_as_unicode())
        data = []

        for stat in stats:
            label = stat['Description']
            path = stat['Language']
            card = stat['Card'][0]
            value = card['Value']
            in_percentage = card['ValueIsInPercentage']
            children = stat['CardDefinitionChild']

            if not path and label:
                path = label.lower()

            if not in_percentage:
                value = int(value)

            if len(children) > 0 and value == 0:
                for child in children:
                    child_label = child['Description']
                    child_path = child['Language']
                    child_card = child['CardDetail'][0]
                    child_value = child_card['Value']
                    child_in_percentage = child_card['ValueIsInPercentage']

                    if not child_path and child_label:
                        child_path = '{}.{}'.format(path, child_label.lower())

                    if not child_in_percentage:
                        child_value = int(child_value)

                    data.append({
                        'label': normalize_label(child_label),
                        'path': normalize_path(child_path),
                        'value': child_value
                    })
            else:
                data.append({
                    'label': normalize_label(label),
                    'path': normalize_path(path),
                    'value': value
                })

        return data

