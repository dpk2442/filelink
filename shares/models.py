import secrets

from django.contrib.auth import get_user_model
from django.db import models


def default_slug():
    return secrets.token_urlsafe(15)


class Share(models.Model):
    id = models.BigAutoField(primary_key=True)
    slug = models.SlugField("Slug", max_length=15,
                            unique=True, default=default_slug)
    directory = models.CharField(
        "Containing Directory", max_length=200, blank=True)
    name = models.CharField("Shared File Name", max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("directory", "name"), name="unique_path")
        ]

    def __str__(self):
        return f"Share(id={self.id}, slug={self.slug}, directory={self.directory}, name={self.name}, user={self.user})"
