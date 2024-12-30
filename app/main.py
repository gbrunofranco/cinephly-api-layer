from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader

from app.utils import verify_api_key

from . import schemas
from .d1_client import D1Client
from .routers.movies import router as movie_router

app = FastAPI()
app.include_router(movie_router)

d1_client = D1Client()

api_key_header = APIKeyHeader(name="Authorization")


@app.post("/api/exec", response_model=schemas.QueryResult)
async def execute_query(query: schemas.QueryParams, api_key: str = Depends(verify_api_key)) -> schemas.QueryResult:
    try:
        result = await d1_client.execute_query(query.query, query.params)
        return schemas.QueryResult(results=result.get("result", []), success=True)
    except Exception as e:
        return schemas.QueryResult(results=[], success=False, errors=[str(e)])
