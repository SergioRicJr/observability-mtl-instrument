from datetime import datetime


def str_to_datetime(timestamp):
    str_timestamp_format = '%Y-%m-%d %H:%M:%S.%f%z'
    datetime_timestamp = datetime.strptime(timestamp, str_timestamp_format)
    return datetime_timestamp
