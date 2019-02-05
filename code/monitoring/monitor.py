from storage.prometheus import PrometheusMetrics, PrometheusGaugeMetrics


class CrawlerMonitor(object):

    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.metrics = PrometheusMetrics('crawler_item', ['spider_name', 'type'])

    def update_artist_count(self):
        self.metrics.inc({
            'spider_name': self.spider_name,
            'type': 'artist',
        })

    def update_song_count(self):
        self.metrics.inc({
            'spider_name': self.spider_name,
            'type': 'song',
        })


class FileMonitor(object):

    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.metrics = PrometheusGaugeMetrics('file_item', ['spider_name', 'type'])

    def update_file_size(self, file_type, file_size):
        labels = {
            'spider_name': self.spider_name,
            'type': file_type,
        }
        self.metrics.update(labels, file_size)


class ProcessMonitor(object):

    def __init__(self):
        self.metrics = PrometheusMetrics('process_item', ['file_type'])

    def update_count(self, task_type):
        labels = {'file_type': task_type}
        self.metrics.inc(labels)
