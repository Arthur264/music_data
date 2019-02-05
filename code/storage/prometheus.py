from prometheus_client import Counter, Gauge


class PrometheusMetrics(object):

    def __init__(self, metrics_name, points):
        self.metrics = Counter(metrics_name, '...', points)

    def inc(self, labels, count=1):
        return self.metrics.labels(**labels).inc(count)


class PrometheusGaugeMetrics(object):

    def __init__(self, metrics_name, points):
        self.metrics = Gauge(metrics_name, '...', points)

    def update(self, labels, value):
        return self.metrics.labels(**labels).set(value)
