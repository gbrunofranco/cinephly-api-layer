from typing import Any

import httpx

from .config import settings


class D1Client:
    def __init__(self):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{settings.cloudflare_account_id}"
        self.headers = {"Authorization": f"Bearer {settings.cloudflare_api_token}", "Content-Type": "application/json"}

    async def execute_query(self, query: str, params: list[Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.post(
                f"/d1/database/{settings.d1_database_id}/query",
                headers=self.headers,
                json={"sql": query, "params": params or []},
            )
            response.raise_for_status()
            return response.json()
