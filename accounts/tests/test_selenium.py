from selenium import webdriver


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

from accounts.models import User
from django.contrib.auth import get_user_model


class TestAccount(StaticLiveServerTestCase):
    def setUp(self):
        PATH = "/Users/josselinlecuyer/Desktop/Formation developpeur Python/PROJETS/Projet 8/Livrable/chromedriver"
        self.browser = webdriver.Chrome(PATH)

    def tearDown(self):
        self.browser.close()

    def test_register(self):
        register_url = self.live_server_url + reverse("register") + "?next=/"

        # Registration
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("register").click()

        self.assertEquals(self.browser.current_url, register_url)

        email_input = self.browser.find_element_by_id("email")
        email_input.send_keys("sel@gmail.com")

        password1_input = self.browser.find_element_by_id("password1")
        password1_input.send_keys("selenium")

        password2_input = self.browser.find_element_by_id("password2")
        password2_input.send_keys("selenium")

        submit_button = self.browser.find_element_by_id("registration_button")
        submit_button.click()

        number_of_users = User.objects.all().count()
        print("number_of_users: ")
        print(number_of_users)

        time.sleep(5)
        # Redirection
        self.assertEquals(self.browser.current_url, register_url)

        # User is logged
        logout_button = self.browser.find_element_by_id("logout")
        self.assertEquals(logout_button.text, "Déconnexion")

    def test_login(self):
        # Create user
        self.client.post(
            reverse("register"),
            data={
                "email": "testo@gmail.com",
                "password1": "VendalTest",
                "password2": "VendalTest",
            },
        )

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("login").click()
        time.sleep(1)

        email_input = self.browser.find_element_by_id("login_email")
        email_input.send_keys("testo@gmail.com")

        password_input = self.browser.find_element_by_id("login_password")
        password_input.send_keys("VendalTest")

        submit_button = self.browser.find_element_by_id("login_button")
        submit_button.click()

        # Redirection
        self.assertEquals(self.browser.current_url, self.live_server_url + "/")

        # User is logged
        logout_button = self.browser.find_element_by_id("logout")
        self.assertEquals(logout_button.text, "Déconnexion")
