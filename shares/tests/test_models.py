from django.test import TestCase

from shares import models


class TestShare(TestCase):

    def test_full_path(self):
        self.assertEqual(models.Share(
            directory="", name="name").full_path, "name")
        self.assertEqual(models.Share(
            directory="dir", name="name").full_path, "dir/name")
