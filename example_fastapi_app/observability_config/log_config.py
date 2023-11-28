from logging import LogRecord
import datetime
from datetime import timezone
import requests
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from dotenv import load_dotenv
load_dotenv()

class LokiLogHandler(logging.Handler):
    def __init__(self, log_format, service_name, log_function, loki_url, extra_labels):
        super(LokiLogHandler, self).__init__()
        self.formatter = logging.Formatter(log_format)
        self.service_name = service_name
        self.log_function = log_function
        self.loki_url = loki_url
        self.extra_labels: dict = extra_labels

    def emit(self, record):
        log_entry = self.format(record)
        
        extra_log_label = record.__dict__.get('extra_labels')
        if extra_log_label:
            self.extra_labels = self.extra_labels | extra_log_label
        response = self.log_function(record, log_entry, self.service_name, self.loki_url, self.extra_labels)
        return response
    
    
class LogConfig():
    def __init__(
        self,
        service_name: str,
        log_level: int,
        loki_url: str,
        extra_labels={},
        log_format: str = '%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"',
        logger_name = __name__
    ):
        super(LogConfig, self).__init__()
        self.service_name = service_name
        self.log_format = log_format
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.logger.addHandler(
            LokiLogHandler(
                log_format=self.log_format,
                service_name=self.service_name,
                log_function=self.send_logs,
                loki_url=loki_url,
                extra_labels=extra_labels
            )
        )
        LoggingInstrumentor().instrument(set_logging_format=True)

    def get_logger(self):
        return self.logger
    
    def send_logs(self, record, log_entry, job_name, loki_url, *extra_labels):
        headers = {
            'Content-type': 'application/json'
        }
        dt = datetime.datetime.now(timezone.utc) 
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp() 
        timestamp_unix_nanos = int(utc_timestamp * 1e9)

        stream_dict = {
            "stream": {
                "job": job_name,
                "severity": record.levelname,
                "name": record.name
            }
        }
        for label in extra_labels:
            stream_dict['stream'].update(label)

        data = {
            "streams": [
                {
                    **stream_dict, 
                    "values": [
                        [str(timestamp_unix_nanos), log_entry]
                    ]
                }
            ]
        }
        response = requests.post(loki_url, json=data, headers=headers)
        return response