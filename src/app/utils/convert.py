from datetime import datetime

from app.settings import FORMATS


def from_str_date_to_datetime(str_date: str, date_format: str = FORMATS['DATE_FORMAT']):
    return datetime.strptime(str_date, date_format)
