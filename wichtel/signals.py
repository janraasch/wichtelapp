from allauth.account.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import Event


@receiver(user_logged_in)
def on_user_logged_in(request, user, **kwargs):
    Event.objects.create(user=user, name='user.logged_in')


@receiver(user_logged_out)
def on_user_logged_out(request, user, **kwargs):
    Event.objects.create(user=user, name='user.logged_out')
