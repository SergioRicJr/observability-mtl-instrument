import logging
from logging import Logger
from unittest.mock import Mock, patch

from opentelemetry.instrumentation.logging import LoggingInstrumentor

from observability_mtl_instrument.log_config import LogConfig

# from observability_mtl_instrument.log_config import LogConfig


def test_logConfig_must_create_attribute_service_name(log_config):
    assert log_config.service_name == 'testes'


def test_logConfig_must_create_attribute_log_format(log_config):
    assert (
        log_config.log_format
        == '%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"'
    )


@patch('logging.getLogger')
def test_logConfig_must_call_getLogger_with_the_name_of_dir(
    getLogger, log_config
):
    LogConfig(
        service_name='testes',
        log_level=logging.DEBUG,
        loki_url='http://url-test/loki/v1/push',
    )
    getLogger.assert_called_once_with(
        'observability_mtl_instrument.log_config'
    )


# @patch('opentelemetry.instrumentation.logging.LoggingInstrumentor.instrument')
# @patch('observability_mtl_instrument.log_config.LokiLogHandler')
# @patch('observability_mtl_instrument.log_config.LogConfig.logger')
# def test_logConfig_must_call_setLevel_with_logging_debug_level(
#     instrument, loki_handler, logger
# ):
#     loki_handler = Mock()

#     log_config = LogConfig(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#     )

#     # log_config.setLevel.assert_called_once_with(logging.DEBUG)

#     # logger.logger.setLevel.assert_called_once_with(logging.DEBUG)


@patch('opentelemetry.instrumentation.logging.LoggingInstrumentor.instrument')
def test_logConfig_constructor_must_call_LoggingInstrumentor_instrumet(
    logging_instrument: LoggingInstrumentor,
):
    LogConfig(
        service_name='testes',
        log_level=logging.DEBUG,
        loki_url='http://url-test/loki/v1/push',
    )

    logging_instrument.assert_called_once_with(set_logging_format=True)
