import random
import re
import string
from datetime import datetime

from . import db

LONG_LINK = 2000
SHORT_LINK = 16


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LONG_LINK), nullable=False)
    short = db.Column(db.String(SHORT_LINK), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def checking_uniqueness_short(short):
        return URLMap.query.filter_by(short=short).first()

    def get_unique_short_id(length=6):
        short = ''.join(random.sample(string.ascii_letters + string.digits, length))
        if URLMap.checking_uniqueness_short(short):
            URLMap.get_unique_short_id()
        else:
            return short

    def validate_short(short):
        if (
            len(short) <= SHORT_LINK and
            short.isalnum() and
            short.islower() and
            not short.isupper() and
            re.search(r'[^0-9a-z]', short) is None
        ):
            return False
        return True

    def created_object(original, short):
        if not short:
            short = URLMap.get_unique_short_id()
        else:
            if URLMap.validate_short(short):
                raise ValueError('Указано недопустимое имя для короткой ссылки')
            if URLMap.checking_uniqueness_short(short):
                raise RuntimeError(f'Имя "{short}" уже занято.')
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap