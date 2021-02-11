from os import environ


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    ENV = environ.get('FLASK_ENV')
    DEBUG = environ.get('DEBUG')
