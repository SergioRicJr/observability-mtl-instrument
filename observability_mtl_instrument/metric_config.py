from prometheus_client import Counter, CollectorRegistry, Summary, Gauge, Histogram, pushadd_to_gateway
from prometheus_client.metrics import Metric
from typing import Type

class MetricConfig:
    def __init__(self, job_name: str, prometheus_url: str) -> None:
        self.registry = CollectorRegistry()
        self.job_name = job_name
        self.prometheus_url = prometheus_url
    
        self.metrics_types: dict[str, Type[Metric]] = {
            'counter': Counter,
            'summary': Summary,
            'gauge': Gauge,
            'histogram': Histogram
        }

        self.metrics = {}

        self.add_metric(
            title='http_requests_total_by_code',
            type='counter',
            description='responses total by status code',
            labels=['http_code', 'unmapped', 'service']
        )
        self.add_metric(
            title='http_requests_duration_seconds',
            type='summary',
            description='reponse time of request',
            labels=['url_path', 'http_method', 'unmapped', 'service']
        )
        self.add_metric(
            title='requests_in_progress',
            type='gauge',
            description='quantity of requests in progress',
            labels=['service']
        )

    def add_metric(self, type: str, title: str, description: str, labels: list[str] = []):
        self.metrics[title] = self.metrics_types[type](
            title,
            description,
            labels,
            registry=self.registry
        )
    
    def show_metrics(self):
        return self.metrics

    def send_metrics(self):
        pushadd_to_gateway(self.prometheus_url, job=self.job_name, registry=self.registry)