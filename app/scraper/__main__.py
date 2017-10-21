import os

from scrapy.crawler import CrawlerProcess

from .spider import StatusPRSpider


if __name__ == '__main__':
    process = CrawlerProcess({
        'LOG_ENABLED': True,
        'FEED_URI': 'stdout:',
        'FEED_FORMAT': 'json',
        'ITEM_PIPELINES': {
            'app.scraper.pipeline.MongoDBPipeline': 0
        },
        'MONGODB_URI': os.getenv('MONGODB_URI')
    })
    process.crawl(StatusPRSpider)
    process.start()
