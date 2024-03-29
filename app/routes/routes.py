from flask import Blueprint, render_template, request, flash
from ..services.anime_service import get_seasonal_anime, get_anime_by_year_season


# Create a Blueprint for your app routes
bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    anime_list = None
    avg_score = None  # Initialize variable for average score
    if request.method == 'POST':
        year = request.form['year']
        season = request.form['season']
        if get_seasonal_anime(year, season):
            anime_list, avg_score = get_anime_by_year_season(year, season)  # Update to receive avg_score
            if anime_list:
                flash('Anime data successfully fetched for {} {}. Average Score: {:.2f}'.format(season, year, avg_score), 'success')
            else:
                flash('No anime data found for {} {}'.format(season, year), 'error')
        else:
            flash('Failed to fetch data from the API.', 'error')
    return render_template('index.html', anime_list=anime_list, avg_score=avg_score)

def configure_routes(app):
    # Register the Blueprint with the Flask application
    app.register_blueprint(bp)
