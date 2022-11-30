

def upload_location_product_image(instance, image):
    """
    Path to image | format: (media)/products/product/product_item/images/image
    """
    path = f'products/{instance.product.name}/'
    if instance.name:
        path = f'products/{instance.product.name}/{instance.name}/'
    if instance.main_image == image:
        return path + f'images/main_image/{image}'
    return path + f'images/{image}'
