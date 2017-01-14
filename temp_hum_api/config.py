# Builtin config values: http://flask.pocoo.org/docs/0.10/config/
import os
import logging


class BaseConfig(object):
    DEBUG = os.environ.get('DEBUG', False)
    HOST = os.environ.get('HOST', 'localhost')
    PORT = int(os.environ.get('PORT', 5000))

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'temp_hum-api.log'
    LOGGING_LEVEL = logging.DEBUG


class DevelopmentConfig(BaseConfig):
    HOST = '10.112.10.15'
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    LOGGING_LEVEL = logging.FATAL
    HOST = '10.112.10.3'
    PORT = 15001


config = {
    "development": "temp_hum_api.config.DevelopmentConfig",
    "testing": "temp_hum_api.config.TestingConfig",
    "production": "temp_hum_api.config.ProductionConfig",
    "default": "temp_hum_api.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
