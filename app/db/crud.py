from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session
import sqlalchemy.exc

from app.db.models import Movie
from app.util import types


def save_movie(session: Session, db_obj: Movie) -> None:
    session.add(db_obj)
    try:
        session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        session.rollback()
        raise
    else:
        # load potentially new values (e.g autogenerated PK)
        session.refresh(db_obj)
    finally:
        session.close()  # not needed if throug get_db_conn


def create_movie(session: Session, save: bool = True, **kwargs) -> Movie:
    """Creates and saved if save=True a movie to the DB"""
    mid, murl = _get_id_and_url(**kwargs)

    genres = kwargs.get('genres', '')
    if isinstance(genres, str):
        genres = genres.split(',')
    genres = types.Genre.from_list(genres)

    # pass attributes explicitly, always a good idea
    movie = Movie(
        id=mid,
        genres=genres,
        imdb_url=murl,
        title=kwargs['title'],
        year=kwargs.get('year'),
        runtime=kwargs.get('runtime'),
        rating=kwargs.get('rating'),
    )
    if save is True:
        save_movie(session, movie)

    return movie


def get_movie(session: Session, mid: str) -> Movie | None:
    return session.query(Movie).filter(Movie.id == mid).first()


def get_movie_by_kwargs(session: Session, **kwargs) -> Movie | None:
    mid, _ = _get_id_and_url(**kwargs)

    return get_movie(session, mid)


def get_movies_lazy(
        session: Session,
        genre: str = None,
        min_rating: float = None,
        order_field: str = '', order_trend: str = ''
) -> sqlalchemy.orm.Query:
    """ Suitable for pagination """

    # base query to build upon
    query = session.query(Movie)

    # Apply genre filter
    genre = types.Genre.get(genre)
    if genre:
        query = query.filter(Movie.genres.any(genre))

    # Apply rating filter
    if min_rating:
        query = query.filter(Movie.rating >= min_rating)

    # Apply sorting if the field is attribute of the class
    if getattr(Movie, order_field, None):
        if order_trend == 'desc':
            query = query.order_by(desc(order_field))
        else:  # 'asc' in all other inputs
            query = query.order_by(order_field)

    return query


def get_all_movies(session: Session, size: int = 100, **kwargs) -> List[Movie]:
    """Loads all movies in memory (non-lazy)"""
    return get_movies_lazy(session, **kwargs).limit(size).all()


def delete_movie(session: Session, obj: Movie):
    session.delete(obj)
    session.commit()

def delete_movie_by_id(session: Session, mid: str):
    obj = session.get(Movie, mid)
    if obj:
        delete_movie(session, obj)


def _get_id_and_url(**kwargs):
    mid = kwargs['id']
    if not mid:
        # no id => imdb_url is provided
        imdb_url = kwargs['imdb_url']
        mid = imdb_url.rstrip('/').split('/')[-1]
    else:
        imdb_url = f'https://www.imdb.com/title/{mid}'

    return mid, imdb_url