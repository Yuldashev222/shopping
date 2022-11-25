from django.forms import model_to_dict
from django.conf import settings
from django.db import transaction
from django.db.models.signals import pre_delete, post_save, pre_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

from .enums import CustomUserRole
from .models import UserDetailOnDelete


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@on_transaction_commit
def add_to_group(instance, *args, **kwargs):
    if kwargs.get('created', False):
        if instance.role != CustomUserRole.developer.name:
            group = Group.objects.get_by_natural_key(f'{instance.role}s')
            instance.groups.set([group])
        else:
            group, group_created = Group.objects.get_or_create(name='developers')
            group.permissions.set(list(Permission.objects.all()))
            instance.groups.set([group])


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def save_user_data(instance, *args, **kwargs):
    user_detail, created = UserDetailOnDelete.objects.get_or_create(
        phone_number=instance.phone_number,
        email=instance.email,
        date_joined=instance.date_joined
    )
    if created:
        user_detail.role = instance.role
        user_detail.first_name = instance.first_name
        user_detail.last_name = instance.last_name
        user_detail.is_staff = instance.is_staff
        user_detail.save()

    if instance.role != CustomUserRole.client.name:
        users = instance.customuser_set.all()
        brands = instance.brand_set.all()
        cats = instance.category_set.all()
        products = instance.product_set.all()
        product_items = instance.productitem_set.all()
        deliveries = instance.delivery_set.all()
        discounts = instance.discount_set.all()
        discount_items = instance.discountitem_set.all()

        if users.exists():
            users.update(creator_detail_on_delete_id=user_detail.id)

        if brands.exists():
            brands.update(creator_detail_on_delete_id=user_detail.id)

        if cats.exists():
            cats.update(creator_detail_on_delete_id=user_detail.id)

        if products.exists():
            products.update(creator_detail_on_delete_id=user_detail.id)

        if product_items.exists():
            product_items.update(creator_detail_on_delete_id=user_detail.id)

        if deliveries.exists():
            deliveries.update(creator_detail_on_delete_id=user_detail.id)

        if discounts.exists():
            discounts.update(creator_detail_on_delete_id=user_detail.id)

        if discount_items.exists():
            discount_items.update(adder_detail_on_delete_id=user_detail.id)

        if user_detail.role == CustomUserRole.vendor.name:
            orders = instance.vendor_orders.all()

            if orders.exists():
                orders.update(vendor_detail_on_delete_id=user_detail.id)

    else:
        comments = instance.productcomment_set.all()
        orders = instance.client_orders.all()

        if comments.exists():
            comments.update(client_detail_on_delete_id=user_detail.id)

        if orders.exists():
            orders.update(client_detail_on_delete_id=user_detail.id)
