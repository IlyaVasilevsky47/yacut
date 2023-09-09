import os
import string


class Config(object):
    FLASK_APP = os.getenv('FLASK_APP', default='yacut')
    FLASK_ENV = os.getenv('FLASK_ENV', default='development')
    SECRET_KEY = os.getenv('SECRET_KEY', default='8f42a73054b1749f8f58848be5e6502c')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHORT_LINK_VIEW = 'short_view'
    LONG_LINK = 2000
    LENGTH_SHORT = 16
    LENGTH_OF_RANDOM_NUMBERS = 6
    CHARACTER_RANGE = string.ascii_letters + string.digits
    NUMBER_OF_REPETITIONS = 4
    REGULAR_EXPRESSION = r'^[a-zA-Z0-9]+$'