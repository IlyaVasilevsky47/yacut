from flask_wtf import FlaskForm
from settings import Config
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

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
            Length(max=Config.LONG_LINK),
            DataRequired(message=ERROR_REQUIRED),
        ]
    )
    custom_id = URLField(
        CUSTOM_ID,
        validators=[
            Length(max=Config.LENGTH_SHORT),
            Optional(),
            Regexp(Config.REGULAR_EXPRESSION, message=ERROR_VALIDATE_SHORT)
        ]
    )
    submit = SubmitField(SUBMIT)
