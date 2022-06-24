# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from itemadapter import ItemAdapter
from datetime import datetime, timedelta


class AlomuabannhadatVnPipeline:
    collection_name = 'RawAlomuabannhadat.vn'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print(item['image'])
        if (item['square'] != 'UNKNOW' and item['square'] != ''):
            item['square'] = float(
                item['square'].replace('m2', '').replace(',', '.'))

        if ('tỷ' in item['price'].lower() and 'triệu' in item['price'].lower()):
            item['price'] = float(item['price'].split(
                'tỷ')[0].strip()) * 1000 + float(item['price'].split(
                    'tỷ')[1].replace('triệu', '').strip())
        elif 'tỷ' in item['price'].lower():
            item['price'] = float(item['price'].replace('tỷ', '').strip())*1000
        else:
            item['price'] = float(item['price'].replace('triệu').strip())

        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())

        return item
