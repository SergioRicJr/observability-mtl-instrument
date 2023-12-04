def test_logConfig_must_create_attribute_service_name(log_config):
    assert log_config.service_name == 'testes'


def test_logConfig_must_create_attribute_log_format(log_config):
    assert (
        log_config.log_format
        == '%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"'
    )