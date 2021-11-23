from django.apps import AppConfig


class CustomermanageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CustomerManage'

    def ready(self):
        import CustomerManage.signals
