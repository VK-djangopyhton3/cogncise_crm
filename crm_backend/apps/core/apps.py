from django.apps import AppConfig
from .settings import CUSER_SETTINGS


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = CUSER_SETTINGS['app_verbose_name']

    def ready(self):
        import core.signals
