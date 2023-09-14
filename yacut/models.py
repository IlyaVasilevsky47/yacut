import random
import re
from datetime import datetime

from settings import (LENGTH_ORIGINAL, LENGTH_SHORT, LENGTH_UNIQUE_SHORT,
                      REGULAR_EXPRESSION, REPETITIONS_UNIQUE_SHORT,
                      SYMBOLS_UNIQUE_SHORT)

from . import db

ERROR_LENGTH_ORIGINAL = 'Указано недопустимая длинна длинный ссылки'
ERROR_SHORT = 'Указано недопустимое имя для короткой ссылки'
ERROR_UNIQUE_SHORT = 'Имя "{short_id}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(LENGTH_SHORT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def generate_short_id():
        for _ in range(REPETITIONS_UNIQUE_SHORT):
            short_id = ''.join(
                random.sample(
                    SYMBOLS_UNIQUE_SHORT,
                    LENGTH_UNIQUE_SHORT
                )
            )
            if not URLMap.get(short_id):
                return short_id
        raise RuntimeError(ERROR_UNIQUE_SHORT.format(short_id=short_id))

    @staticmethod
    def create(original, short_id=None, validation=False):
        if validation:
            if len(original) > LENGTH_ORIGINAL:
                raise ValueError(ERROR_LENGTH_ORIGINAL)
        if short_id:
            if validation:
                if (
                    len(short_id) > LENGTH_SHORT or
                    re.search(REGULAR_EXPRESSION, short_id) is None
                ):
                    raise ValueError(ERROR_SHORT)
                if URLMap.get(short_id):
                    raise RuntimeError(
                        ERROR_UNIQUE_SHORT.format(short_id=short_id)
                    )
        else:
            short_id = URLMap.generate_short_id()
        url_map = URLMap(original=original, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map
