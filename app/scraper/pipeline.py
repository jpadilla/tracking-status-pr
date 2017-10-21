import datetime
import pymongo


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
