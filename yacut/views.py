from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for
from settings import Config

from . import app
from .forms import URLMapForm
from .models import URLMap

FLASH_UNIQUE_SHORT = 'Имя {short} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    try:
        return render_template(
            'index.html',
            form=form,
            link_short=url_for(
                Config.SHORT_LINK_VIEW,
                short_id=URLMap.created_object(
                    original=form.original_link.data, short=short
                ).short,
                _external=True,
            ),
        )
    except ValueError as error:
        flash(error)
        return render_template('index.html', form=form)
    except RuntimeError:
        flash(FLASH_UNIQUE_SHORT.format(short=short))
        return render_template('index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def short_view(short_id):
    url_map = URLMap.get(short_id)
    if url_map:
        return redirect(url_map.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
