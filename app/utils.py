from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config import settings

api_key_header = APIKeyHeader(name="Authorization")


async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid API key format")
    key = api_key.split(" ")[1]
    if key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key
