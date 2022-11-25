from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.accounts'
    label = 'accounts'

    def ready(self):
        from . import signals

        from django.db.models.signals import post_migrate
        from .management import create_default_groups
        post_migrate.connect(create_default_groups, dispatch_uid='api.v1.accounts.management.create_default_groups')
