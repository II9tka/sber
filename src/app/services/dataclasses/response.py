from pydantic.dataclasses import dataclass

from app.services.dataclasses.cbr import ValCursDataClass


@dataclass
class Response:
    val_curs: ValCursDataClass | None = None
    has_errors: bool = False
    errors: str = ''
