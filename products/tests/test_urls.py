from django.test import SimpleTestCase
from django.urls import resolve, reverse
from products import views


class TestUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, views.index)

    def test_get_favorites_url_is_resolved(self):
        url = reverse("favorites")
        self.assertEquals(resolve(url).func, views.get_favorites)

    def test_get_substitutes_url_is_resolved(self):
        url = reverse("substitutes", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, views.get_substitutes)

    def test_manage_favorites_url_is_resolved(self):
        url = reverse("fav")
        self.assertEquals(resolve(url).func, views.manage_favorites)

    def test_get_product_details_url_is_resolved(self):
        url = reverse("product_details", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, views.get_product_details)

    def test_get_category_products_url_is_resolved(self):
        url = reverse("category_products", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, views.get_category_products)
