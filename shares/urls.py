from django.urls import path

from . import views

app_name = "shares"
urlpatterns = [
    path("", views.index, name="index"),
    path("files", views.files, name="files"),
    path("shares", views.shares, name="shares"),
    path("shares/new", views.new_share, name="new_share"),
]
