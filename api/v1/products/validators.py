from django.core.exceptions import ValidationError
from re import compile as re_compile
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from . import models as product_models

COLOR_HEXA_RE = re_compile("#([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$")
validate_color_hexa = RegexValidator(
    COLOR_HEXA_RE,
    _("Enter a valid hexa color, eg. #00000000"), "invalid"
)


def active_and_not_deleted_product_item(product_item_id):
    product_item = product_models.ProductItem.objects.get(pk=product_item_id)
    if not product_item.is_active or product_item.is_deleted:
        raise ValidationError('object is not active')


def active_and_not_deleted_product(product_id):
    product = product_models.Product.objects.get(pk=product_id)
    if not product.is_active or product.is_deleted:
        raise ValidationError('object is not active')


def active_category(cat_id):
    cat = product_models.Category.objects.get(pk=cat_id)
    if not cat.is_active:
        raise ValidationError('object is not active')


def active_brand(brand_id):
    brand = product_models.Brand.objects.get(pk=brand_id)
    if not brand.is_active:
        raise ValidationError('object is not active')


def active_manufacturer(manufacturer_id):
    manufacturer = product_models.ProductManufacturer.objects.get(pk=manufacturer_id)
    if not manufacturer.is_active:
        raise ValidationError('object is not active')


def active_product_size(product_size_id):
    product_size = product_models.ProductSize.objects.get(pk=product_size_id)
    if not product_size.is_active:
        raise ValidationError('object is not active')


def active_product_color(product_color_id):
    product_color = product_models.ProductColor.objects.get(pk=product_color_id)
    if not product_color.is_active:
        raise ValidationError('object is not active')
