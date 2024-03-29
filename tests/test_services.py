# Import the function from your services module
from app.services.anime_service import get_seasonal_anime


def test_fetch_seasonal_anime(app):
    with app.app_context():
        result = get_seasonal_anime(2022, 'Spring')
        assert result is True  # Or the actual expected outcome
