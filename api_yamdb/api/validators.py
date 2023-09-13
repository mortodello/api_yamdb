import re

from datetime import date
from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError('Этот username запрещён!')
    for ch in value:
        if not re.search(r'^[\w.@+-]+\Z$', ch):
            raise ValidationError(f'Символ {ch} запрещён в username.')
    return value


def year_validator(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError('Произведения из будущего не принимаются!')
