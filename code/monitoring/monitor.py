from storage.prometheus import PrometheusMetrics


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

    def update_size(self, spider_name, file_type, size, count):
        data = {'spider_name': spider_name, 'file_type': file_type, 'size': size, 'count': count}
        # db.update(
        #     'file_size',
        #     {'file_type': file_type, 'spider_name': spider_name},
        #     {'$set': data}
        # )


class ProcessMonitor(object):

    def __init__(self):
        self.metrics = PrometheusMetrics('process_item', ['file_type'])

    def update_count(self, task_type):
        labels = {'file_type': task_type}
        self.metrics.inc(labels)
