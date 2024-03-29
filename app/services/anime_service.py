import requests
from ..models.models import Anime



def get_seasonal_anime(year, season):
    """
    Fetches seasonal anime data from the Jikan API and inserts it into the database.
    """
    url = f"https://api.jikan.moe/v4/seasons/{year}/{season}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses

        anime_data = response.json()['data']
        for anime in anime_data:
            title = anime['title']
            score = anime.get('score', 'N/A')
            # Correctly assign the result of insert_anime to the inserted variable
            inserted = Anime.insert_anime(title, score, year, season)
            if not inserted:
                print(f"Skipped insertion: Anime '{title}' for {season} {year} already exists in the database.")
        return True
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False


def get_anime_by_year_season(year, season):
    """
    Retrieves anime from the database filtered by year and season.
    """
    try:
        anime_list = Anime.query.filter_by(year=year, season=season).all()
        scores = [float(anime.score) for anime in anime_list if anime.score != 'N/A']
        avg_score = sum(scores) / len(scores) if scores else 0
        return anime_list, avg_score
    except Exception as e:
        print(f"Error fetching anime data: {e}")
        return [], 0
