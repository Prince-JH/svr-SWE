from django.apps import AppConfig


class SweConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'swe'

    def ready(self):
        import utils.signal_receivers
        pass
