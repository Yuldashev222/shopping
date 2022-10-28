from datetime import datetime, date
from django.core.exceptions import ValidationError


def date_from_today_date(value):
    today_date = datetime.today()
    error = None
    try:
        if value < today_date:
            error = 'the available date must not be less than today\'s date'
    except ValidationError:
        today_date = date.today()
        if value < today_date:
            error = 'the available date must not be less than today\'s date'
    if error:
        raise ValidationError(error)
