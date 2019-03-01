import io
import logging
import os
import time

from scrapy.exporters import CsvItemExporter

from config import COUNT_EMIT_ITEMS
from crawler.items import MusicItem
from monitoring.monitor import FileMonitor


class MusicPipeline(object):
    folder_path = 'results'
    current_time = None
    file_crawler_name = None
    file_crawler = None
    crawler = None
    file_artist_name = None
    file_artist = None
    artist = None
    is_start_export = False
    monitor = None
    counter = 0
    spider_name = None

    def start_export(self, spider_name):
        self.spider_name = spider_name
        self.current_time = time.strftime('%m_%d_%H_%M')
        folder_name = f'{spider_name}_{self.current_time}'
        self.create_folder(folder_name)

        self.monitor = FileMonitor(spider_name)

        self.file_crawler_name = os.path.join(self.folder_path, folder_name, 'crawler.csv')
        self.file_crawler = io.open(self.file_crawler_name, 'wb')
        self.crawler = CsvItemExporter(self.file_crawler, encoding='utf-8')
        self.crawler.start_exporting()

        self.file_artist_name = os.path.join(self.folder_path, folder_name, 'artist.csv')
        self.file_artist = io.open(self.file_artist_name, 'wb')
        self.artist = CsvItemExporter(self.file_artist, encoding='utf-8')
        self.artist.start_exporting()

        self.is_start_export = True

    def close_spider(self, _):
        self.crawler.finish_exporting()
        self.file_crawler.close()
        self.metrics_update('crawler', self.file_crawler_name)

        self.artist.finish_exporting()
        self.file_artist.close()
        self.metrics_update('artist', self.file_artist_name)
        logging.info(f'Spider close: {self.spider_name}')

    def process_item(self, item, spider):
        if not self.is_start_export:
            self.start_export(spider.name)

        param = {}
        if isinstance(item, MusicItem):
            self.crawler.export_item(item)
            param.update({
                'name': 'crawler',
                'file': self.file_crawler_name
            })
        else:
            self.artist.export_item(item)
            param.update({
                'name': 'artist',
                'file': self.file_artist_name
            })

        if self.counter and not self.counter % COUNT_EMIT_ITEMS:
            self.metrics_update(**param)
            self.counter = 0
        else:
            self.counter += 1
        return item

    def metrics_update(self, name, file):
        file_size = self.get_file_size(file)
        self.monitor.update_file_size(name, file_size)

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
        return os.path.getsize(os.path.abspath(file_name)) >> 20
