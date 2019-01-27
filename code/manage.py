import logging
import os
import sys
from multiprocessing import Process

from flask import Flask, request
from flask_prometheus import monitor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crawler import settings
from crawler.spiders.jam_en_do import JamEnDoSpider
from monitoring.config import CONFIG
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

app = Flask(__name__)
app.config.update(CONFIG)


def process_run(handle, processing, items):
    if processing:
        project_settings = get_project_settings()
        project_settings.setdict({
            item: getattr(settings, item) for item in dir(settings) if not item.startswith('__')
        })
        process = CrawlerProcess(project_settings)
        for item in items:
            process.crawl(item)

        process.start()

    if handle:
        handler.start()

    return None


@app.route('/start', methods=['POST'])
def start():
    body = request.data or {}
    handle = body.get('handle', True)
    processing = body.get('processing', True)
    items = body.get('items', [JamEnDoSpider])
    thread = Process(target=process_run, args=(handle, processing, items))
    thread.start()
    return 'OK'


if __name__ == '__main__':
    monitor(app, port=8081)
    app.run(host='0.0.0.0', port=8080)
