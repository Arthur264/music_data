import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from database.connect import db
from music import settings
from music.spiders.zk import ZkSpider
from processing import handler

os.path.dirname(sys.modules['__main__'].__file__)


def main():
    db.delete_db()
    project_settings = get_project_settings()

    for item in dir(settings):
        if item.startswith("__"):
            continue

        project_settings.setdict({item: getattr(settings, item)})

    process = CrawlerProcess(project_settings)
    process.crawl(ZkSpider)
    process.start()


if __name__ == "__main__":
    handler.run()
