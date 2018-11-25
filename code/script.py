import logging
import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import config
from database.connect import db
from music import settings
from music.spiders.jamendo import JamEnDoSpider
from music.spiders.zk import ZkSpider
from processing import handler

os.path.dirname(sys.modules['__main__'].__file__)

LOGGER_FORMAT = '%(asctime)s %(message)s'
configure_logging(install_root_handler=True)
logging.basicConfig(
    filename='log.txt',
    format=LOGGER_FORMAT,
    level=logging.INFO,
    datefmt='[%H:%M:%S]',
)


def main():
    project_settings = get_project_settings()
    project_settings.setdict({item: getattr(settings, item) for item in dir(settings) if not item.startswith('__')})

    process = CrawlerProcess(project_settings)
    process.crawl(JamEnDoSpider)
    process.crawl(ZkSpider)
    process.start()

    handler.start()


if __name__ == "__main__":
    if config.DEBUG:
        db.delete_db()

    main()
