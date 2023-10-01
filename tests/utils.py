import random
import string

from sqlalchemy.orm import Session

from app.db import crud, models
from app.util import types


def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_int(lower, upper):
    return random.randint(lower, upper)


def random_float(lower, upper):
    return random.uniform(lower, upper)


def create_random_movie_data():
    return {
        'title': random_lower_string(30),
        'id': random_lower_string(10),
        'year': random_int(1990, 2010),
        'runtime': random_int(10, 9999),
        'rating': random_float(1, 10),
        'genres': [types.Genre.Drama, types.Genre.Mystery]  # todo randomize
    }


def create_random_movie(session: Session, save: bool = True) -> models.Movie:
    kwargs = create_random_movie_data()

    # item_in = schemas.MovieCreateDTO(session, **kwargs)
    return crud.create_movie(session, save=save, **kwargs)
