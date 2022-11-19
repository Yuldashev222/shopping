from django.db import models

from api.v1.accounts.enums import CustomUserRole
from api.v1.accounts.models import Director


class ShopAbout(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='shop/logo/')

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    creator = models.ForeignKey(
        Director,
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True, 'is_deleted': False, 'role': CustomUserRole.director.name},
    )
