from django.test import TestCase
from accounts.models import User


class TestModels(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create(
            email="regular_user@gmail.com",
            is_active=True,
            staff=False,
            admin=False,
        )

    def test_str(self):
        self.assertEquals(
            str(self.regular_user),
            "regular_user@gmail.com"
            )

    def test_get_full_name(self):
        self.assertEquals(
            self.regular_user.get_full_name(),
            "regular_user@gmail.com"
            )

    def test_get_short_name(self):
        self.assertEquals(
            self.regular_user.get_short_name(),
            "regular_user@gmail.com"
            )

    def test_regular_user_is_not_staff(self):
        self.assertEquals(self.regular_user.is_staff, False)

    def test_regular_user_is_not_admin(self):
        self.assertEquals(self.regular_user.is_admin, False)
