from app.endpoints import delete_valutes_by_char_code, list_valutes_unique_char_code, list_val_curs, create_val_curs

from starlette.routing import Route

from app.utils.route import create_route_path

version = 'v1'
valutes = 'valutes'
val_curs = 'val_curs'

routes = [
    Route(
        create_route_path(version, val_curs), list_val_curs, methods=["GET"],
        name="val_curs-list"
    ),
    Route(
        create_route_path(version, valutes, 'delete_by_char_code'), delete_valutes_by_char_code, methods=["POST"],
        name="delete-valute-by-char-code"
    ),
    Route(
        create_route_path(version, val_curs, 'create_val_curs_by_date'), create_val_curs, methods=["POST"],
        name="create-val-curs-by-date"
    ),
    Route(
        create_route_path(version, valutes, 'get_unique_char_codes'), list_valutes_unique_char_code, methods=["GET"],
        name="list-valute-unique-char-codes"
    ),
]
