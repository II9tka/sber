import sqlalchemy as sa

from sqlalchemy.orm import load_only

from .bases import Base
from ..db import db_session


class Valute(Base):
    __tablename__ = "valute"

    id = sa.Column(
        "id", sa.Integer, primary_key=True
    )
    alter_id = sa.Column(
        'alter_id', sa.String
    )
    char_code = sa.Column(
        "char_code", sa.String, index=True
    )
    num_code = sa.Column(
        "num_code", sa.Integer
    )
    nominal = sa.Column(
        "nominal", sa.Integer
    )
    name = sa.Column(
        "name", sa.String
    )
    value = sa.Column(
        "value", sa.DECIMAL(10, 4)
    )  # Yes, I know it's not supported in sqlite3
    val_curs_id = sa.Column(
        'val_curs_id',
        sa.Integer,
        sa.ForeignKey('val_curs.id')
    )

    @classmethod
    def bulk_delete_by_char_code(cls, char_code):
        query = cls.__table__.delete().where(cls.char_code == char_code)
        db_session.execute(query)
        db_session.commit()
        return True

    @classmethod
    def get_unique_by_char_code(cls):
        return db_session.query(cls).options(load_only('char_code')).distinct(cls.char_code).group_by(cls.char_code)
