from typing import Type, Any

from app.db import Base


def get_data_from_object_using_dataclass_fields(
        obj: Type[Base],
        dataclass,
        exclude_fields: tuple[str, ...] = None
) -> dict[str, Any]:
    """
    :param obj: Type[Base]
    :param dataclass: Type[DataclassClassOrWrapper]
    :param exclude_fields: tuple[str, ...]
    :return: dict[str, Any]

    Is used for to fill up obj (mapped model) using dataclass fields.

    """
    if not exclude_fields:
        exclude_fields = tuple()

    return {key: getattr(obj, key) for key in dataclass.__annotations__ if key not in exclude_fields}
