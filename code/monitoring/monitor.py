from storage.prometheus import PrometheusMetrics


class CrawlerMonitor(object):

    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.metrics = PrometheusMetrics(f'crawler_item_{spider_name}', ['type'])

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


class ProcessMonitor(object):

    def __init__(self):
        self.metrics = PrometheusMetrics('process_item', ['file_type'])

    def update_count(self, task_type):
        labels = {'file_type': task_type}
        self.metrics.inc(labels)
