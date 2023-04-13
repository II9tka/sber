import json

from pydantic import BaseModel
from typing import Type, Any

from sqlalchemy.orm import Query
from starlette.requests import Request

from app.db import Base


def _construct_data(
        objects: Type[Base],
        schema_class: Type[BaseModel],
        fields: tuple[str, ...] = None,
        sub_serialize=None
):
    if fields is not None:
        return [
            {field: getattr(obj, field) for field in fields} for obj in objects
        ]

    result = []

    for obj in objects:
        fields = {key: getattr(obj, key) for key in schema_class.__annotations__}

        if sub_serialize is not None:
            fields.update(
                {s['field']: _construct_data(getattr(obj, s['field']).all(), s['schema_class']) for s in sub_serialize}
            )

        result.append(json.loads(schema_class(**fields).json()))
    return result


def simple_rest_paginator(
        request: Request,
        model_class: Type[Base],
        schema_class: Type[BaseModel],
        page_size: int = 50,
        fields: tuple[str, ...] = None,
        query: Query = None,
        sub_serialize: tuple[dict[str, Any]] = None
):
    """
    :param request: Request
    :param model_class: Type[Base]
    :param schema_class: Type[BaseModel]
    :param page_size: int
    :param fields: tuple[str, ...]
    :param query: Query. For serialize specify queries, for example with ONLY or specify filters.
    :param sub_serialize: tuple[dict[str, Any]]. For serialize reversed FK or M2M (relationships) objects.
                                                 For example: ({"field": "valutes", "schema_class": SomeSchemeClass})
    :return:
    """
    page_number = request.query_params.get("page", 1)

    if isinstance(page_number, str):
        if page_number.isdigit():
            page_number = int(page_number)
        else:
            page_number = 1

    if page_number <= 0:
        page_number = 1

    offset = 0 if page_number == 1 else page_size * (page_number - 1)
    count = query.count() if query is not None else model_class.count()
    _offset = offset or count
    max_page = count // page_size + 1 if bool(count % _offset) else 0
    request_url = str(request.url).replace(f"?{request.query_params}", '')

    if query:
        objects = query.offset(offset).limit(page_size).all()
    else:
        objects = model_class.all(offset=offset, limit=page_size)

    if count < offset and page_number != max_page:
        prev_page = max_page
    else:
        prev_page = page_number - 1

    return {
        'count': count,
        'prev_page': request_url + f'?page={prev_page}' if page_number > 1 and count >= 1 else '',
        'next_page': request_url + f'?page={page_number + 1}' if count > (offset + page_size) else '',
        'data': _construct_data(objects, schema_class, fields=fields, sub_serialize=sub_serialize)
    }
