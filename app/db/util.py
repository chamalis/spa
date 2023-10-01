from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression
from sqlalchemy.types import (
    DateTime
)

from app import settings


def create_sess_factory(debug: bool = settings.DEBUG) -> sessionmaker:
    db_url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        settings.DB_USER, settings.DB_PASS,
        settings.DB_HOST, settings.DB_PORT,
        settings.DB_NAME
    )

    # The first step is to create a SQLAlchemy "engine".
    echo = True if debug is True else False
    engine = create_engine(db_url, echo=echo)

    # Scoped (Thread local) session factory
    sess_local_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)

    return sess_local_factory


# ref: https://docs.sqlalchemy.org/en/20/core/compiler.html#utc-timestamp-function
class UtcNow(expression.FunctionElement):
    """
    A helper class to provide default values in UTC
    """
    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(UtcNow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"
