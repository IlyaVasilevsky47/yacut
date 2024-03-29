import os
import re
import string

SHORT_LINK_VIEW = 'short_view'
LENGTH_ORIGINAL = 2000
LENGTH_SHORT = 16
LENGTH_UNIQUE_SHORT = 6
SYMBOLS_UNIQUE_SHORT = string.ascii_letters + string.digits
REPETITIONS_UNIQUE_SHORT = 4
REGULAR_EXPRESSION = rf'^[{re.escape(SYMBOLS_UNIQUE_SHORT)}]+$'


class Config():
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV', default='development')
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='8f42a73054b1749f8f58848be5e6502c'
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
