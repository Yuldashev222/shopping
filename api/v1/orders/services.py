def upload_location_order_contract_file(instance, file):
    """
    Faylga joylashgan address | format: (media)/orders/client/Contract files/file
    """
    return f'Orders/%Y-%m-%d/{instance.client}/Contract_files/{file}'
