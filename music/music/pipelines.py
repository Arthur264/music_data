# -*- coding: utf-8 -*-
#! /usr/bin/python3
import os
import io
import time
import logging
from scrapy.exporters import CsvItemExporter, JsonItemExporter


class MusicPipeline(object):
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    folder_path = 'music_data/{}'

    def __init__(self):
        self.create_folder(self.folder_path.format(self.current_time))
        self.count_artist = 0
        self.file_item = io.open("music_data/{}/music.json".format(self.current_time), "wb")
        self.item = JsonItemExporter(self.file_item, encoding="utf-8", ensure_ascii=False)
        self.item.start_exporting()
        self.file_artist = io.open("music_data/{}/artist.json".format(self.current_time), "wb")
        self.artist = JsonItemExporter(self.file_artist, encoding="utf-8", ensure_ascii=False)
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
