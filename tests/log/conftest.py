import logging

import pytest

from observability_mtl_instrument.log_config import LogConfig, LokiLogHandler


@pytest.fixture
def loki_log_handler() -> LokiLogHandler:
    return LokiLogHandler(
        log_format='%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"',
        service_name='testes',
        loki_url='http://url-test/loki/v1/push',
    )


@pytest.fixture
def log_config() -> LogConfig:
    return LogConfig(
        service_name='testes',
        log_level=logging.DEBUG,
        loki_url='http://url-test/loki/v1/push',
        extra_labels={'first_label': 'first_value'},
    )
