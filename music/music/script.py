import settings
from scrapy.crawler import CrawlerProcess
from spiders.zk import ZkSpider
from scrapy.utils.project import get_project_settings


if __name__ == "__main__":
    # start_with = None
    # with open('start_with.txt', 'r') as infile:
    #     start_with = int(infile.readline().strip())
    #
    # with open('start_with.txt', 'w+') as the_file:
    #     the_file.write(str(start_with + 50000))

    scrapy_settings = get_project_settings()
    for item in dir(settings):
        if item.startswith("__"):
            continue
        print(item)
        scrapy_settings.setdict({item: getattr(settings, item)})
    process = CrawlerProcess(scrapy_settings)
    process.crawl(ZkSpider)
    process.start()

