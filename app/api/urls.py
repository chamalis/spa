
from fastapi import APIRouter

from app.api import ctrl


main_router = APIRouter()

main_router.include_router(
    ctrl.movie_router, prefix="/movies", tags=["movie"])


@main_router.get(path="/")
def home():
    return {
        "detail": "Welcome to SPA API. Please find the OpenAPI at /api/v1/openapi.json"
    }
