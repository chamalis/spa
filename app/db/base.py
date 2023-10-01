from typing import Generator

from sqlalchemy import Column, MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_mixin, declarative_base
from sqlalchemy.types import (
    Integer,
    DateTime
)

from app.db import util


@declarative_mixin
class MyBaseModel:
    """Used as a base class for our models (ORM Classes) to inherit"""
    @declared_attr
    def __tablename__(cls):  # noqa
        """By default name the db table by class name lowercase"""
        return cls.__name__.lower()

    # not used in this project cause bulk updates happen via imdb id
    # id = Column(Integer, primary_key=True, index=True)


class TimestampedMixin:
    """A Mixin providing automated created/updated functionality"""
    # lots of entries in this project, save a column
    # time_created = Column(
    #     DateTime,
    #     server_default=util.UtcNow(),
    #     nullable=False)
    time_updated = Column(
        DateTime,
        server_default=util.UtcNow(),
        onupdate=util.UtcNow(),
        nullable=False)


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
# Construct an sqlalchemy base class for declarative class definitions.
# using our own defined MyBaseModel base class
Base = declarative_base(cls=MyBaseModel, metadata=metadata)


# session factory
SessionLocalFact = util.create_sess_factory()


# Dependency
def get_db_sess() -> Generator:
    """
    Uses SQLalchemy's connection pool to assign a new
    connection to each request handler that performs DB ops,
    assuming each requestis calling this function to get a db handler
    """
    sess = SessionLocalFact()
    try:
        # yield ensures the close() happens AFTER the request handler
        yield sess
    finally:
        sess.close()
