from prometheus_client import Counter


class PrometheusMetrics(object):

    def __init__(self, metrics_name, points):
        self.metrics = Counter(metrics_name, '...', points)

    def inc(self, labels, count=1):
        return self.metrics.labels(**labels).inc(count)
