from observability_mtl_instrument.logs.log_config import (
    LogConfig,
    LokiLogHandler,
)


class FullLogBase:
    def __init__(
        self,
        service_name: str,
        loki_url: str,
        make_request_class,
        logger_name: str,
        log_level: int,
        extra_labels: {str: str | int | float} | {},
        log_format: str,
    ) -> None:
        self.log_config = LogConfig()
        self.set_attributes(
            make_request_class,
            logger_name,
            extra_labels,
            service_name,
            log_format,
            loki_url,
        )
        self.log_config.set_level(log_level)
        self.set_loki_handler()
        self.log_config.instrument_log()

    def get_log_config(self):
        return self.log_config

    def set_attributes(
        self,
        make_request_class,
        logger_name,
        extra_labels,
        service_name,
        log_format,
        loki_url,
    ):
        self.log_config.make_request_class = make_request_class
        self.log_config.logger = logger_name
        self.log_config.extra_labels = extra_labels
        self.log_config.service_name = service_name
        self.log_config.log_format = log_format
        self.log_config.loki_url = loki_url

    def set_loki_handler(self):

        self.log_config.loki_log_handler = LokiLogHandler(
            instance=self.log_config.make_request_class,
            log_format=self.log_config.log_format,
            service_name=self.log_config.service_name,
            loki_url=self.log_config.loki_url,
            extra_labels=self.log_config.extra_labels,
        )
        self.log_config.set_handler()
