from fastapi import APIRouter, Depends

from app.d1_client import D1Client
from app.main import verify_api_key
from app.schemas import Movie, QueryResult

d1_client = D1Client()
router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.post("/", response_model=QueryResult)
async def create_movie(movie: Movie, api_key: str = Depends(verify_api_key)) -> QueryResult:
    # First, create the movies table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id TEXT PRIMARY KEY,
        imdb_id TEXT,
        movie_name TEXT NOT NULL,
        duration_minutes INTEGER,
        year INTEGER,
        director TEXT,
        synopsis TEXT,
        genres TEXT,
        poster_url TEXT
    );
    """

    try:
        await d1_client.execute_query(create_table_query)

        insert_query = """
        INSERT INTO movies (
            imdb_id, movie_id, movie_name, duration_minutes, 
            year, director, synopsis, genres, poster_url
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """

        params = [
            movie.imdb_id,
            movie.movie_id,
            movie.movie_name,
            movie.duration_minutes,
            movie.year,
            ",".join(movie.director),
            movie.synopsis,
            ",".join(movie.genres),
            movie.poster_url,
        ]

        await d1_client.execute_query(insert_query, params)
        return QueryResult(results=[{"message": "Movie created successfully"}], success=True)

    except Exception as e:
        return QueryResult(results=[], success=False, errors=[str(e)])
