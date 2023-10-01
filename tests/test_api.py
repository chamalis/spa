from fastapi.testclient import TestClient

from app import settings
from app.db import models
from .conftest import db  # noqa


def test_create_movie(movie_data, client: TestClient) -> None:
    data = movie_data('tttest01')

    # First time should pass
    response = client.post(
        f"{settings.API_URLPATH}/movies", json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert "title" in content and "imdb_url" in content
    assert content["title"] == data["title"]
    assert content["imdb_url"] == f"https://www.imdb.com/title/{data['imdb_id']}"

    # second time should return conflict
    response = client.post(
        f"{settings.API_URLPATH}/movies", json=data,
    )
    assert response.status_code == 409


def test_get_movie(random_movie: models.Movie, client: TestClient) -> None:
    """
    @param random_movie: fixture that creates and saves a movie, calls
    the current function, and after that deletes the movie from the db
    @param builtin client from starlene, made for testing
    """
    response = client.get(
        f"{settings.API_URLPATH}/movies/{random_movie.id}",
    )
    assert response.status_code == 200

    content = response.json()
    assert content["title"] == random_movie.title
    assert content["imdb_id"] == random_movie.id
