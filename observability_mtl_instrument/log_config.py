import datetime
import logging
from datetime import timezone
from logging import Logger, LogRecord

import requests
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from requests import Response


class LokiLogHandler(logging.Handler):
    def __init__(
        self,
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
        response = requests.post(loki_url, json=data, headers=headers)
        return response

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

    def __init__(
        self,
        service_name: str,
        log_level: int,
        loki_url: str,
        extra_labels: {str: str | int | float} | {} = {},
        log_format: str = '%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"',
        logger_name=__name__,
    ):
        super(LogConfig, self).__init__()
        self.service_name = service_name
        self.log_format = log_format
        self.loki_url = loki_url
        self.extra_labels = extra_labels
        self.loki_log_handler = LokiLogHandler(
            log_format=self.log_format,
            service_name=self.service_name,
            loki_url=self.loki_url,
            extra_labels=self.extra_labels,
        )
        self.logger = logging.getLogger(logger_name)
        self.set_level(self.logger, log_level)
        self.set_handler()
        LoggingInstrumentor().instrument(set_logging_format=True)

    def set_handler(self):
        self.logger.addHandler(self.loki_log_handler)

    def set_level(self, logger, level):
        logger.setLevel(level)

    def get_logger(self) -> Logger:
        return self.logger
