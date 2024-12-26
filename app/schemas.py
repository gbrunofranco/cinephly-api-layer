from typing import Any

from pydantic import BaseModel


class QueryParams(BaseModel):
    query: str
    params: dict[str, Any] | None = None


class QueryResult(BaseModel):
    results: list[dict[str, Any]]
    success: bool
    errors: list[str] | None = None
