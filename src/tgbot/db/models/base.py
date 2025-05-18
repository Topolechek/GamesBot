from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase

convention = {
    "ix": "ix__%(column_0_label)s",
    "uq": "uq__%(table_name)s_%(column_0_name)s",
    "ck": "ck__%(table_name)s_%(constraint_name)s",
    "fk": "fk__%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
DeclarativeBase = declarative_base(cls=RepresentableBase, metadata=metadata)


class Base(DeclarativeBase):
    __abstract__ = True

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
