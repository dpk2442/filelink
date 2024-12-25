from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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

    def test_hides_nav_links_if_not_logged_in(self):
        response = self.client.get(reverse("login"))
        self.assertNotContains(response,
                               f"<a href=\"{reverse("shares:shares")}\">Shares</a>", html=True)
        self.assertNotContains(response,
                               f"<a href=\"{reverse("shares:files")}\">Files</a>", html=True)
