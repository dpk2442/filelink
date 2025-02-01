from pathlib import Path
from unittest import mock

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from shares import models
from ..utils import create_random_string, get_user


class TestDownloadShare(TestCase):

    @mock.patch("django_sendfile.sendfile")
    def test_valid_link(self, mock_sendfile):
        mock_sendfile.return_value = HttpResponse()
        mock_files_path = Path(__file__).resolve().parent

        share = models.Share.objects.create(
            directory=create_random_string(),
            name=create_random_string(),
            user=get_user(),
        )

        with self.settings(FL_FILES_PATH=mock_files_path):
            response = self.client.get(
                reverse("shares:download_share", args=(share.slug,)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers.get("Accept-Ranges"), "bytes")

        self.assertEqual(
            len(models.DownloadLog.objects.filter(share=share)), 1)

        mock_sendfile.assert_called_once_with(
            mock.ANY,
            (mock_files_path / share.directory / share.name).as_posix(),
            attachment=True,
            attachment_filename=share.name)

    def test_invalid_link(self):
        response = self.client.get(
            reverse("shares:download_share", args=("slug",)))
        self.assertEqual(response.status_code, 404)

    def test_cannot_download_disabled_share(self):
        share = models.Share.objects.create(
            download_enabled=False,
            directory=create_random_string(),
            name=create_random_string(),
            user=get_user()
        )

        response = self.client.get(
            reverse("shares:download_share", args=(share.slug,)))
        self.assertEqual(response.status_code, 404)

    @mock.patch("django_sendfile.sendfile")
    def test_valid_without_force_download(self, mock_sendfile):
        mock_sendfile.return_value = HttpResponse()
        mock_files_path = Path(__file__).resolve().parent

        share = models.Share.objects.create(
            directory=create_random_string(),
            name=create_random_string(),
            user=get_user(),
            force_download=False,
        )

        with self.settings(FL_FILES_PATH=mock_files_path):
            response = self.client.get(
                reverse("shares:download_share", args=(share.slug,)))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers.get("Accept-Ranges"), "bytes")

        self.assertEqual(
            len(models.DownloadLog.objects.filter(share=share)), 1)

        mock_sendfile.assert_called_once_with(
            mock.ANY,
            (mock_files_path / share.directory / share.name).as_posix(),
            attachment=False,
            attachment_filename=share.name)
