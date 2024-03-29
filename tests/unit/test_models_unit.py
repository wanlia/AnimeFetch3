from app.models.models import Anime

def test_anime_model_creation():
    """Test creating an Anime model works correctly."""
    anime = Anime(title="Sora yori mo Tooi Basho", score="8.5", year=2018, season="Winter")
    assert anime.title == "Sora yori mo Tooi Basho"
    assert anime.score == "8.5"
    assert anime.year == 2018
    assert anime.season == "Winter"
