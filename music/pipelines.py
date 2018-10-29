# -*- coding: utf-8 -*-
import os
import io
import time
import logging
from scrapy.exporters import CsvItemExporter


class MusicPipeline(object):
    folder_path = 'results/{}'

    def __init__(self):
        self.current_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.create_folder(self.folder_path.format(self.current_time))
        self.count_artist = 0
        self.file_item = io.open("results/{}/music.csv".format(self.current_time), "wb")
        self.item = CsvItemExporter(self.file_item, encoding="utf-8")
        self.item.start_exporting()
        self.file_artist = io.open("results/{}/artist.csv".format(self.current_time), "wb")
        self.artist = CsvItemExporter(self.file_artist, encoding="utf-8")
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

    @staticmethod
    def create_folder(path):
        try:
            os.makedirs(path)
            logging.info("Created folder " + str(path))
        except OSError:
            if not os.path.isdir(path):
                raise
