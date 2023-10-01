# ################################################ #
# Only SQLAlchemy (ORM) models here.               #
# All models in this module are imported in env.py #
# ################################################ #

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import (
    Column,
    String,
    Integer, Float, Enum,
)

from app.db.base import Base, TimestampedMixin
from app.util import types

# todo validations

class Movie(Base, TimestampedMixin):
    """
    Due to data entry/update considerations, the imdb id
    is chosen as the PK (id) here. This is in order to bulk
    update efficiently from imdb tsv data files that use imdb_id
    as their identifier. That implies the assumption the updates will
    happen "often".

    Normally, and in case this project was
    expanded we would use an auto-inc integer as in base.MyBaseModel
    so that lookups and joins were more efficient among other benefits
    """
    id = Column(String(12), primary_key=True)

    title = Column(String(128), index=True)  # there are common titles
    year = Column(Integer, index=True)
    rating = Column(Float, index=True)
    runtime = Column(Integer)  # minutes
    imdb_url = Column(String(512), unique=True, nullable=False)
    genres = Column(pg.ARRAY(Enum(types.Genre, native_enum=False)))  # allow_nulltype=True ?
    # _genres = Column('genres', pg.ARRAY(Enum(types.Genre, native_enum=False)))

    def __repr__(self) -> str:
        return f"<Movie-{self.id}"

    def __str__(self) -> str:
        return self.title

    @property
    def display_title(self):
        if self.year:
            return f"{self.title} ({self.year})"
        else:
            return self.title
