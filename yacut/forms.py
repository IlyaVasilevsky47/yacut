from flask_wtf import FlaskForm
from settings import LENGTH_ORIGINAL, LENGTH_SHORT, REGULAR_EXPRESSION
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .models import URLMap

ORIGINAL_LINK = 'Длинная ссылка'
CUSTOM_ID = 'Ваш вариант короткой ссылки'
SUBMIT = 'Создать'

ERROR_REQUIRED = 'Обязательное поле'
ERROR_VALIDATE_SHORT = (
    'Доступные символы: большие латинские буквы,'
    'маленькие латинские буквы, цифры в диапазоне от 0 до 9.'
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK,
        validators=[
            Length(max=LENGTH_ORIGINAL),
            DataRequired(message=ERROR_REQUIRED),
        ]
    )
    custom_id = URLField(
        CUSTOM_ID,
        default=URLMap.short_id(),
        validators=[
            Length(max=LENGTH_SHORT),
            Optional(),
            Regexp(REGULAR_EXPRESSION, message=ERROR_VALIDATE_SHORT)
        ]
    )
    submit = SubmitField(SUBMIT)
