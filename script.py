import logging
import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from database.connect import db
from music import settings
from music.spiders.zk import ZkSpider
from music.spiders.jamendo import JamEnDoSpider
from processing import handler
import config

os.path.dirname(sys.modules['__main__'].__file__)

LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)


def main():
    project_settings = get_project_settings()

    for item in dir(settings):
        if item.startswith("__"):
            continue

        project_settings.setdict({item: getattr(settings, item)})

    process = CrawlerProcess(project_settings)
    process.crawl(JamEnDoSpider)
    process.crawl(ZkSpider)
    process.start()


if __name__ == "__main__":
    if config.DEBUG:
        log.setLevel(logging.DEBUG)
        db.delete_db()

    # handler.run()
    main()
