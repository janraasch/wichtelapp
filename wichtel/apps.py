from django.apps import AppConfig


class WichtelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wichtel"

    def ready(self):
        pass
