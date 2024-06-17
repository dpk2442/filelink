from pathlib import Path
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from shares import views
from shares.exceptions import InvalidRequestPathException


class TestGetFiles(TestCase):

    @mock.patch("shares.actions.get_directories_and_files")
    def test_displays_files_and_directories_in_order(self, mock_get_directories_and_files):
        mock_get_directories_and_files.return_value = (
            [dict(name="file1"), dict(name="file2")],
            [dict(name="dir1", path="dir1"), dict(name="dir2", path="dir2")],
            None,
        )

        files_url = reverse("shares:files")
        response = self.client.get(files_url)
        self.assertContains(response, "<title>Browse Files | FileLink</title>")
        self.assertNotContains(response, "Parent")
        self.assertContains(response, f"""
        <tr><td><a href="{files_url}?path=dir1">dir1</a></td></tr>
        <tr><td><a href="{files_url}?path=dir2">dir2</a></td></tr>
        <tr><td>file1</td></tr>
        <tr><td>file2</td></tr>
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
