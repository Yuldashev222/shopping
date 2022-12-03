from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

from api.v1.delivery.models import Delivery


class Command(BaseCommand):
    def handle(self, *args, **options):
        deliveries = []
        creator = get_user_model().objects.filter(is_superuser=True)[0]
        if not creator:
            creator = get_user_model().objects.create_superuser(
                first_name='super',
                last_name='user',
                email=settings.BASE_USER_EMAIL,
                phone_number=settings.BASE_USER_PHONE_NUMBER,
                password=settings.BASE_USER_PASSWORD
            )
        for i in range(1, 100001):
            deliveries.append(
                Delivery(
                    title=f'Title No {i}',
                    price=5 * (i + 1),
                    delivery_time_in_hour=2 * i * .4,
                    info_on_delivery_time=f'khans iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd iuhasidu hasiudh iausdhiukjhuahsd iuhasidu hasiudh '
                                          f'iausdhiukjhuahsd {i}',
                    creator_id=creator.id,
                    is_deleted=i % 2,
                    is_active=(i + 1) % 2
                )
            )
            self.stdout.write(f'created delivery No {i}')
        Delivery.objects.bulk_create(deliveries)
