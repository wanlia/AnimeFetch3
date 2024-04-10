import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

@pytest.fixture
def mock_get_seasonal_anime():
    with patch('app.routes.routes.get_seasonal_anime') as mock:

        mock.return_value = (True, [{"title": "Example Anime", "score": "8.5", "year": 2021, "season": "Winter"}], 8.5)
        yield mock

@pytest.mark.usefixtures("client")
def test_index_route_get(client):
    """Test that the index route is accessible via GET and loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Anime" in response.data

