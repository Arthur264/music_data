import logging
import os
import sys
from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crawler import settings
from crawler.spiders.jam_en_do import JamEnDoSpider
from crawler.spiders.zk import ZkSpider
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


def main(only_handle):
    if only_handle:
        handler.start()
        return

    project_settings = get_project_settings()
    project_settings.setdict({item: getattr(settings, item) for item in dir(settings) if not item.startswith('__')})
    process = CrawlerProcess(project_settings)
    process.crawl(JamEnDoSpider)
    process.crawl(ZkSpider)
    process.start()

    handler.start()


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--handle', dest='handle', help='only handle', action='store_true')
    parser.set_defaults(handle=False)

    args = parser.parse_args()
    main(args.handle)
