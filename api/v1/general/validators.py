from django.core.exceptions import ValidationError


def active_relation(object):
    try:
        if not (object.is_active and object.is_deleted):
            raise ValidationError('No active relation object')
    except ValueError:
        if not object.is_deleted:
            raise ValidationError('No active relation object')
    except ValueError:
        if not object.is_active:
            raise ValidationError('No active relation object')
