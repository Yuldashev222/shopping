from django.core.exceptions import ValidationError
from re import compile as re_compile
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from . import models as product_models

COLOR_HEXA_RE = re_compile("#([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$")
validate_color_hexa = RegexValidator(
    COLOR_HEXA_RE,
    _("Enter a valid hexa color, eg. #FFFFFF00"), "invalid"
)


def active_and_not_deleted_product_item(product_item_id):
    product_item = product_models.ProductItem.objects.get(pk=product_item_id)
    if not product_item.active_object():
        raise ValidationError('object is not active')


def active_and_not_deleted_product(product_id):
    product = product_models.Product.objects.get(pk=product_id)
    if not product.active_object():
        raise ValidationError('object is not active')


def active_and_not_deleted_category(cat_id):
    cat = product_models.ProductCategory.objects.get(pk=cat_id)
    if not cat.active_object():
        raise ValidationError('object is not active')


def active_and_not_deleted_brand(brand_id):
    brand = product_models.Brand.objects.get(pk=brand_id)
    if not brand.active_object():
        raise ValidationError('object is not active')


def active_manufacturer(manufacturer_id):
    manufacturer = product_models.ProductManufacturer.objects.get(pk=manufacturer_id)
    if not manufacturer.active_object():
        raise ValidationError('object is not active')


def active_product_size(product_size_id):
    product_size = product_models.ProductSize.objects.get(pk=product_size_id)
    if not product_size.active_object():
        raise ValidationError('object is not active')


def active_product_color(product_color_id):
    product_color = product_models.ProductColor.objects.get(pk=product_color_id)
    if not product_color.active_object():
        raise ValidationError('object is not active')
