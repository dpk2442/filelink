from unittest import mock

from django.urls import reverse

from shares import forms, models
from ..utils import AuthenticatedTestCase


class ShareEditViewTests(AuthenticatedTestCase):

    def test_get(self):
        share = self.create_share_in_db()
        response = self.client.get(
            reverse("shares:edit_share", args=(share.id,)))
        self.assertContains(response, share.directory)
        self.assertContains(response, share.name)

        form = response.context["form"]
        self.assertIsNotNone(form)
        self.assertIsInstance(form, forms.ShareForm)
        self.assertEqual(form.instance, share)

    def test_get_does_not_exist(self):
        response = self.client.get(reverse("shares:edit_share", args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_post_valid(self):
        share = self.create_share_in_db()
        response = self.client.post(reverse("shares:edit_share", args=(share.id,)), dict(
            directory="dir",
            name="test.txt",
        ))
        self.assertRedirects(response, reverse(
            "shares:index"), fetch_redirect_response=False)

        db_share = models.Share.objects.get(pk=share.id)
        self.assertEqual(self.user, db_share.user)
        self.assertEqual("dir", db_share.directory)
        self.assertEqual("test.txt", db_share.name)

    def test_post_invalid(self):
        share = self.create_share_in_db()
        response = self.client.post(reverse("shares:edit_share", args=(share.id,)), dict(
            directory="new_dir",
            name="",
        ))

        self.assertContains(response, "This field is required.", 1)
        db_share = models.Share.objects.get(pk=share.id)
        self.assertNotEqual("new_dir", db_share.directory)
