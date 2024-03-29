from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()

def create_database(app):
    """Initializes the database."""
    db.init_app(app)
    with app.app_context():
        db.create_all()

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    score = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String(50), nullable=False)

    @staticmethod
    def insert_anime(title, score, year, season):
        exists = Anime.query.filter_by(title=title, year=year, season=season).first()
        if not exists:
            new_anime = Anime(title=title, score=score, year=year, season=season)
            db.session.add(new_anime)
            db.session.commit()
            return True
        else:
            print(f"Anime '{title}' for {season} {year} already exists in the database.")
            return False

    @staticmethod
    def get_anime_by_year_season(year, season):
        anime_list = Anime.query.filter_by(year=year, season=season).all()
        scores = [float(anime.score) for anime in anime_list if anime.score and anime.score != 'N/A']
        avg_score = sum(scores) / len(scores) if scores else 0
        return anime_list, avg_score
