# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
from itemadapter import ItemAdapter
from datetime import datetime, timedelta


class AlonhadatComVnPipeline:

    collection_name = 'RawAlonhadat.com.vn'

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
            item.setdefault(field, ['---'])
            if field != 'image':
                item[field] = item[field][0]

        item['postedTime'] = item['postedTime'].replace(
            'Ngày đăng:', '').strip()

        if (item['postedTime'] == 'Hôm nay'):
            item['postedTime'] = datetime.today().strftime("%d/%m/%Y")

        if (item['postedTime'] == 'Hôm qua'):
            item['postedTime'] = (
                datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")

        if (item['square'] != 'UNKNOW' and item['square'] != ''):
            item['square'] = float(item['square'].replace('m', '').replace(
                ',', '*').replace('.', ',').replace('*', '.'))

        if ('tỷ' in item['price'].lower()):
            item['price'] = float(item['price'].split(
                ' ')[0].strip().replace(',', '.')) * 1000
        elif 'triệu/' in item['price'].lower().strip():
            item['price'] = float(item['price'].split(
                ' ')[0].strip().replace(',', '.')) * float(item['square'])
        else:
            item['price'] = float(item['price'].split(' ')[0].strip())

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
