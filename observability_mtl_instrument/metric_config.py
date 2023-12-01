from enum import Enum
from typing import Type

from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    Summary,
    pushadd_to_gateway,
)
from prometheus_client.metrics import Metric


class MetricType(Enum):
    COUNTER = 'counter'
    SUMMARY = 'summary'
    GAUGE = 'gauge'
    HISTOGRAM = 'histogram'

    @property
    def metric_class(self) -> Type:
        return {
            MetricType.COUNTER: Counter,
            MetricType.SUMMARY: Summary,
            MetricType.GAUGE: Gauge,
            MetricType.HISTOGRAM: Histogram,
        }[self]


class MetricConfig:
    def __init__(self, job_name: str, prometheus_url: str) -> None:
        self.registry = CollectorRegistry()
        self.job_name = job_name
        self.prometheus_url = prometheus_url

        self.metrics = {}

        self.add_metric(
            title='http_requests_total_by_code',
            type=MetricType.COUNTER,
            description='responses total by status code',
            labels=['http_code', 'unmapped', 'service'],
        )
        self.add_metric(
            title='http_requests_duration_seconds',
            type=MetricType.SUMMARY,
            description='reponse time of request',
            labels=['url_path', 'http_method', 'unmapped', 'service'],
        )
        self.add_metric(
            title='requests_in_progress',
            type=MetricType.GAUGE,
            description='quantity of requests in progress',
            labels=['service'],
        )

    def add_metric(
        self,
        type: MetricType,
        title: str,
        description: str,
        labels: list[str] = [],
    ):
        metric_class = type.metric_class
        self.metrics[title] = metric_class(
            title, description, labels, registry=self.registry
        )

    def show_metrics(self):
        return self.metrics

    def send_metrics(self):
        pushadd_to_gateway(
            self.prometheus_url, job=self.job_name, registry=self.registry
        )
