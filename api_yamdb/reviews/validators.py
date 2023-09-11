from datetime import date

from django.core.exceptions import ValidationError


def year_validator(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError('Произведения из будущего не принимаются!')
