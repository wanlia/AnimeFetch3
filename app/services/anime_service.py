import os
import requests
import pika
import logging
from ..models.models import Anime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            inserted = Anime.insert_anime(title, score, year, season)
            if inserted:
                # Publish an event only if the anime is successfully inserted
                publish_anime_event(title)
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return False
    return True

def publish_anime_event(anime_title):
    """
    Publishes an event to a RabbitMQ queue when a new anime is added.
    """
    cloudamqp_url = os.getenv('CLOUDAMQP_URL')
    logging.info(f"Using CLOUDAMQP_URL: {cloudamqp_url}")
    connection = None
    try:
        params = pika.URLParameters(cloudamqp_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='anime_updates')
        channel.basic_publish(exchange='', routing_key='anime_updates', body=f'New anime added: {anime_title}')
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        logging.error(f"An error occurred while publishing to RabbitMQ: {e}")
    finally:
        if connection:
            connection.close()

def get_anime_by_year_season(year, season):
    """
    Retrieves anime from the database filtered by year and season.
    """
    try:
        anime_list = Anime.query.filter_by(year=year, season=season).all()
        scores = [float(anime.score) for anime in anime_list if anime.score and anime.score != 'N/A']
        avg_score = sum(scores) / len(scores) if scores else 0
        return anime_list, avg_score
    except Exception as e:
        logging.error(f"Error fetching anime data: {e}")
        return [], 0
