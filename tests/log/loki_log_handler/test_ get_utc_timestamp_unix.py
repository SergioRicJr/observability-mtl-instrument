import datetime
from unittest.mock import MagicMock, patch

import pytest
from utils import str_to_datetime


@pytest.mark.parametrize(
    'timestamp_str, timestamp_unix_nanoseconds',
    [
        ('2015-04-20 19:05:41.788302+00:00', '1429556741788301824'),
        ('2023-12-20 19:05:41.788302+00:00', '1703099141788301824'),
        ('1998-01-25 05:45:11.184302+00:00', '885707111184301952'),
    ],
)
@patch('datetime.datetime')
def test_should_return_the_correct_unix_timestamp_in_nanoseconds(
    mock_datetime: datetime.datetime,
    timestamp_str: str,
    timestamp_unix_nanoseconds: str,
    loki_log_handler,
):
    mocked_timestamp = str_to_datetime(timestamp_str)
    mock_datetime.now.return_value = mocked_timestamp
    log_timestamp_unix_nanoseconds = loki_log_handler.get_utc_timestamp_unix()
    assert log_timestamp_unix_nanoseconds == timestamp_unix_nanoseconds
