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

        self.metrics = {
            'status_http_counter': self.metrics_types['counter'](
                'http_requests_total_by_code',
                'responses total by status code',
                ['http_code', 'unmapped'],
                registry=self.registry
            ),
            'http_request_duration': self.metrics_types['summary'](
                'http_requests_duration_seconds',
                'reponse time of request',
                ['url_path', 'http_method', 'unmapped'],
                registry=self.registry
            ),
            'requests_in_progress': self.metrics_types['gauge'](
                'request_in_progress_total',
                'quantity of requests in progress',
                registry=self.registry
            )
        }

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