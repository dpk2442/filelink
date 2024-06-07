from pathlib import Path
from typing import cast

from django.apps import AppConfig
from django.conf import settings


class SharesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shares"
