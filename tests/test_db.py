import pytest
from app.models.models import Anime, db

def test_insertion_and_query(app):
    """Test inserting an anime and querying it."""
    with app.app_context():
        title = "Test Anime"
        score = "8.5"
        year = 2022
        season = "Spring"
        
        # Test insertion
        inserted = Anime.insert_anime(title, score, year, season)
        assert inserted is True, "Anime should be inserted successfully."
        
        # Test insertion of duplicate (should return False)
        inserted_again = Anime.insert_anime(title, score, year, season)
        assert inserted_again is False, "Duplicate anime should not be inserted."
        
        # Test querying
        anime_list, avg_score = Anime.get_anime_by_year_season(year, season)
        assert len(anime_list) == 1, "There should be exactly one anime for the specified year and season."
        assert anime_list[0].title == title, "The queried anime title should match the inserted title."
        assert float(anime_list[0].score) == float(score), "The queried anime score should match the inserted score."
