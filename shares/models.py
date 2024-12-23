import secrets
import string
from typing import Any, Dict, Self

from django.contrib.auth import get_user_model
from django.db import models
from django.http import HttpRequest
from django.utils import timezone


SLUG_CHARACTERS = string.ascii_letters + string.digits


def default_slug() -> str:
    return "".join(secrets.choice(SLUG_CHARACTERS) for _ in range(15))


def get_ip_from_meta(meta: Dict[str, Any]) -> str:
    x_forwarded_for = meta.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1]
    else:
        ip = meta.get("REMOTE_ADDR", "")
    return ip


class Share(models.Model):
    id = models.BigAutoField(primary_key=True)
    download_enabled = models.BooleanField("Enable Download", default=True)
    force_download = models.BooleanField("Force Downloading", default=True)
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

    @property
    def full_path(self):
        return f"{self.directory}/{self.name}" \
            if self.directory else self.name

    def __str__(self):
        return "Share(" \
            f"id={self.id}," \
            f"download_enabled={self.download_enabled}," \
            f"force_download={self.force_download}," \
            f"slug={self.slug}," \
            f"directory={self.directory}," \
            f"name={self.name}," \
            f"user={self.user}" \
            ")"


class DownloadLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField("Timestamp")
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    ip = models.CharField("IP Address", max_length=50, blank=True)
    user_agent = models.TextField("User Agent", blank=True)
    range_header = models.CharField(
        "HTTP Range Header", max_length=100, blank=True)

    def __str__(self):
        return "DownloadLog(id={}, timestamp={}, share={}, ip={}, user_agent={}, range_header={})".format(
            self.pk,
            self.timestamp,
            self.share.full_path,
            self.ip,
            self.user_agent,
            self.range_header,
        )

    @classmethod
    def create_from_request_and_share(cls, request: HttpRequest, share: Share) -> Self:
        return cls.objects.create(
            timestamp=timezone.now(),
            share=share,
            ip=get_ip_from_meta(request.META),
            user_agent=request.headers.get("User-Agent", ""),
            range_header=request.headers.get("Range", ""),
        )
