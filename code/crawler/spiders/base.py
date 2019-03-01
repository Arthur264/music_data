import gc
import logging
from abc import abstractmethod
from urllib.parse import urljoin

import scrapy

from config import TEST_MODE
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
    test_mode = TEST_MODE
    custom_settings = {
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 405, 408, 410],
        'DEFAULT_REQUEST_HEADERS': HEADERS
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitor = CrawlerMonitor(self.name)

    @abstractmethod
    def parse(self, response):
        pass

    def get_url(self, url):
        return urljoin(self.base_url, url)

    @staticmethod
    def gc_clear():
        gc.collect()

    @staticmethod
    def error(response):
        logging.error('Error:', response)
        return True
