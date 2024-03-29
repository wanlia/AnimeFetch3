import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    # Update to use the DATABASE_URL for PostgreSQL, fallback to a local one if not found
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'anime_database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration, with a separate database."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'anime_database_test.db')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
