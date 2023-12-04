from logging import Formatter
from unittest.mock import patch

@patch('logging.Formatter.formatTime')
def test_build_loki_log_data_must_create_correct_data(
    format, log_record_with_extra_labels, stream_dict, loki_log_handler
):
    format.return_value = '2023-12-04 17:49:37,547'

    log_record_with_extra_labels.__dict__ = (
        log_record_with_extra_labels.__dict__
        | {
            'otelSpanID': 'f4e865e0e89d2822',
            'otelTraceID': '8fe805c363235f6da2475405fa8dfe81',
            'otelTraceSampled': True,
            'otelServiceName': 'fastapi-module',
        }
    )

    loki_log_data = loki_log_handler.build_loki_log_data(
        stream_dict,
        '1703099141788301824',
        loki_log_handler.format(log_record_with_extra_labels),
    )

    assert loki_log_data == {'streams': [{'stream': {'service': 'application', 'severity': 'INFO', 'name': 'observability_config.log_config', '1': '1', '2': '2'}, 'values': [['1703099141788301824', '2023-12-04 17:49:37,547 levelname=INFO name=observability_config.log_config file=main.py:32 trace_id=8fe805c363235f6da2475405fa8dfe81 span_id=f4e865e0e89d2822 resource.service.name=fastapi-module trace_sampled=True - message="hello message was sent"']]}]}
