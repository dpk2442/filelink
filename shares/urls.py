from django.urls import path

from . import views

app_name = "shares"
urlpatterns = [
    path("", views.index, name="index"),
]
