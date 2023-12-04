from unittest.mock import MagicMock, patch


def test_build_extra_label_function_must_add_in_extra_label_attribute_off_loki_log_handler(
    loki_log_handler, log_record_with_extra_labels
):
    log_record_with_extra_labels.__dict__ = (
        log_record_with_extra_labels.__dict__
        | {'extra_labels': {'foo': 'bar', 'john': 'doe'}}
    )

    loki_log_handler.extra_labels == {}
    loki_log_handler.build_extra_labels(log_record_with_extra_labels)
    assert loki_log_handler.extra_labels == {'foo': 'bar', 'john': 'doe'}


@patch('observability_mtl_instrument.log_config.LokiLogHandler.send_logs')
def test_build_extra_label_function_must_be_called_when_logger_was_called(
    send_logs, log_config
):
    loki_handler = log_config.loki_log_handler

    MagicMock(wraps=loki_handler.build_extra_labels)

    logger = log_config.get_logger()

    logger.info(
        'hello world, first message',
        extra={'extra_labels': {'foo': 'bar', 'second_label': 'second_value'}},
    )

    assert loki_handler.extra_labels == {
        'first_label': 'first_value',
        'foo': 'bar',
        'second_label': 'second_value',
    }
