from datetime import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    if value < 1500:
        raise ValidationError(
            (f'Год издания не может быть меньше или равным "1500". '
             f'Введите корректное значение.'),
            params={'value': value},
        )
    if value > datetime.now().year:
        raise ValidationError(
            (f'Год издания не может быть больше текущего. '
             f'Введите корректное значение.'),
            params={'value': value},
        )
