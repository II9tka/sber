from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.settings import config


middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=config.get('SECRET_KEY'),
    )
]
