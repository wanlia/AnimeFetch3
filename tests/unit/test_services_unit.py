import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.services.anime_service import get_seasonal_anime

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield

@patch('app.services.anime_service.requests.get')
def test_get_seasonal_anime(mock_get, app_context):
    """Test fetching seasonal anime works and handles API response correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [{"title": "Attack on Titan", "score": "9.0", "year": 2021, "season": "Winter"}]
    }
    mock_get.return_value = mock_response

    result = get_seasonal_anime(2021, 'Winter')
    assert result is True
