import threading

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from database.connect import db
from music import settings
from music.spiders.zk import ZkSpider
from pubsub.pubsub import pub_sub


def main():
    db.delete_db()
    scrapy_settings = get_project_settings()
    for item in dir(settings):
        if item.startswith("__"):
            continue

        scrapy_settings.setdict({item: getattr(settings, item)})

    process = CrawlerProcess(scrapy_settings)
    process.crawl(ZkSpider)
    process.start()


if __name__ == "__main__":
    thread1 = threading.Thread(target=main, args=(pub_sub, ))
    thread2 = threading.Thread(target=func2, args=(num, q))
    thread1.start()
    thread2.start()
