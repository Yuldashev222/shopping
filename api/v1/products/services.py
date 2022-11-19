

def upload_location_product_image(instance, image):
    """
    Image joylashgan address | format: (media)/products/product/product_item/images/image
    """
    if instance.main_image == image:
        return f'products/{instance.product.name}/{instance.name}/images/main_image/{image}'
    return f'products/{instance.product.name}/{instance.name}/images/{image}'
