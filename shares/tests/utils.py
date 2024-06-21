import random
import string

from django.contrib.auth.models import User


def get_user() -> User:
    user, _ = User.objects.get_or_create(username="test")
    return user


def create_random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=20))
