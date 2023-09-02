# валидатор для года на уровне модели
from datetime import date

from django.core.exceptions import ValidationError


# На вход функция будет принимать год в формате integer.
def year_validator(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError('Произведения из будущего не принимаются!')
