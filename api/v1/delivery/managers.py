from django.db.models.manager import Manager
from django.db.models import Q, F
from datetime import date


class ActiveDeliveryManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_active=True) & Q(is_deleted=False)
            # (
            #         Q(available_from_date__isnull=True)
            #         |
            #         Q(available_to_date__isnull=False) &
            #         Q(available_to_date__lte=date.today())
            #         |
            #         Q(available_to_date__isnull=True) &
            #         Q(available_from_date__isnull=False) &
            #         Q(available_from_date__gte=date.today())
            # )
        )  # last
