# import logging
# from logging import Logger
# from unittest.mock import MagicMock, Mock, patch

# from opentelemetry.instrumentation.logging import LoggingInstrumentor


# @patch('logging.getLogger')
# def test_logConfig_must_call_getLogger_with_the_name_of_dir(
#     getLogger, log_config
# ):
#     log_config.__init__(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#     )
#     getLogger.assert_called_once_with(
#         'observability_mtl_instrument.log_config'
#     )


# @patch('logging.getLogger')
# def test_logConfig_must_call_getLogger_with_the_chosen_name(
#     getLogger, log_config
# ):
#     log_config.__init__(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#         logger_name='teste',
#     )
#     getLogger.assert_called_once_with('teste')


# @patch('observability_mtl_instrument.log_config.LogConfig.set_level')
# def test_logConfig_must_call_setLevel_with_logging_debug_level(
#     set_level, log_config
# ):

#     log_config.__init__(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#     )

#     set_level.assert_called_once_with(log_config.get_logger(), logging.DEBUG)


# @patch('opentelemetry.instrumentation.logging.LoggingInstrumentor.instrument')
# def test_logConfig_constructor_must_call_LoggingInstrumentor_instrumet(
#     logging_instrument: LoggingInstrumentor, log_config
# ):
#     log_config.__init__(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#     )

#     logging_instrument.assert_called_once_with(set_logging_format=True)


# @patch('observability_mtl_instrument.log_config.LogConfig.set_handler')
# def test_logConfig_constructor_must_call_add_handler(
#     set_handler: LoggingInstrumentor, log_config
# ):
#     log_config.__init__(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#     )

#     set_handler.assert_called_once()


# @patch('logging.getLogger')
# def test_logConfing_must_call_logger_add_handler_with_loki_log_handler_instance(
#     logger: Logger, log_config
# ):
#     log_config.__init__(
#         service_name='testes',
#         log_level=logging.DEBUG,
#         loki_url='http://url-test/loki/v1/push',
#         logger_name='teste',
#     )

#     logging.getLogger('teste').addHandler.assert_called_once_with(
#         log_config.loki_log_handler
#     )
