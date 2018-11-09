import io
import logging
import os
import time

from fs import filesize
from scrapy.exporters import CsvItemExporter

import config
from database.connect import db
from monitoring.monitor import CrawlerMonitor
from music.items import MusicItem


class MusicPipeline(object):
    folder_path = 'results'
    current_time = None
    count_artist = 0
    count_song = 0
    file_music_name = None
    file_music = None
    music = None
    file_artist_name = None
    file_artist = None
    artist = None
    is_start_export = False

    def __init__(self):
        self.monitor = CrawlerMonitor()

    def start_export(self, spider_name):
        self.current_time = time.strftime('%m_%d_%H_%M')
        folder_name = f'{spider_name}_{self.current_time}'
        self.create_folder(folder_name)

        self.file_music_name = os.path.join(self.folder_path, folder_name, 'music.csv')
        self.file_music = io.open(self.file_music_name, 'wb')
        self.music = CsvItemExporter(self.file_music, encoding='utf-8')
        self.music.start_exporting()

        self.file_artist_name = os.path.join(self.folder_path, folder_name, 'artist.csv')
        self.file_artist = io.open(self.file_artist_name, 'wb')
        self.artist = CsvItemExporter(self.file_artist, encoding='utf-8')
        self.artist.start_exporting()

        db.insert('file_size', [
            {'file_type': 'song', 'size': 0, 'count': 0},
            {'file_type': 'artist', 'size': 0, 'count': 0}
        ])
        self.is_start_export = True

    def close_spider(self, spider):
        self.music.finish_exporting()
        self.file_music.close()
        file_music_size = self.get_file_size(self.file_music_name)
        self.monitor.update_size(spider.name, 'song', file_music_size, self.count_song)

        self.artist.finish_exporting()
        self.file_artist.close()
        file_artist_size = self.get_file_size(self.file_artist_name)
        self.monitor.update_size(spider.name, 'artist', file_artist_size, self.count_artist)

    def process_item(self, item, spider):
        if not self.is_start_export:
            self.start_export(spider.name)

        if isinstance(item, MusicItem):
            self.music.export_item(item)
            self.count_song += 1
            if self.count_song % config.COUNT_EMIT_ITEMS == 0:
                file_size = self.get_file_size(self.file_music_name)
                self.monitor.update_size(spider.name, 'song', file_size, self.count_song)
        else:
            self.count_artist += 1
            logging.info(f'Artist added {self.count_artist}')
            self.artist.export_item(item)

            file_size = self.get_file_size(self.file_artist_name)
            self.monitor.update_size(spider.name, 'artist', file_size, self.count_artist)

        return item

    def create_folder(self, folder_name):
        path = os.path.join(self.folder_path, folder_name)
        try:
            os.makedirs(path)
            logging.info(f'Created folder {path}')
        except OSError:
            if not os.path.isdir(path):
                raise

    @staticmethod
    def get_file_size(file_name):
        return filesize.traditional(os.path.getsize(os.path.abspath(file_name)))
