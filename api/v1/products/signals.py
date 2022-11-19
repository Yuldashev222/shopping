# from django.db.models import signals
# from django.dispatch import receiver
# from django.db import transaction
#
# from api.v1.accounts.models import Manager
# from .models import Brand, CreatorDetail
#
#
# @receiver(signals.pre_delete, sender=Manager)
# def save_user_data(sender, **kwargs):
#     instance = kwargs.get('instance')
#     brands = instance.brand_set.all()
#     print(brands)
#     print(sender, kwargs)
#     print()
