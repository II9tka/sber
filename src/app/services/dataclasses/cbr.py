from datetime import datetime
from decimal import Decimal

from pydantic.dataclasses import dataclass


@dataclass
class ValuteDataClass:
    alter_id: str
    num_code: int
    char_code: str
    nominal: int
    name: str
    value: Decimal


@dataclass
class ValCursDataClass:
    request_date: datetime
    date: datetime
    name: str

    valutes: list[ValuteDataClass]
