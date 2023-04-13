from starlette.requests import Request
from starlette.responses import JSONResponse

from app.models import Valute, ValCurs
from app.schemas import ValuteSchema, ValCursSchema
from app.services.request_services import get_cbr
from app.services.db_services import (
    create_val_curs as _create_val_curs,
    delete_valutes_by_char_code as _delete_valutes_by_char_code,
)
from app.utils.pagination import simple_rest_paginator
from app.utils.validation import validate_date, validate_char_code


async def list_val_curs(request: Request):
    return JSONResponse(simple_rest_paginator(
        request,
        ValCurs,
        ValCursSchema,
        sub_serialize=({'field': 'valutes', 'schema_class': ValuteSchema},),
        page_size=20
    ))


async def delete_valutes_by_char_code(request: Request):
    data = await request.json()

    try:
        char_code = validate_char_code(data.get('char_code'))
    except ValueError as e:
        return JSONResponse({
            'status': 400,
            'success': False,
            'errors': e.args[0]
        }, status_code=400)

    _delete_valutes_by_char_code(char_code)

    return JSONResponse({
        'status': 204,
        'success': True,
        'errors': []
    }, status_code=200)


async def list_valutes_unique_char_code(request: Request):
    return JSONResponse(
        simple_rest_paginator(
            request, Valute, ValuteSchema, fields=('char_code',),
            query=Valute.get_unique_by_char_code()
        )
    )


async def create_val_curs(request: Request):
    data = await request.json()

    try:
        date = validate_date(data.get('date'))
    except ValueError as e:
        return JSONResponse({
            'status': 400,
            'success': False,
            'errors': e.args[0]
        }, status_code=400)

    response = await get_cbr(date)

    if response.has_errors:
        return JSONResponse({
            'status': 500,
            'success': False,
            'errors': ['CBR service not available.']
        }, status_code=500)

    _create_val_curs(response.val_curs)

    return JSONResponse({
        'status': 201,
        'success': True,
        'errors': []
    }, status_code=201)
