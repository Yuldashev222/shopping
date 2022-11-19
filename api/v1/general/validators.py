from django.core.exceptions import ValidationError
from datetime import datetime, date


def validate_date(model_date):
    if model_date <= date.today():
        raise ValidationError('date must be greater than today date')
