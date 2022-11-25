def upload_location_discount_image(instance, image):
    """
    Rasmga joylashgan address | format: (media)/discounts/discount/images/image
    """
    return f'Discounts/%Y-%m-%d/{instance.title}/images/{image}'


def upload_location_discount_file(instance, file):
    """
    Faylga joylashgan address | format: (media)/discounts/discount/files/file
    """
    return f'Discounts/%Y-%m-%d/{instance.title}/files/{file}'
