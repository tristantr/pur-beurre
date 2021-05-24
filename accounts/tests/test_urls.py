from django.test import SimpleTestCase
from django.urls import resolve, reverse
from accounts.views import register_user, log_user, get_my_account, logout_user
from django.contrib.auth import views as auth_views

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

    def test_password_reset_url_is_resolved(self):
        url = reverse("password_reset")
        resolver = resolve(url)
        self.assertEquals(resolver.func.__name__, auth_views.PasswordResetView.as_view().__name__)

    def test_password_reset_done_is_resolved(self):
        url = reverse("password_reset_done")
        resolver = resolve(url)
        self.assertEquals(resolver.func.__name__, auth_views.PasswordResetDoneView.as_view().__name__)

    def test_password_reset_confirm_is_resolved(self):
        url = reverse("password_reset_confirm", kwargs={"uidb64":'srgfvzsqefs',"token": 1})
        resolver = resolve(url)
        self.assertEquals(resolver.func.__name__, auth_views.PasswordResetConfirmView.as_view().__name__)

    def test_password_reset_complete_is_resolved(self):
        url = reverse("password_reset_complete")
        resolver = resolve(url)
        self.assertEquals(resolver.func.__name__, auth_views.PasswordResetCompleteView.as_view().__name__)

