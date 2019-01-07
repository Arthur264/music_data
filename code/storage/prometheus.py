from prometheus_client import Counter


class PrometheusMetrics(object):

    def __init__(self, metrics_name):
        self.metrics_name = metrics_name
