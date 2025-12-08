from django.apps import AppConfig


class WichtelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wichtel"

    def ready(self):
        from allauth.account.signals import user_logged_in, user_logged_out

        from .signals import on_user_logged_in, on_user_logged_out

        user_logged_in.connect(on_user_logged_in)
        user_logged_out.connect(on_user_logged_out)
