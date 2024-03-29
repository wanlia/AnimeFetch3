from flask import Flask
# Ensure you import os for environment variable access
import os
from .models.models import db  # Adjust based on your project structure
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from .routes.routes import configure_routes


def create_app():
    app = Flask(__name__)

    # Assuming the use of DevelopmentConfig, ProductionConfig, TestingConfig
    # Automatically select the configuration based on an environment variable
    config_type = os.getenv('FLASK_CONFIG', 'development').lower()
    if config_type == 'production':
        app.config.from_object(ProductionConfig)
    elif config_type == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Database URI configuration
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Ensure the URI starts with "postgresql://" (Heroku sometimes provides "postgres://")
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    else:
        # Fallback to a default SQLite database if DATABASE_URL is not set
        database_url = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    configure_routes(app)

    # Further configuration, such as registering blueprints
    # ...

    return app
