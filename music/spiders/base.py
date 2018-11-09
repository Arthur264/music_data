import gc
import logging
import os
from abc import abstractmethod
from urllib.parse import urljoin

import psutil
import scrapy

from monitoring.monitor import CrawlerMonitor


class BaseSpider(scrapy.Spider):
    base_url = None

    def __init__(self, *args, **kwargs):
        self.monitor = CrawlerMonitor()
        super().__init__(*args, **kwargs)

    @abstractmethod
    def parse(self, response):
        pass

    def memory_usage(self):
        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / float(2 ** 20)
        self.monitor.update_memory(self.name, mem)
        return mem

    def get_url(self, url):
        return urljoin(self.base_url, url)

    @staticmethod
    def gc_clear():
        gc.collect()

    @staticmethod
    def error(response):
        logging.error('Error:', response)
        return True
