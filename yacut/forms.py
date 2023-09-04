from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .models import LONG_LINK, SHORT_LINK, URLMap

ORIGINAL_LINK = 'Длинная ссылка'
CUSTOM_ID = 'Ваш вариант короткой ссылки'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK,
        validators=[Length(max=LONG_LINK), DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        CUSTOM_ID,
        validators=[Length(max=SHORT_LINK), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id):
        if URLMap.validate_short(self.custom_id.data):
            raise ValidationError(
                'Доступные символы: большие латинские буквы,' +
                'маленькие латинские буквы, цифры в диапазоне от 0 до 9.'
            )