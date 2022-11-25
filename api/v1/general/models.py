from django.db import models
from django.conf import settings

from api.v1.accounts.models import CustomUser
from api.v1.accounts.validators import is_director, active_and_not_deleted_user


class ShopAbout(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='Shop_About/logotype/')

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        validators=[active_and_not_deleted_user, is_director],
    )
