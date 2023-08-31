from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, validate_short


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    short = data.get('custom_id')
    if not short:
        short = get_unique_short_id()
    else:
        if validate_short(short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(short=short).first():
            raise InvalidAPIUsage(f'Имя "{short}" уже занято.')

    urlmap = URLMap(original=data.get('url'), short=short)
    db.session.add(urlmap)
    db.session.commit()
    return (
        jsonify(
            dict(
                url=urlmap.original,
                short_link=f'{url_for("index_view", _external=True)}{urlmap.short}',
            )
        ),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original(short_id):
    try:
        return (
            jsonify(
                dict(
                    url=URLMap.query.filter_by(short=short_id).first().original,
                )
            ),
            HTTPStatus.OK,
        )
    except AttributeError:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
