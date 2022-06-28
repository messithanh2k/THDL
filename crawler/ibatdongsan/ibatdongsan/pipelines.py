# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
from itemadapter import ItemAdapter
from datetime import datetime, timedelta


class IbatdongsanComPipeline:
    collection_name = 'RawI-batdongsan.com'

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
        for field in item.fields:
            item.setdefault(field, '---')

        item['postedTime'] = item['postedTime'].replace(
            'Ngày đăng:', '').strip()

        if (item['postedTime'] == 'Hôm nay'):
            item['postedTime'] = datetime.today().strftime("%d/%m/%Y")

        if (item['postedTime'] == 'Hôm qua'):
            item['postedTime'] = (
                datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")

        if item['direction'] == '_':
            item['direction'] = '---'

        if item['dinningRoom'] != '---':
            item['dinningRoom'] = 1

        if item['kitchen'] != '---':
            item['kitchen'] = 1

        if item['rooftop'] != '---':
            item['rooftop'] = 1

        if item['garage'] != '---':
            item['garage'] = 1

        if item['proprietor'] != '---':
            item['proprietor'] = 1

        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())

        return item
