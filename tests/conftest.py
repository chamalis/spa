from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db import crud
from app.db.base import SessionLocalFact
from app.main import app
from app.util import types
from . import utils as testutils
from .utils import random_int


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocalFact()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='function')
def random_movie(db) -> Generator:
    """
    Create random movie, pass over the execution to the test
    function and clean up the db at the end

    @param db: An SQLALchemy Session
    @return: A models.Movie generator
    """
    movie = testutils.create_random_movie(db, save=True)
    yield movie

    # now cleanup aka: delete the movie
    crud.delete_movie(db, movie)


@pytest.fixture(scope='function')
def random_movie_unsaved(db) -> Generator:
    """
    Create random movie data, pass over the execution to the test
    function which will eventually create the movie and clean up
    the db at the end

    @param db: An SQLALchemy Session
    @return: A models.Movie generator
    """
    movie = testutils.create_random_movie(db, save=False)
    yield movie

    # now cleanup aka: delete the movie
    crud.delete_movie(db, movie)


@pytest.fixture(scope='function')
def movie_data(db) -> Generator:
    """
    Similar logic with the previous random_movie fixture
    but instead of creating the movies, create a factory
    for the movie data to be POST-ed (aka simulating the API)
    by the actual test function while keeping track of those ids.
    Pass control to the test fucntion and clean up later

    @param db: An SQLALchemy Session
    @return: A dict factory generator
    """
    created_movies = []

    def _make_movie_data(movie_id: str):
        data = {
            'imdb_id': movie_id,
            'title': f"{movie_id}-title",
            'year': random_int(2010, 2023),
            'genres': ["Adventure", "War", "Action"]
        }
        created_movies.append(movie_id)
        return data

    # pass over execution to the "caller func"
    yield _make_movie_data

    # cleanup
    for mid in created_movies:
        crud.delete_movie_by_id(db, mid)


@pytest.fixture(scope='function')
def movie_to_clean(db) -> Generator:
    """
    Similar to previous fixture 'movie_data' but only keep track
    of movie IDs, dont return anything back
    @param db: An SQLALchemy Session
    @return: Generator
    """
    created_movies = []

    def _movie_to_clean(movie_id: str):
        created_movies.append(movie_id)

    # pass over execution to the "caller func"
    yield _movie_to_clean

    # cleanup
    for mid in created_movies:
        crud.delete_movie_by_id(db, mid)
