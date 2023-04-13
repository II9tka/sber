from app.db import create, database
from app.routes import routes
from app.middlewares import middleware
from app.settings import config

from starlette.applications import Starlette

app = Starlette(
    debug=config.get('DEBUG'),
    routes=routes,
    middleware=middleware
)


@app.on_event('startup')
async def on_startup():
    create()

    await database.connect()


@app.on_event('shutdown')
async def on_shutdown():
    await database.disconnect()
