def test_development_config(app):
    app.config.from_object('config.DevelopmentConfig')
    assert app.config['DEBUG'] is True
    assert not app.config.get('SECRET_KEY') is 'your_secret_key_here'

def test_production_config(app):
    app.config.from_object('config.ProductionConfig')
    assert app.config['DEBUG'] is False
