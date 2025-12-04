from django.urls import path

from . import views

app_name = "wichtel"
urlpatterns = [
    path("", views.home, name="home"),
]
