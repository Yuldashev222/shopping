from django.db import models

from api.v1.products.models import Product
from api.v1.accounts.models import Client


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Client, models.PROTECT, related_name='comments')

    text = models.CharField(max_length=400)

    def __str__(self):
        return f"Comment: in {self.author}"
