import gc
import logging
import os
from abc import abstractmethod
from urllib.parse import urljoin

import psutil
import scrapy

from monitoring.monitor import CrawlerMonitor

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'User-Agent': USER_AGENT,
}


class BaseSpider(scrapy.Spider):
    base_url = None
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': HEADERS
    }

    def __init__(self, *args, **kwargs):
        self.monitor = CrawlerMonitor()
        self.memory_usage()
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
