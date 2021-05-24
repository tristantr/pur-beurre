from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from django.contrib import auth
from django.contrib.messages import get_messages
from accounts.forms import CreateUserForm
from django.contrib.auth import get_user_model

from django.core import mail 


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {"email": "user@gmail.com", "password": "password"}
        self.user = User.objects.create_user(**self.credentials)
        return super().setUp()


class RegisterTest(BaseTest):
    def test_register_page_url(self):
        """ Get correct status code and template when calling the URL"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_form(self):
        """Test that the CreateUserForm is valid"""
        data = {
            "email": "testseleniumy345@gmail.com",
            "password1": "VendalTest",
            "password2": "VendalTest",
        }
        form = CreateUserForm(data)

        self.assertTrue(form.is_valid())

    def test_email_required(self):
        """ An error occurs if a user does not register with an email"""
        data = {
            "email": "test",
            "password1": "VendalTest",
            "password2": "VendalTesto",
        }
        form = CreateUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors.keys())
        self.assertEqual(
            form.errors["email"][0],
            "Enter a valid email address.")

    def test_password_dont_match(self):
        """Test that an error occurs when password don't match"""
        data = {
            "email": "2@gmail.com",
            "password1": "VendalTest",
            "password2": "VendalTesto",
        }
        form = CreateUserForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors.keys())
        self.assertEqual(
            form.errors["password2"][0],
            "The two password fields didn’t match."
        )

    def test_missing_password_confirmation(self):
        """An error occurs if the conformation password is missing"""
        data = {
            "email": "2@gmail.com",
            "password1": "VendalTest",
        }
        form = CreateUserForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "password2",
            form.errors.keys())
        self.assertEqual(
            form.errors["password2"][0],
            "This field is required.")

    def test_user_is_registered(self):
        """User is correctly registered"""
        response = self.client.post(
            reverse("register"),
            data={
                "email": "test@gmail.com",
                "password1": "VendalTest",
                "password2": "VendalTest",
            },
        )

        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 2)
        self.assertTemplateUsed(response, "index.html")


class LoginTest(BaseTest):
    def test_login_page_url(self):
        """Getet correct status code and template when calling the URL"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_log_user(self):
        """The user is correctly logged after using the registering form"""
        self.client.post(reverse("login"), self.credentials)
        client_user = auth.get_user(self.client)
        self.assertTrue(client_user.is_authenticated)

    def test_user_does_not_exist(self):
        """A message is returned if email or password are incorrect"""
        response = self.client.post(
            reverse("login"),
            {"email": "not_user@gmail.com", "password": "password"}
        )
        auth.get_user(self.client)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email OR password is incorrect")


class MyAccountTest(BaseTest):
    def test_my_account_page_url_if_not_logged(self):
        """User is redirect to the login page before my_account section"""
        response = self.client.get(reverse("my_account"))
        self.assertRedirects(
            response,
            "/accounts/login?next=/accounts/my_account",
            status_code=302
        )

    def test_my_account_if_user_is_logged(self):
        """Test that the logged user can access his account section"""
        self.client.post(reverse("login"), self.credentials)
        auth.get_user(self.client)
        response = self.client.get(reverse("my_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_account.html")


class LogoutTest(BaseTest):
    def test_logout_page_url(self):
        """Test that we get a redirect status code when calling the URL"""
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_log_out_user(self):
        """User is correctly logged out after calling logout url"""
        self.client.post(reverse("login"), self.credentials)
        auth.get_user(self.client)

        self.client.get(reverse("logout"))
        client_user = auth.get_user(self.client)

        self.assertFalse(client_user.is_authenticated)

class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
        