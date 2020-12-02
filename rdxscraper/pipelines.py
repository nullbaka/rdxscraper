from itemadapter import ItemAdapter
import pymongo


class CommonPipeline:
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, collection):
        self.mongodb_server = mongodb_server
        self.mongodb_db = mongodb_db
        self.mongodb_port = mongodb_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_server=crawler.settings.get('MONGODB_SERVER'),
            mongodb_port=crawler.settings.get('MONGODB_PORT'),
            mongodb_db=crawler.settings.get('MONGODB_DB', 'items'),
            collection=crawler.spider.category
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_server, self.mongodb_port)
        self.db = self.client[self.mongodb_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class FirstpostPipeline(CommonPipeline):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, collection):
        super().__init__(mongodb_server, mongodb_port, mongodb_db, collection)
        self.collection_name = "firstpost_"+collection


class ExpressPipeline(CommonPipeline):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, collection):
        super().__init__(mongodb_server, mongodb_port, mongodb_db, collection)
        self.collection_name = "indianexpress_"+collection


class TimesOfIndiaPipeline(CommonPipeline):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, collection):
        super().__init__(mongodb_server, mongodb_port, mongodb_db, collection)
        self.collection_name = "toi_"+collection


class MoneyControlPipeline(CommonPipeline):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, collection):
        super().__init__(mongodb_server, mongodb_port, mongodb_db, collection)
        self.collection_name = "moneycontrol_"+collection
