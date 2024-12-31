import pytest


class TestMovie:
    def test_create_movie_unauthorized(self, client, valid_movie):
        response = client.post("/api/v1/movies/", json=valid_movie, headers={})
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]

    def test_create_movie_invalid_api_key(self, client, valid_movie):
        headers = {"Authorization": "Bearer not-api-key"}
        response = client.post("/api/v1/movies/", json=valid_movie, headers=headers)
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_movie_success(self, client, auth_headers, mock_d1_client, valid_movie):
        mock_d1_client.execute_query.return_value = {"result": []}

        response = client.post("/api/v1/movies/", json=valid_movie, headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == {"results": [{"message": "Movie created successfully"}], "success": True, "errors": None}

        # Verify D1Client was called correctly
        calls = mock_d1_client.execute_query.call_args_list
        assert len(calls) == 2  # One for CREATE TABLE, one for INSERT

        # Verify the INSERT query parameters
        insert_call = calls[1]
        assert "INSERT INTO movies" in insert_call.args[0]
        assert valid_movie["imdb_id"] in insert_call.args[1]

    def test_create_movie_invalid_data(self, client, auth_headers, valid_movie):
        invalid_movie = valid_movie.copy()
        invalid_movie.pop("imdb_id")  # Remove required field

        response = client.post("/api/v1/movies/", json=invalid_movie, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_database_error_handling(self, client, auth_headers, mock_d1_client, valid_movie):
        mock_d1_client.execute_query.side_effect = Exception("Database error")

        response = client.post("/api/v1/movies/", json=valid_movie, headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == {"results": [], "success": False, "errors": ["Database error"]}
