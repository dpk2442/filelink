from pathlib import Path
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shares import forms, models
from shares.exceptions import InvalidRequestPathException
from .utils import create_random_string


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


class LoginTest(TestCase):

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("shares:files"))
        self.assertRedirects(response,
                             f"{reverse("login")}?next={reverse("shares:files")}")

    def test_shows_logout_form_if_logged_in(self):
        user, _ = User.objects.get_or_create(username="test")
        self.client.force_login(user)
        response = self.client.get(reverse("shares:files"))
        self.assertContains(
            response,
            f"<form action=\"{reverse("logout")}\" method=\"post\">")


class TestGetFiles(AuthenticatedTestCase):

    @mock.patch("shares.actions.get_directories_and_files")
    def test_displays_files_and_directories_in_order(self, mock_get_directories_and_files):
        mock_get_directories_and_files.return_value = (
            [dict(name="dir1", path="dir1"), dict(name="dir2", path="dir2")],
            [dict(name="file1", path="file1"),
             dict(name="file2", path="file2")],
            None,
        )

        files_url = reverse("shares:files")
        new_share_url = reverse("shares:new_share")
        response = self.client.get(files_url)
        self.assertContains(response, "<title>Browse Files | FileLink</title>")
        self.assertNotContains(response, "Parent")
        self.assertContains(response, f"""
        <tr><td><a href="{files_url}?path=dir1">dir1</a></td><td></td></tr>
        <tr><td><a href="{files_url}?path=dir2">dir2</a></td><td></td></tr>
        <tr><td>file1</td><td><a href="{new_share_url}?path=file1">Share</a></td></tr>
        <tr><td>file2</td><td><a href="{new_share_url}?path=file2">Share</a></td></tr>
                            """, html=True)

    @mock.patch("shares.actions.get_directories_and_files")
    def test_renders_parent_path_when_provided(self, mock_get_directories_and_files):
        mock_get_directories_and_files.return_value = (
            [],
            [],
            Path("parent"),
        )

        files_url = reverse("shares:files")
        response = self.client.get(files_url)
        self.assertContains(response,
                            f"<a href=\"{files_url}?path=parent\">Parent</a>",
                            html=True)

    @mock.patch("shares.actions.get_directories_and_files")
    def test_redirects_when_get_directories_and_files_raises(self, mock_get_directories_and_files):
        mock_get_directories_and_files.side_effect = InvalidRequestPathException

        files_url = reverse("shares:files")
        response = self.client.get(files_url)
        self.assertRedirects(response, files_url,
                             fetch_redirect_response=False)


class TestNewShare(AuthenticatedTestCase):

    def test_get(self):
        response = self.client.get(reverse("shares:new_share"))
        self.assertContains(response, "Containing Directory")
        self.assertContains(response, "File Name")
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
            <tr><td>{share1.name}</td><td>{share1.slug}</td><td></td></tr>
            <tr><td>{share2.directory}/{share2.name}</td><td>{share2.slug}</td><td></td></tr>
        """, html=True)


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
