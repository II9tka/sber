from pydantic import BaseModel


class ValuteSchema(BaseModel):
    id: int
    alter_id: str
    char_code: str
    num_code: int
    nominal: int
    name: str
    value: str
    val_curs_id: int
