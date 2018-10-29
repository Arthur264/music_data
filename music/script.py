from music import settings
from scrapy.crawler import CrawlerProcess
from music.spiders.zk import ZkSpider
from scrapy.utils.project import get_project_settings


if __name__ == "__main__":
    scrapy_settings = get_project_settings()
    for item in dir(settings):
        if item.startswith("__"):
            continue

        scrapy_settings.setdict({item: getattr(settings, item)})

    process = CrawlerProcess(scrapy_settings)
    process.crawl(ZkSpider)
    process.start()

