from app.db import Base as _Base, db_session


class Base(_Base):
    __abstract__ = True

    def save(self, commit=True):
        db_session.add(self)
        if commit:
            try:
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                raise e
        return self

    @classmethod
    def is_exists(cls, **filters):
        return bool(db_session.query(cls).filter_by(**filters).first())

    @classmethod
    def all(cls, limit=0, offset=0):
        _default = db_session.query(cls)

        if not limit and not offset:
            return _default.all()
        return _default.limit(limit).offset(offset).all()

    @classmethod
    def count(cls):
        return db_session.query(cls).count()

