import os


class Config(object):
    FLASK_APP = os.getenv('FLASK_APP', default='yacut')
    FLASK_ENV = os.getenv('FLASK_ENV', default='development')
    SECRET_KEY = os.getenv('SECRET_KEY', default='8f42a73054b1749f8f58848be5e6502c')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
