from django.urls import path

from . import views

app_name = "wichtel"
urlpatterns = [
    path('', views.wishlist, name='wishlist'),
]
