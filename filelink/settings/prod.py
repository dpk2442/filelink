import os

from .base import *


DEBUG = False

ALLOWED_HOSTS = ["*"]

# SSL Settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Enable secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Application settings

# Use project folder as fallback for local testing
FL_FILES_PATH = Path(os.environ.get("FL_FILES_PATH") or "/files").resolve()

# Sendfile settings

SENDFILE_ROOT = FL_FILES_PATH
SENDFILE_BACKEND = "django_sendfile.backends.xsendfile"
