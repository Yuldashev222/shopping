

def upload_location_product_image(instance, image):
    """
    Image joylashgan address | format: (media)/products/product/product_item/images/image
    """
    return f'products/{instance.product_item.product.name}/{instance.product_item.name}/images/{image}'
