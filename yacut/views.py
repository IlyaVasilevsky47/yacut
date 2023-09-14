from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for
from settings import SHORT_LINK_VIEW

from . import app
from .forms import URLMapForm
from .models import URLMap

FLASH_UNIQUE_SHORT = 'Имя {short_id} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    try:
        if not form.validate_on_submit():
            return render_template('index.html', form=form)
        short_id = form.custom_id.data
        return render_template(
            'index.html',
            form=form,
            link_short=url_for(
                SHORT_LINK_VIEW,
                short_id=URLMap.create(
                    original=form.original_link.data,
                    short_id=short_id
                ).short,
                _external=True,
            ),
        )
    except ValueError as error:
        flash(error)
    except RuntimeError:
        flash(FLASH_UNIQUE_SHORT.format(short_id=short_id))
    return render_template('index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def short_view(short_id):
    url_map = URLMap.get(short_id)
    if url_map:
        return redirect(url_map.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
