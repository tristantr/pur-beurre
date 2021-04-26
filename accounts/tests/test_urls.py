from django.test import SimpleTestCase
from django.urls import resolve, reverse
from accounts.views import register_user, log_user, get_my_account, logout_user


class TestUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, register_user)

    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, log_user)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logout_user)

    def test_my_account_url_is_resolved(self):
        url = reverse("my_account")
        self.assertEquals(resolve(url).func, get_my_account)
