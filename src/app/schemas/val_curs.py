from sqlite3 import Date

from pydantic import BaseModel

from app.schemas.valute import ValuteSchema


class ValCursSchema(BaseModel):
    id: int
    date: Date
    request_date: Date
    name: str

    valutes: list[ValuteSchema]
