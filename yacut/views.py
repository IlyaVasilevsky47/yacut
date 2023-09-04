from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    try:
        urlmap = URLMap.created_object(
            original=form.original_link.data,
            short=short
        )
    except ValueError as error:
        flash(error)
        return render_template('index.html', form=form)
    except RuntimeError:
        flash(f'Имя {short} уже занято!')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form, urlmap=urlmap)


@app.route('/<short_id>', methods=['GET'])
def short_view(short_id):
    short = URLMap.checking_uniqueness_short(short_id)
    if short:
        return redirect(short.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
