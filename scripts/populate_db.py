#!/usr/bin/env python

import subprocess
import sys
from pathlib import Path
from typing import List

import pandas as pd
import sqlalchemy.exc
from sqlalchemy import update, insert

ROOTDIR = Path(__file__).resolve().parent.parent
sys.path.append(ROOTDIR.joinpath('app'))

from app.db import crud
from app.db.util import create_sess_factory
from app.db.models import Movie
from app.util.types import Genre

RAW_DATADIR = ROOTDIR.joinpath('raw_data')

basics = RAW_DATADIR.joinpath('title.basics.tsv.gz')
ratings = RAW_DATADIR.joinpath('title.ratings.tsv.gz')
basics_cols_to_use = [
    'tconst', 'titleType', 'originalTitle', 'startYear', 'runtimeMinutes', 'genres'
]
ratings_cols_to_use = [
    'tconst', 'averageRating'
]


def _build_movie_data(row: List) -> dict:
    return {
        'id': row[0],
        'title': row[2][:128] if row[2] else None,
        'year': row[3] if row[3] else None,
        'runtime': row[4] if row[4] else None,
        'genres': Genre.from_list(
            row[5].split(',') if row[5] else None),
        'imdb_url': f'https://www.imdb.com/title/{row[0]}'
    }


def _parse_basics(sess_factory, basics_file: Path | str):
    with sess_factory() as sess:
        print(f'Parsing {basics_file} file...')

        chunk_gen = pd.read_csv(
            basics_file,
            delimiter='\t',
            quoting=3,  # ignore quotes
            iterator=True,
            chunksize=50000,
            na_values="\\N",  # keep_default_na=False,
            usecols=basics_cols_to_use,
            dtype={
                'startYear': 'Int16',  # Int8 fails with NaN values :S
                'runtimeMinutes': 'Int16'
            },
            on_bad_lines="warn"
        )
        for chunk in chunk_gen:
            chunk.fillna(0, inplace=True)

            sess.scalars(
                insert(Movie).values().returning(Movie),
                [
                    _build_movie_data(row)
                    for row in chunk.values if row[1] in ('movie', 'tvMovie')
                ]
            )
            sess.commit()

        # This alternative way we can continue looping in case of contraint
        # error, because save is per-object, but it takes ages ...
        # for row in chunk.iterrows():  # vs chunk.values:
        #     row[1].fillna(0, inplace=True)
        #     values = row[1].values
        #     if values[1] and values[1].lower() in ('movie', 'tvmovie'):
        #         kwargs = build_movie_data(values)
        #         try:
        #             create_movie(db_conn, **kwargs)
        #         except sqlalchemy.exc.IntegrityError as e:
        #             pass  # already in


def _parse_ratings(sess_factory, ratings_file: Path | str):
    print(f'Parsing {ratings_file} file...')

    with sess_factory() as sess:
        for chunk in pd.read_csv(
                ratings_file,
                delimiter='\t',
                quoting=3,  # ignore quotes
                iterator=True,
                chunksize=50000,
                na_values="\\N",  # keep_default_na=False,
                usecols=ratings_cols_to_use,
                dtype={
                    'averageRating': 'float'
                },
                on_bad_lines="warn"
        ):
            chunk.fillna(0, inplace=True)
            sess.flush()

            # SQLALCHEMY Bug: cant update only PKs matching (StaleDataError)
            # hence we need to cross match keys in the update payload
            pks = set(mid for mid, in sess.query(Movie.id))
            sess.execute(
                update(Movie),
                [
                    {
                        'id': row[0],
                        'rating': row[1]
                    }
                    for row in chunk.values if row[0] in pks  # tragic ...
                ],
            )
            sess.commit()


def init_db_pipeline(sess_factory):
    """
    WARNING: This pipeline will take 5-15 minutes. Will
    1) download dataset, if not already in raw-data
    2) fill in the database
    """
    print("Filling in data! This will take 5-15' ...")

    # prepare_data_script = ROOTDIR.joinpath('scripts/prepare_data.sh')
    # rc = subprocess.call(prepare_data_script)
    # if rc:
    #     print(f"prepare_data.sh returned error code: {rc}\nExiting...")
    #     sys.exit(rc)

    try:
        _parse_basics(sess_factory, basics)
    except sqlalchemy.exc.IntegrityError as e:
        # just in case _parse_basics was completed last time but _parse_settings
        # didnt, continue with attempting to rerun _parse_settings
        print(e)

    _parse_ratings(sess_factory, ratings)


def main():
    print("checking the database status...")

    # create db factory. Due to huge inserts, dont print sql (debug false)
    sess_factory = create_sess_factory(debug=False)

    # check if sufficient data in the db
    with sess_factory() as sess:
        res = crud.get_all_movies(sess, size=50)
        if len(res) < 50:
            # INIT DB FROM THE BEGINNING:
            init_db_pipeline(sess_factory)
        else:
            print("Connection ok, some data in, skipping initialization")
            print("If you want to force data insertion, need to truncate the table first")


if __name__ == '__main__':
    # this way this script can also be invoked directly
    main()
