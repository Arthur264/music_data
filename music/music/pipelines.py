# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.exporters import JsonItemExporter


class MusicPipeline(object):
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S")

    def __init__(self):
        pass
        # self.file_item = open("music_{}.json".format(self.current_time), 'wb')
        # self.item = JsonItemExporter(self.file_item, encoding='utf-8', ensure_ascii=False)
        # self.item.start_exporting()
        # self.file_artist = open("artist_{}.json".format(self.current_time), 'wb')
        # self.artist = JsonItemExporter(self.file_artist, encoding='utf-8', ensure_ascii=False)
        # self.artist.start_exporting()

    def close_spider(self, spider):
        pass
        # self.item.finish_exporting()
        # self.item.close()
        #
        # self.artist.finish_exporting()
        # self.artist.close()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "MusicItem":
            # self.item.export_item(item)
            log.msg("Item added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        else:
            # self.artist.export_item(item)
            log.msg("Artist added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
        

class MusicMongoPipeline(object):
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
