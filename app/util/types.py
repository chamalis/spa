import logging
from enum import Enum
from typing import Iterable, Optional


class UserRole(Enum):
    ADMIN = 'A'
    USER = 'U'


class Genre(Enum):
    Drama = 'Drama'
    Mystery = 'Mystery'
    War = 'War'
    Short = 'Short'
    Documentary = 'Documentary'
    Action = 'Action'
    Reality = 'Reality-TV'
    Romance = 'Romance'
    Comedy = 'Comedy'
    Music = 'Music'
    Scifi = 'Sci-Fi'
    Fantasy = 'Fantasy'
    Adventure = 'Adventure'
    Horror = 'Horror'
    Biography = 'Biography'
    Family = 'Family'
    Thriller = 'Thriller'
    Crime = 'Crime'
    Western = 'Western'
    Adult = 'Adult'
    History = 'History'
    Sport = 'Sport'
    Animation = 'Animation'
    Musical = 'Musical'
    FilmNoir = 'Film-Noir'
    News = 'News'
    TalkShow = 'Talk-Show'
    GameShow = 'Game-Show'

    @classmethod
    def get(cls, value: str):
        if value:
            try:
                return cls(value)
            except ValueError:
                logging.error(f'Unknown Genre: {value}')

    @classmethod
    def from_list(cls, value: Iterable):
        if value:
            return [cls.get(v) for v in value]

    @classmethod
    def list_from_str(cls, values: str):
        if values:
            return cls.from_list(values.split(','))

