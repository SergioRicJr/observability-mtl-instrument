import logging

from pytest import fixture


@fixture
def log_record_with_extra_labels():
    my_record = logging.LogRecord(
        funcionaaquijesus='aloooooooooooooooooo',
        name='observability_config.log_config',
        msg='hello message was sent',
        level=logging.INFO,
        lineno=32,
        args=(),
        levelname='INFO',
        levelno=20,
        pathname='/workspaces/Sergio/fastapi-app/main.py',
        filename='main.py',
        module='main',
        exc_info=None,
        exc_text=None,
        stack_info=None,
        funcName='welcome',
        created=1701711302.0109453,
        msecs=10.0,
        relativeCreated=29161.38529777527,
        thread=139756812891904,
        threadName='AnyIO worker thread',
        processName='SpawnProcess-1',
        process=3406,
    )

    return my_record


@fixture
def stream_dict():
    return {
        'stream': {
            'service': 'application',
            'severity': 'INFO',
            'name': 'observability_config.log_config',
            '1': '1',
            '2': '2',
        }
    }
