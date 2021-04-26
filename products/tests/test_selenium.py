from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from products.models import Product


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
