from http import HTTPStatus

from flask import jsonify, request, url_for

from . import CLICK_ON_A_SHORT_LINK, app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    try:
        urlmap = URLMap.created_object(
            original=data.get('url'),
            short=data.get('custom_id')
        )
    except Exception as error:
        raise InvalidAPIUsage(str(error))

    return (
        jsonify(dict(
            url=urlmap.original,
            short_link=f'{url_for(CLICK_ON_A_SHORT_LINK, short_id=urlmap.short, _external=True)}',
        )),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original(short_id):
    short = URLMap.checking_uniqueness_short(short_id)
    if short:
        return jsonify(dict(url=short.original)), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
