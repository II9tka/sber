import os

from pathlib import Path

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from starlette_core.database import DatabaseURL
from starlette.config import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = Config(os.path.join(BASE_DIR, '.env'))

environ['DATABASE_URL'] = f'sqlite:///{os.path.join(BASE_DIR, "sqlite3.db")}'

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=[])
DATABASE_URL = config("DATABASE_URL", cast=DatabaseURL)
DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=Secret)

CBR_URL = 'http://www.cbr.ru/scripts/XML_daily.asp'

FORMATS = {
    'DATE_FORMAT': '%Y-%m-%d',
    'DATE_CBR_REQUEST_FORMAT': '%d/%m/%Y',
    'DATE_CBR_RESPONSE_FORMAT': '%d.%m.%Y'
}
