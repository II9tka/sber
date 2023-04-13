from app.models import ValCurs, Valute
from app.services.dataclasses.cbr import ValCursDataClass, ValuteDataClass
from app.utils.db import get_data_from_object_using_dataclass_fields


def val_curs_is_exists(date) -> bool:
    return ValCurs.is_exists(request_date=date)


def valute_is_exists(char_code) -> bool:
    return Valute.is_exists(char_code=char_code)


def create_val_curs(val_curs: ValCursDataClass) -> bool:
    val_curs_obj = ValCurs(
        **get_data_from_object_using_dataclass_fields(val_curs, ValCursDataClass, exclude_fields=('valutes',))
    ).save()

    for valute in val_curs.valutes:
        Valute(**get_data_from_object_using_dataclass_fields(valute, ValuteDataClass), val_curs=val_curs_obj).save()

    return True


def delete_valutes_by_char_code(char_code) -> bool:
    Valute.bulk_delete_by_char_code(char_code)

    return True
