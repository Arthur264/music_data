# -*- coding: utf-8 -*-
#! /usr/bin/python3
import time
import logging
from scrapy.exporters import CsvItemExporter


class MusicPipeline(object):
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S")

    def __init__(self):
        self.count_artist = 0
        self.file_item = open("music_data/music_{}.csv".format(self.current_time), 'wb')
        self.item = CsvItemExporter(self.file_item, encoding='utf-8')
        self.item.start_exporting()
        self.file_artist = open("music_data/artist_{}.csv".format(self.current_time), 'wb')
        self.artist = CsvItemExporter(self.file_artist, encoding='utf-8')
        self.artist.start_exporting()

    def close_spider(self, spider):
        self.item.finish_exporting()
        self.file_item.close()

        self.artist.finish_exporting()
        self.file_artist.close()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "MusicItem":
            self.item.export_item(item)
        else:
            self.count_artist += 1
            logging.info("Artist added " + str(self.count_artist))
            self.artist.export_item(item)
        return item
