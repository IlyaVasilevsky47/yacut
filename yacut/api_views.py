from http import HTTPStatus

from flask import jsonify, request, url_for
from settings import SHORT_LINK_VIEW

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

NO_BODY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
ERROR_SHORT_ID = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_BODY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED)
    try:
        return (
            jsonify(
                dict(
                    url=data['url'],
                    short_link=url_for(
                        SHORT_LINK_VIEW,
                        short_id=URLMap.create(
                            original=data['url'],
                            short_id=data.get('custom_id'),
                            full_validation=True
                        ).short,
                        _external=True,
                    ),
                )
            ),
            HTTPStatus.CREATED,
        )
    except (ValueError, RuntimeError) as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original(short_id):
    url_map = URLMap.get(short_id)
    if url_map:
        return jsonify(dict(url=url_map.original)), HTTPStatus.OK
    raise InvalidAPIUsage(ERROR_SHORT_ID, HTTPStatus.NOT_FOUND)
