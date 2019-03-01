import json
import logging
import os
import sys
from multiprocessing import Process

from flask import Flask, request, Response
from flask_prometheus import monitor
from prometheus_client import CollectorRegistry, multiprocess, generate_latest, CONTENT_TYPE_LATEST
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crawler import settings
from crawler.spiders.jam_en_do import JamEnDoSpider
from crawler.spiders.zk import ZkSpider
from monitoring.config import CONFIG
from processing import handler

os.path.dirname(sys.modules['__main__'].__file__)
os.environ['prometheus_multiproc_dir'] = '/home/arthur264/Documents/music_data/prometheus_dir'
LOGGER_FORMAT = '%(asctime)s %(message)s'
configure_logging(install_root_handler=True)
logging.basicConfig(
    # filename='log.txt',
    format=LOGGER_FORMAT,
    level=logging.INFO,
    datefmt='[%H:%M:%S]',
)

app = Flask(__name__)
app.config.update(CONFIG)


def process_run(crawl, processing, items):
    if crawl:
        project_settings = get_project_settings()
        project_settings.setdict({
            item: getattr(settings, item) for item in dir(settings) if not item.startswith('__')
        })
        process = CrawlerProcess(project_settings)
        for item in items:
            process.crawl(item)

        process.start()

    if processing:
        handler.start()

    return None


@app.route('/start', methods=['POST'])
def start():
    body = json.loads(request.data)
    crawl = body.get('crawl', True)
    processing = body.get('processing', False)
    items = body.get('items', [JamEnDoSpider, ZkSpider])
    sub_process = Process(target=process_run, args=(crawl, processing, items))
    sub_process.start()
    return 'OK'


@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    monitor(app, port=8081)
    app.run(host='0.0.0.0', port=8080)
