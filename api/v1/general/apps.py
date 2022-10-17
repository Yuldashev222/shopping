from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.general'
    label = 'general'
    #
    # def ready(self):
    #     from . import signals
