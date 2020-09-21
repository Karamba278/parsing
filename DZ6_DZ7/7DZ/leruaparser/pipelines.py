# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.avito_photo_kittens

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
       if item['photo']:
           for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item


