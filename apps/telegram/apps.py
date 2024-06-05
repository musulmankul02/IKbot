from django.apps import AppConfig

class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.telegram'

    def ready(self):
        import apps.telegram.utils.signals
