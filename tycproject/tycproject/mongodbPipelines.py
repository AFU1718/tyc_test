from scrapy.conf import settings
import pymongo

class MongodbPipeline_Qiye58(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['qiye58']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item

class MongodbPipeline_Youboy(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['youboy']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item

class MongodbPipeline_Shop99114(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['shop99114']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item

class MongodbPipeline_Qiye56ye(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['qiye56ye']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item

class MongodbPipeline_Huangye88(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['huangye88']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item

class MongodbPipeline_B2b168(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['b2b168']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item

class MongodbPipeline_Pe168(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.connection[settings['MONGO_DB']]
        self.collection = self.db['pe168']

    def process_item(self, item,spider):
        self.collection.insert(dict(item))
        return item