# -*- coding: utf-8 -*-
import io
import logging
import os
import time

from fs import filesize
from scrapy.exporters import CsvItemExporter

from database.connect import db


class MusicPipeline(object):
    folder_path = 'results/{}'

    def __init__(self):
        self.current_time = time.strftime('%Y_%m_%d_%H_%M_%S')
        self.create_folder(self.folder_path.format(self.current_time))
        self.count_artist = 0
        self.file_music_name = 'results/{}/music.csv'.format(self.current_time)
        self.file_item = io.open(self.file_music_name, 'wb')
        self.item = CsvItemExporter(self.file_item, encoding='utf-8')
        self.item.start_exporting()
        self.file_artist_name = 'results/{}/artist.csv'.format(self.current_time)
        self.file_artist = io.open(self.file_artist_name, 'wb')
        self.artist = CsvItemExporter(self.file_artist, encoding='utf-8')
        self.artist.start_exporting()
        db.insert('file_size', [{'file_type': 'song', 'size': 0}, {'file_type': 'artist', 'size': 0}])

    def close_spider(self, spider):
        self.item.finish_exporting()
        self.file_item.close()

        self.artist.finish_exporting()
        self.file_artist.close()

    def process_item(self, item, spider):
        if item.__class__.__name__ == 'MusicItem':
            self.item.export_item(item)
            db.update(
                'file_size',
                {'file_type': 'song'},
                {'$set': {'file_type': 'song', 'size': self.get_file_size(self.file_music_name)}}
            )
        else:
            self.count_artist += 1
            logging.info('Artist added ' + str(self.count_artist))
            self.artist.export_item(item)
            db.update(
                'file_size',
                {'file_type': 'artist'},
                {'$set': {'file_type': 'artist', 'size': self.get_file_size(self.file_artist_name)}}
            )
        return item

    @staticmethod
    def create_folder(path):
        try:
            os.makedirs(path)
            logging.info('Created folder ' + str(path))
        except OSError:
            if not os.path.isdir(path):
                raise

    @staticmethod
    def get_file_size(file_name):
        return filesize.traditional(os.path.getsize(os.path.abspath(file_name)))
