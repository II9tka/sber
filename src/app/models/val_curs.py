import sqlalchemy as sa

from sqlalchemy.orm import relationship

from .bases import Base


class ValCurs(Base):
    __tablename__ = "val_curs"

    id = sa.Column(
        "id", sa.Integer, primary_key=True
    )
    date = sa.Column(
        'date', sa.Date
    )
    request_date = sa.Column(
        'request_date', sa.Date, index=True
    )
    name = sa.Column(
        'name', sa.String
    )
    valutes = relationship(
        'Valute', backref='val_curs', lazy='dynamic'
    )
