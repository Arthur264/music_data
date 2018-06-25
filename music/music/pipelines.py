# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MusicPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.item = db[settings['MONGODB_COLLECTION_ITEM']]
        self.artict = db[settings['MONGODB_COLLECTION_ARTICT']]
            
    def close_spider(self, spider):
            self.connection.close()
            
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            if item.__class__.__name__ == "MusicItem":
                self.item.insert(dict(item))
                log.msg("Item added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
            else:
                self.artict.insert(dict(item))
                log.msg("Artist added to MongoDB database!",
                        level=log.DEBUG, spider=spider)
        return item

