import json
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session
from starlette import status

from app.api import schemas
from app.db import crud
from app.db.base import get_db_sess
from app.util import types

movie_router = APIRouter()


@movie_router.get(path="", response_model=Page[schemas.MovieDTO])
def get_movies(
        sess: Session = Depends(get_db_sess),
        rating: float = 0, genre: types.Genre = None,
        order: str = ''):

    # order can be provided like: e.g order=rating,desc or order=title
    order_field, *order_trend = order.split(',')[0:2]
    order_trend = order_trend[0] if order_trend else ''

    ret = crud.get_movies_lazy(
        sess,
        min_rating=rating, genre=genre,
        order_field=order_field, order_trend=order_trend)

    return paginate(sess, ret)


@movie_router.get(
    path="/{mid}",
    response_model=schemas.MovieDTO,
    status_code=status.HTTP_200_OK)
def get_movie(mid: str, sess: Session = Depends(get_db_sess)) -> Any:
    movie = crud.get_movie(sess, mid)
    if not movie:
        raise HTTPException(status_code=404, detail="movie not found")

    return movie


@movie_router.post(
    path='',
    response_model=schemas.MovieDTO,
    status_code=status.HTTP_201_CREATED)
def create_movie(
        *,
        sess: Session = Depends(get_db_sess),
        movie_in: schemas.MovieCreateDTO
) -> Any:
    """
    Create new movie.
    """
    # Convert Pydantic instance to dict
    try:
        obj_in_data = jsonable_encoder(movie_in, by_alias=False)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f'Malformed input data:\n{e}\n'
        )

    # check if the movie already exists
    movie = crud.get_movie_by_kwargs(sess, **obj_in_data)
    if movie:
        raise HTTPException(
            status_code=409,
            detail=f'Movie with id: {movie.id}, already exists'
        )

    # Create and save the movie
    try:
        movie = crud.create_movie(sess, **obj_in_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f'Malformed input data:\n{e}\n'
        )

    return movie
