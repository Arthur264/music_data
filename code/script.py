import logging
import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from code import config
from code.database.connect import db
from code.music import settings
from code.music.spiders.jamendo import JamEnDoSpider
from code.music.spiders.zk import ZkSpider
from code.processing import handler

os.path.dirname(sys.modules['__main__'].__file__)

LOGGER_FORMAT = '%(asctime)s %(message)s'
configure_logging(install_root_handler=True)
logging.basicConfig(
    filename='log.txt',
    format=LOGGER_FORMAT,
    level=logging.ERROR,
    datefmt='[%H:%M:%S]',
)


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
    handler.run()


if __name__ == "__main__":
    if config.DEBUG:
        db.delete_db()

    main()
