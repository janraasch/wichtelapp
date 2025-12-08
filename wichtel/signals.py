from .models import Event


def on_user_logged_in(request, user, **kwargs):
    Event.objects.create(user=user, name="user.logged_in")


def on_user_logged_out(request, user, **kwargs):
    Event.objects.create(user=user, name="user.logged_out")
