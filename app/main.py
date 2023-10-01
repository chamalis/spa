from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api import urls
from app.db.base import get_db_sess
from app.db import models

app = FastAPI(
    title="API v1",
    openapi_url=f"/api/v1/openapi.json"
)
add_pagination(app)

app.include_router(urls.main_router, prefix="/api/v1")

# check that we can connect to the db
sess = get_db_sess()
