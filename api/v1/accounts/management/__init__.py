from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db import transaction


@transaction.atomic
def create_default_groups(*args, **kwargs):
    for index, group_detail in enumerate(settings.USER_GROUP_PERMISSIONS_LIST, 0):
        group_name = group_detail[0].strip().lower()
        group, group_created = Group.objects.get_or_create(name=group_name)
        if group_created:
            group_permissions = settings.USER_GROUP_PERMISSIONS_LIST[index][1]
            permissions = []
            for app_label in group_permissions:
                for codename in group_permissions[app_label]:
                    print()
                    print(app_label, codename, str(codename).split('_')[1])
                    print()
                    permissions.append(
                        Permission.objects.get_by_natural_key(
                            codename=codename,
                            app_label=app_label,
                            model=str(codename).split('_')[1]
                        )
                    )
            group.permissions.set(permissions)
