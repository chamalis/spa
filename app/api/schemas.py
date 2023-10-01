"""
Request / Response Models aka DTOs
"""
from typing import List

from pydantic import BaseModel, Field, root_validator

from app.util import types


class MovieBase(BaseModel):
    genres: List[types.Genre] | None
    year: int | None
    rating: float | None
    runtime: int | None  # minutes


class MovieDTO(MovieBase):
    """ Response Model """
    id: str = Field(alias='imdb_id')  # id -> serialized: imdb_id
    title: str | None
    imdb_url: str
    # time_updated: datetime.datetime

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class MovieCreateDTO(MovieBase):
    """Request Model"""
    id: str | None = Field(alias='imdb_id')  # imdb_id -> deserialized:id
    imdb_url: str | None
    title: str

    @root_validator()
    def check_id_or_url(cls, values):
        if values.get('id') is None and values.get("imdb_url") is None:
            raise ValueError('either imdb_id or imdb_url is required')
        return values
