def upload_location_delivery_image(instance, image):
    """
    Rasmga joylashgan address | format: (media)/deliveries/delivery/images/image
    """
    return f'Discounts/%Y-%m-%d/{instance.title}/images/{image}'


def upload_location_delivery_file(instance, file):
    """
    Faylga joylashgan address | format: (media)/deliveries/delivery/files/file
    """
    return f'Discounts/%Y-%m-%d/{instance.title}/files/{file}'
