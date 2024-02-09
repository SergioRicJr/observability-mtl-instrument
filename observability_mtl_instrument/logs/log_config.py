import datetime
import logging
from datetime import timezone
from logging import Logger, LogRecord
from typing import Type

from opentelemetry.instrumentation.logging import LoggingInstrumentor
from requests import Response

from observability_mtl_instrument.logs.request_strategies.log_request_interface import (
    LogRequestInterface,
)


class LokiLogHandler(logging.Handler):
    def __init__(
        self,
        instance: Type[LogRequestInterface],
        log_format: str,
        service_name: str,
        loki_url: str,
        extra_labels: {str: str | int | float} | {} = {},
    ):
        super(LokiLogHandler, self).__init__()
        self.formatter = logging.Formatter(log_format)
        self.service_name = service_name
        self.loki_url = loki_url
        self.extra_labels = extra_labels
        self.tasks = []
        self.instance = instance

    def get_utc_timestamp_unix(self) -> str:
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        timestamp_unix_nanos = int(utc_timestamp * 1e9)
        timestamp_unix_nanos_str = str(timestamp_unix_nanos)
        return timestamp_unix_nanos_str

    def build_stream_dict(
        self, service_name: str, record: LogRecord, extra_labels: dict
    ) -> dict[str, dict[str, str]]:
        stream_dict = {
            'stream': {
                'service': service_name,
                'severity': record.levelname,
                'name': record.name,
            }
        }
        for label in extra_labels:
            stream_dict['stream'].update(label)

        return stream_dict

    def build_loki_log_data(
        self, stream_dict: dict, timestamp_unix_nanos_str: str, log_entry: str
    ) -> dict:
        data = {
            'streams': [
                {
                    **stream_dict,
                    'values': [[timestamp_unix_nanos_str, log_entry]],
                }
            ]
        }
        return data

    def make_request(
        self, instance: LogRequestInterface, loki_url, data, headers
    ):
        instance = instance(loki_url, data, headers)
        instance.make_request()

    def send_logs(
        self,
        record,
        log_entry,
        job_name,
        loki_url,
        timestamp_unix_nanos_str,
        *extra_labels
    ) -> Response:
        headers = {'Content-type': 'application/json'}

        stream_dict = self.build_stream_dict(job_name, record, extra_labels)
        data = self.build_loki_log_data(
            stream_dict, timestamp_unix_nanos_str, log_entry
        )
        self.make_request(self.instance, loki_url, data, headers)

    def build_extra_labels(self, record: LogRecord) -> dict:
        extra_log_label = record.__dict__.get('extra_labels')
        if extra_log_label:
            self.extra_labels = self.extra_labels | extra_log_label
        return self.extra_labels

    def emit(self, record: LogRecord):
        log_entry = self.format(record)
        timestamp_unix_nanos_str = self.get_utc_timestamp_unix()
        self.extra_labels = self.build_extra_labels(record)
        response = self.send_logs(
            record,
            log_entry,
            self.service_name,
            self.loki_url,
            timestamp_unix_nanos_str,
            self.extra_labels,
        )

        return response


class LogConfig:
    """
    Configura logs e realiza o envio ao grafana Loki.

    Parameters:
        service_name: Nome do serviço ou aplicação que está rodando
        log_level: Valor inteiro que representa um nível mínimo para que os logs sejam salvos. Usando a biblioteca logging, ex: logging.DEGUB ou logging.WARNING
        loki_url: Url da aplicação Grafana/Loki, que receberá os logs
        extra_labels: Objeto com labels personalizados que serão aplicados em todos os logs daquela instância
        log_format: Formatação de quais dados integrarão os logs e de que forma
        logger_name: Nome que será dado ao logger
    """

    @property
    def service_name(self):
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        self._service_name = service_name

    @property
    def log_format(self):
        return self._log_format

    @log_format.setter
    def log_format(self, log_format):
        self._log_format = log_format

    @property
    def loki_url(self):
        return self._loki_url

    @loki_url.setter
    def loki_url(self, loki_url):
        self._loki_url = loki_url

    @property
    def extra_labels(self):
        return self._extra_labels

    @extra_labels.setter
    def extra_labels(self, extra_labels):
        self._extra_labels = extra_labels

    @property
    def make_request_class(self):
        return self._make_request_class

    @make_request_class.setter
    def make_request_class(self, make_request_class):
        self._make_request_class = make_request_class

    @property
    def loki_log_handler(self):
        return self._loki_log_handler

    @loki_log_handler.setter
    def loki_log_handler(self, loki_log_handler: LokiLogHandler):
        self._loki_log_handler = loki_log_handler

    @property
    def logger(self) -> Logger:
        return self._logger

    @logger.setter
    def logger(self, logger_name) -> None:
        self._logger = logging.getLogger(logger_name)

    @property
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    def logger_name(self, logger_name):
        self._logger_name = logger_name

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        self._log_level = log_level

    def set_handler(self):
        self._logger.addHandler(self.loki_log_handler)

    def set_level(self, level: int):
        self._logger.setLevel(level)

    def instrument_log(self):
        LoggingInstrumentor().instrument(set_logging_format=True)

    def get_logger(self) -> Logger:
        return self._logger
