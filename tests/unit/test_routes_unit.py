import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

@pytest.fixture
def mock_get_seasonal_anime():
    with patch('app.routes.routes.get_seasonal_anime') as mock:
        # Setup a default return value that can be overridden in individual tests
        mock.return_value = (True, [{"title": "Example Anime", "score": "8.5", "year": 2021, "season": "Winter"}], 8.5)
        yield mock

@pytest.mark.usefixtures("client")
def test_index_route_get(client):
    """Test that the index route is accessible via GET and loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Anime" in response.data

#@pytest.mark.usefixtures("client", "mock_get_seasonal_anime")
#def test_index_route_post(mock_get_seasonal_anime, client):
#    """Test posting to the index route processes data correctly."""
    # If needed, adjust the mock return value for specific tests here
    # mock_get_seasonal_anime.return_value = (True, [{"title": "Specific Anime", "score": "9.0", "year": 2021, "season": "Winter"}], 9.0)

#    response = client.post('/', data={'year': '2021', 'season': 'Winter'})
#    assert response.status_code == 200
    # Ensure the assertions match the expected outcomes of the route's logic
#    assert b"Anime data successfully fetched" in response.data or b"Average Score: 8.5" in response.data
