def test_build_stream_dict_must_add_extra_labels_in_stream(
    log_record_with_extra_labels, loki_log_handler
):
    stream_dict = loki_log_handler.build_stream_dict(
        'application',
        log_record_with_extra_labels,
        extra_labels=({'1': '1'}, {'2': '2'}),
    )

    assert stream_dict == {
        'stream': {
            'service': 'application',
            'severity': 'INFO',
            'name': 'observability_config.log_config',
            '1': '1',
            '2': '2',
        }
    }
