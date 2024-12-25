import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from shares import models


class AuthenticatedTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user, _ = User.objects.get_or_create(username="test")
        self.client.force_login(self.user)

    def create_share_in_db(self, with_directory=True) -> models.Share:
        return models.Share.objects.create(
            directory=create_random_string() if with_directory else "",
            name=create_random_string(),
            user=self.user,
        )


def get_user() -> User:
    user, _ = User.objects.get_or_create(username="test")
    return user


def create_random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=20))
