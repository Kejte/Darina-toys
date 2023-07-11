from django.apps import AppConfig
from django.core.signals import setting_changed


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = 'Магазин'

    def ready(self):
        from .signal import create_profile
