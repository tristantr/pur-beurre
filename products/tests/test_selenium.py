from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from products.models import Product, Category
from accounts.models import User

from django.contrib.auth import get_user_model

import time


class TestHomePage(StaticLiveServerTestCase):
    def setUp(self):
        PATH = "/Users/josselinlecuyer/Desktop/Formation developpeur Python/PROJETS/Projet 8/Livrable/chromedriver"
        self.browser = webdriver.Chrome(PATH)

    def tearDown(self):
        self.browser.close()

    def test_welcome_page_is_displayed(self):
        self.browser.get(self.live_server_url)
        home_page = self.browser.find_element_by_id("home-page")
        self.assertEquals(
            home_page.find_element_by_tag_name("h1").text,
            "DU GRAS OUI, MAIS DE QUALITÉ !",
        )

    def test_get_substitutes_path_from_main_search(self):
        coca = Product.objects.create(
            name="Coca",
            brand="Coca-Cola",
            description="Soda",
            stores="Franprix",
            url="www.coca.com",
            image="image",
            nutriscore="101",
        )

        self.browser.get(self.live_server_url)
        substitutes_page = self.live_server_url + reverse(
            "substitutes", kwargs={"id": coca.id}
        )

        search_input = self.browser.find_element_by_id("home-search")
        search_input.send_keys("Coca" + Keys.ENTER)

        result = self.browser.find_element_by_id("results")
        result.find_element_by_tag_name("a").click()

        self.assertEquals(self.browser.current_url, substitutes_page)

    def test_get_substitutes_path_from_nav_search(self):
        orangina = Product.objects.create(
            name="Orangina",
            brand="Orangina",
            description="Soda",
            stores="Franprix",
            url="www.orangina.com",
            image="image",
            nutriscore="101",
        )

        self.browser.get(self.live_server_url)
        substitutes_page = self.live_server_url + reverse(
            "substitutes", kwargs={"id": orangina.id}
        )

        search_input = self.browser.find_element_by_id("navbar-search")
        search_input.send_keys("Orangina" + Keys.ENTER)

        result = self.browser.find_element_by_id("results")
        result.find_element_by_tag_name("a").click()

        self.assertEquals(self.browser.current_url, substitutes_page)


class Favorites(StaticLiveServerTestCase):
    def setUp(self):
        PATH = "/Users/josselinlecuyer/Desktop/Formation developpeur Python/PROJETS/Projet 8/Livrable/chromedriver"
        self.browser = webdriver.Chrome(PATH)

        self.orangina = Product.objects.create(
            name="Orangina",
            brand="Orangina",
            description="Soda",
            stores="Franprix",
            url="www.orangina.com",
            image="image",
            nutriscore="101",
        )

        self.user = User.objects.create_user(
            email="user@gmail.com",
            password="erpufubapeur")

        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id("login").click()
        email_input = self.browser.find_element_by_id("login_email")
        email_input.send_keys("user@gmail.com")

        password_input = self.browser.find_element_by_id("login_password")
        password_input.send_keys("erpufubapeur")

        submit_button = self.browser.find_element_by_id("login_button")
        submit_button.click()


    def tearDown(self):
        self.browser.close()

    def test_add_a_product_to_favorites(self):
        product_page = self.browser.get(self.live_server_url + reverse(
            "product_details", kwargs={"id": self.orangina.id}
        ))
        favorites_button = self.browser.find_element_by_class_name('far')
        favorites_button.click()
        time.sleep(3)
        self.assertEquals(self.user.favorites.count(), 1)
        favorite_product = self.user.favorites.all()[0]
        self.assertEquals(favorite_product.id, 1)


    def test_remove_a_product_from_favorites(self):
        self.user.favorites.add(self.orangina)
        self.user.save()
        self.assertEquals(self.user.favorites.count(), 1)

        product_page = self.browser.get(self.live_server_url + reverse(
            "product_details", kwargs={"id": self.orangina.id}
        ))

        remove_from_favorites_button = self.browser.find_element_by_class_name('fa-heart')
        remove_from_favorites_button.click()
        time.sleep(4)

        self.assertEquals(self.user.favorites.count(), 0)

            

