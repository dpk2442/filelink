from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from shares import models
from .utils import get_user


class TestShare(TestCase):

    def test_full_path(self):
        self.assertEqual(models.Share(
            directory="", name="name").full_path, "name")
        self.assertEqual(models.Share(
            directory="dir", name="name").full_path, "dir/name")


class TestDownloadLog(TestCase):

    def test_get_ip_from_meta(self):
        self.assertEqual(models.get_ip_from_meta({}), "")
        self.assertEqual(models.get_ip_from_meta({
            "HTTP_X_FORWARDED_FOR": "forwarded",
        }), "forwarded")
        self.assertEqual(models.get_ip_from_meta({
            "REMOTE_ADDR": "addr",
        }), "addr")
        self.assertEqual(models.get_ip_from_meta({
            "HTTP_X_FORWARDED_FOR": "forwarded",
            "REMOTE_ADDR": "addr",
        }), "forwarded")

    def test_creates_object(self):
        user = get_user()
        request = HttpRequest()
        request.META["REMOTE_ADDR"] = "remote_addr"
        request.META["HTTP_USER_AGENT"] = "user_agent"
        request.META["HTTP_RANGE"] = "range"
        request.user = user
        share = models.Share.objects.create(
            directory="dir", name="name", user=user)

        now = timezone.now()
        download_log = models.DownloadLog.create_from_request_and_share(
            request, share)
        self.assertGreater(download_log.timestamp, now)
        self.assertEqual(download_log.share, share)
        self.assertEqual(download_log.ip, "remote_addr")
        self.assertEqual(download_log.user_agent, "user_agent")
        self.assertEqual(download_log.range_header, "range")

    def test_defaults_fields_to_empty(self):
        user = get_user()
        request = HttpRequest()
        request.user = user
        share = models.Share.objects.create(
            directory="dir", name="name", user=user)

        download_log = models.DownloadLog.create_from_request_and_share(
            request, share)
        self.assertEqual(download_log.ip, "")
        self.assertEqual(download_log.user_agent, "")
        self.assertEqual(download_log.range_header, "")
