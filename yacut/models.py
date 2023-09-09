import random
import re
from datetime import datetime

from settings import Config

from . import db

ERROR_LONG_LINK = 'Указано недопустимая длинна длинный ссылки'
ERROR_SHORT = 'Указано недопустимое имя для короткой ссылки'
ERROR_UNIQUE_SHORT = 'Имя "{short}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(Config.LONG_LINK), nullable=False)
    short = db.Column(db.String(Config.LENGTH_SHORT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(Config.NUMBER_OF_REPETITIONS):
            short = ''.join(
                random.sample(
                    Config.CHARACTER_RANGE,
                    Config.LENGTH_OF_RANDOM_NUMBERS
                )
            )
            if not URLMap.get(short):
                break
        return short

    @staticmethod
    def created_object(original, short):
        if len(original) > Config.LONG_LINK:
            raise ValueError(ERROR_LONG_LINK)
        if not short:
            short = URLMap.get_unique_short_id()
        else:
            if (
                len(short) > Config.LENGTH_SHORT or
                re.search(Config.REGULAR_EXPRESSION, short) is None
            ):
                raise ValueError(ERROR_SHORT)
            if URLMap.get(short):
                raise RuntimeError(ERROR_UNIQUE_SHORT.format(short=short))
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
