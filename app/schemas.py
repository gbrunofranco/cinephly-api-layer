from typing import Any

from pydantic import BaseModel


class QueryParams(BaseModel):
    query: str
    params: list[Any] | None = None


class QueryResult(BaseModel):
    results: list[dict[str, Any]]
    success: bool
    errors: list[str] | None = None


class Movie(BaseModel):
    movie_id: str
    movie_name: str
    imdb_id: str
    duration_minutes: int
    year: int
    director: list[str]
    synopsis: str
    genres: list[str]
    poster_url: str
