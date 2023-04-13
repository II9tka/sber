from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

from databases import Database

from app.settings import config

DATABASE_URL = config.get('DATABASE_URL')

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def create():
    if not database_exists(DATABASE_URL):
        create_database(engine.url)
        Base.metadata.create_all(bind=engine)
