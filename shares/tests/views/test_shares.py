from unittest import mock

from django.urls import reverse

from shares import forms, models
from ..utils import AuthenticatedTestCase, create_random_string


class TestNewShare(AuthenticatedTestCase):

    def test_get(self):
        response = self.client.get(reverse("shares:new_share"))
        self.assertContains(response, "Containing Directory")
        self.assertContains(response, "File Name")
        self.assertContains(response, "Enable Download")
        self.assertContains(
            response,
            "<input type='checkbox' name='download_enabled' id='id_download_enabled' checked>",
            html=True)
        self.assertContains(response, "Force Downloading")
        self.assertContains(
            response,
            "<input type='checkbox' name='force_download' id='id_force_download' checked>",
            html=True)
        self.assertIsNotNone(response.context["form"])
        self.assertIsInstance(response.context["form"], forms.ShareForm)

    def test_post_valid(self):
        share_directory = create_random_string()
        share_name = create_random_string()
        response = self.client.post(reverse("shares:new_share"), dict(
            directory=share_directory,
            name=share_name,
        ))
        self.assertRedirects(response, reverse(
            "shares:index"), fetch_redirect_response=False)

        share = models.Share.objects.get(
            directory=share_directory, name=share_name)
        self.assertEqual(share.directory, share_directory)
        self.assertEqual(share.name, share_name)
        self.assertTrue(share.slug)

    def test_post_invalid(self):
        response = self.client.post(reverse("shares:new_share"))
        self.assertContains(response, "This field is required.")

    def test_requires_unique_path(self):
        share_directory = create_random_string()
        share_name = create_random_string()
        models.Share.objects.create(
            directory=share_directory, name=share_name, user=self.user)

        response = self.client.post(reverse("shares:new_share"), dict(
            directory=share_directory,
            name=share_name,
        ))
        self.assertContains(
            response, "Share with this Containing Directory and Shared File Name already exists.")


class TestGetShares(AuthenticatedTestCase):

    def test_displays_shares(self):
        share1 = self.create_share_in_db(with_directory=False)
        share2 = self.create_share_in_db()
        response = self.client.get(reverse("shares:shares"))
        self.assertContains(response, f"""
            <tr>
                <td>{share1.name}</td>
                <td><a href="{reverse("shares:download_share", args=(share1.slug,))}">Direct Download</a></td>
                <td>
                    <a href="{reverse("shares:share", args=(share1.id,))}">Manage</a>
                    <a href="{reverse("shares:edit_share", args=(share1.id,))}">Edit</a>
                    <a href="{reverse("shares:delete_share", args=(share1.id,))}">Delete</a>
                </td>
            </tr>
            <tr>
                <td>{share2.directory}/{share2.name}</td>
                <td><a href="{reverse("shares:download_share", args=(share2.slug,))}">Direct Download</a></td>
                <td>
                    <a href="{reverse("shares:share", args=(share2.id,))}">Manage</a>
                    <a href="{reverse("shares:edit_share", args=(share2.id,))}">Edit</a>
                    <a href="{reverse("shares:delete_share", args=(share2.id,))}">Delete</a>
                </td>
            </tr>
        """, html=True)

    def test_displays_empty_shares(self):
        response = self.client.get(reverse("shares:shares"))
        self.assertContains(response, "<tbody></tbody>", html=True)


class TestGetShare(AuthenticatedTestCase):

    def test_displays_share(self):
        share = self.create_share_in_db()
        response = self.client.get(reverse("shares:share", args=(share.id,)))
        self.assertContains(response, f"<a href=\"{reverse(
            "shares:delete_share", args=(share.id,))}\">Delete Share</a>", html=True)
        self.assertContains(response, f"<a href=\"{reverse(
            "shares:download_share", args=(share.slug,))}\">Direct Download</a>", html=True)
        self.assertContains(response, f"{share.directory}/{share.name}")


class TestDeleteShare(AuthenticatedTestCase):

    def test_get(self):
        share = self.create_share_in_db()
        response = self.client.get(
            reverse("shares:delete_share", args=(share.id,)))
        self.assertContains(
            response, f"Are you sure you want to delete \"{share.directory}/{share.name}\"?")

    def test_get_does_not_exist(self):
        response = self.client.get(
            reverse("shares:delete_share", args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        share = self.create_share_in_db()
        response = self.client.post(
            reverse("shares:delete_share", args=(share.id,)))
        self.assertRedirects(response, reverse(
            "shares:index"), fetch_redirect_response=False)

        self.assertQuerySetEqual(models.Share.objects.filter(id=share.id), [])


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

    def test_can_edit_share_settings(self):
        share = self.create_share_in_db()
        response = self.client.post(reverse("shares:edit_share", args=(share.id,)), dict(
            directory=share.directory,
            name=share.name,
            download_enabled=not share.download_enabled,
            force_download=not share.force_download,
        ))
        self.assertRedirects(response, reverse(
            "shares:index"), fetch_redirect_response=False)

        db_share = models.Share.objects.get(pk=share.id)
        self.assertEqual(not share.download_enabled, db_share.download_enabled)
        self.assertEqual(not share.force_download, db_share.force_download)
