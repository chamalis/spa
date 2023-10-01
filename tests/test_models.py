import pytest
import sqlalchemy.exc
from sqlalchemy.orm import Session

from app.db import crud
from app.db.models import Movie
from app.util import types


def test_movie_save_fail(db: Session):
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        # id (from imdb_id) missing
        movie1 = Movie(
            title='Incendies',
            year=2010,
            runtime=131,
            rating=8.3,
            genres=['Drama', 'Mystery', 'War'],
            imdb_url="https://www.imdb.com/title/tt1255953/"
        )
        crud.save_movie(db, movie1)


def test_movie_save_pass(db, movie_to_clean):
    mid = 'tttest02'

    # register the id to be cleaned with a fixture
    movie_to_clean(mid)

    data = {
        "id": mid,
        "year": 2010,
        "runtime": 131,
        "rating": 8.3,
        "genres": [types.Genre.War, types.Genre.Adventure],
        "imdb_url": f"https://www.imdb.com/title/{mid}"
    }
    # create and save the movie
    movie1 = Movie(**data)
    crud.save_movie(db, movie1)

    # ensure everything went fine. The fixture will clean up
    assert movie1 is not None
    assert movie1.id == mid
    assert len(movie1.genres) == 2


def test_movie_create_fail(db: Session):
    # test wrong genre
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        crud.create_movie(
            db,
            id='shall',
            title='notpass',
            year=2010,
            runtime=131,
            rating=8.3,
            genres=['WRONGGENRE', 'Mystery', 'War'],
            imdb_url="https://www.imdb.com/title/tt1255953/"
        )

    # todo test other cases of validation error etc
