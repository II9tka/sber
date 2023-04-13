from app.services.db_services import val_curs_is_exists, valute_is_exists
from .convert import from_str_date_to_datetime


def validate_date(value: str) -> str:
    errors = []

    if not value:
        errors.append('Date field cannot be empty.')

    try:
        from_str_date_to_datetime(value)

        if val_curs_is_exists(value):
            errors.append(f'ValCurs already created for {value}.')
    except ValueError:
        errors.append('Date field has wrong format.')

    if errors:
        raise ValueError(errors)

    return value


def validate_char_code(value: str) -> str:
    errors = []

    if not value:
        errors.append('CharCode field cannot be empty.')
    else:
        if not valute_is_exists(value):
            errors.append('Valutes by CharCode does not exists.')

    if errors:
        raise ValueError(errors)

    return value
