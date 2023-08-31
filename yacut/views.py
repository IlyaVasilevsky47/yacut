import random
import re
import string
from http import HTTPStatus

from flask import Markup, abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    short = ''.join(random.sample(string.ascii_letters + string.digits, length))
    if URLMap.query.filter_by(short=short).first():
        get_unique_short_id()
    else:
        return short


def validate_short(short):
    if (
        len(short) <= 16 and
        short.isalnum() and
        short.islower() and
        not short.isupper() and
        re.search(r'[^0-9a-z]', short) is None
    ):
        return False
    return True


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        else:
            if validate_short(short):
                flash('Недопустимая короткая ссылка!')
                return render_template('pages/index.html', form=form)
            if URLMap.query.filter_by(short=short).first():
                flash(f'Имя {short} уже занято!')
                return render_template('pages/index.html', form=form)
        db.session.add(URLMap(original=form.original_link.data, short=short))
        db.session.commit()
        flash(
            Markup(
                (
                    'Ваша новая ссылка готова: \n'
                    '<a href="{href}{short}" class="alert-link">{href}{short}</a>'
                ).format(href=url_for('index_view', _external=True), short=short)
            )
        )
    return render_template('pages/index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def short_view(short_id):
    short = URLMap.query.filter_by(short=short_id).first()
    if short:
        return redirect(short.original, code=HTTPStatus.FOUND)
    abort(HTTPStatus.NOT_FOUND)
