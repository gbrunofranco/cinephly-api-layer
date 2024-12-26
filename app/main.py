from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from . import schemas
from .config import settings
from .d1_client import D1Client

app = FastAPI()
d1_client = D1Client()

api_key_header = APIKeyHeader(name="Authorization")


async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid API key format")
    key = api_key.split(" ")[1]
    if key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key


@app.post("/api/exec", response_model=schemas.QueryResult)
async def execute_query(query: schemas.QueryParams, api_key: str = Depends(verify_api_key)) -> schemas.QueryResult:
    try:
        result = await d1_client.execute_query(query.query, query.params)
        return schemas.QueryResult(results=result.get("result", []), success=True)
    except Exception as e:
        return schemas.QueryResult(results=[], success=False, errors=[str(e)])
