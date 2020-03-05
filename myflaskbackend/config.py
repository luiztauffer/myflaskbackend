import os


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    # FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    # SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
