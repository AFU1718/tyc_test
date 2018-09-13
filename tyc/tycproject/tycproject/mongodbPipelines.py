from scrapy.conf import settings
import pymongo

class MongodbPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(settings['MONGO_HOST'],settings['MONGO_PORT'])
        db = self.connection[settings['MONGO_DB']]
        self.collection = db[settings['MONGO_COLL']]

        # self.connection = pymongo.MongoClient('119.23.241.65',27017)
        # db = self.connection['tyc']
        # self.collection = db[settings['COLLECTION']]

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item