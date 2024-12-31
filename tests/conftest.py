from typing import Generator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings, SettingsConfigDict


@pytest.fixture(scope="module")
def mock_d1_client() -> Generator[AsyncMock, None, None]:
    with patch("app.d1_client.D1Client") as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        yield mock_instance


class Settings(BaseSettings):
    api_key: str = ""
    cloudflare_api_token: str = ""
    cloudflare_account_id: str = ""
    d1_database_id: str = ""

    model_config = SettingsConfigDict(env_file=".test.env", env_file_encoding="utf-8", extra="ignore")


@pytest.fixture
def client(mock_d1_client):  # Needed otherwise patching of d1_client won't work, due to the app import
    from app.main import app

    return TestClient(app)


@pytest.fixture
def mock_settings():
    return Settings()


@pytest.fixture
def auth_headers(mock_settings):
    return {"Authorization": f"Bearer {mock_settings.api_key}"}


@pytest.fixture
def valid_movie():
    return {
        "imdb_id": "tt0111161",
        "movie_id": "shawshank-redemption-test",
        "movie_name": "The Shawshank Redemption",
        "duration_minutes": 142,
        "year": 1994,
        "director": ["Frank Darabont"],
        "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "genres": ["Drama", "Crime"],
        "poster_url": "https://example.com/shawshank-poster.jpg",
    }
