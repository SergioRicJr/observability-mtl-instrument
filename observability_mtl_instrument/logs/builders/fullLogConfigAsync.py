import logging

from observability_mtl_instrument.logs.builders.fullLogBase import FullLogBase
from observability_mtl_instrument.logs.request_strategies.log_request import (
    LogRequestAsync,
)


class FullLogConfigAsync(FullLogBase):
    """
    Configura logs e realiza o envio ao grafana Loki de forma assíncrona, onde a aplicação não espera o envio dos logs para realizar as demais atividades ou retorno da resposta.

    Parameters:
        service_name: Nome do serviço ou aplicação que está rodando
        loki_url: Url da aplicação Grafana/Loki, que receberá os logs
        logger_name: Nome que será dado ao logger
        log_level: Valor inteiro que representa um nível mínimo para que os logs sejam salvos. Usando a biblioteca logging, ex: logging.DEGUB ou logging.WARNING
        extra_labels: Objeto com labels personalizados que serão aplicados em todos os logs daquela instância
        log_format: Formatação de quais dados integrarão os logs e de que forma
    """

    def __init__(
        self,
        service_name: str,
        loki_url: str,
        logger_name: str = __name__,
        log_level: int = logging.DEBUG,
        extra_labels: {str: str | int | float} | {} = {},
        log_format: str = '%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"',
    ) -> None:
        super().__init__(
            service_name=service_name,
            loki_url=loki_url,
            make_request_class=LogRequestAsync,
            logger_name=logger_name,
            log_level=log_level,
            extra_labels=extra_labels,
            log_format=log_format,
        )
