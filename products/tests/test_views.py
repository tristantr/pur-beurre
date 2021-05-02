from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category
from accounts.models import User
from django.contrib import auth


class HomePageView(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class ProductsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.best_product = Product.objects.create(
            name="Eau minérale",
            brand="Contrex",
            description="Eau minérale naturelle",
            stores="Franprix",
            url="www.contrex.com",
            image="image",
            nutriscore="98",
        )

        cls.product1 = Product.objects.create(
            name="Coca",
            brand="Coca-Cola",
            description="Soda",
            stores="Franprix",
            url="www.coca.com",
            image="image",
            nutriscore="101",
        )

        categories = ["boissons",
                      "eau",
                      "liquide",
                      "rafraichissements",
                      "sodas"]

        for category in categories:
            Category.objects.create(name=category)

        cls.best_product.categories.add(
            Category.objects.get(id=1),
            Category.objects.get(id=2),
            Category.objects.get(id=3),
            Category.objects.get(id=4),
        )

        cls.product1.categories.add(
            Category.objects.get(id=1),
            Category.objects.get(id=3),
            Category.objects.get(id=4),
            Category.objects.get(id=5),
        )

    def test_get_substitutes_if_no_better_product(self):
        """Result when the selected product doesn't have substitutes"""
        response = self.client.get(
            reverse("substitutes", kwargs={"id": self.best_product.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/substitutes.html")

    def test_get_substitutes(self):
        """Results when the selected product has substitutes"""
        response = self.client.get(
            reverse("substitutes", kwargs={"id": self.product1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/substitutes.html")

    def test_get_product_details(self):
        """Test when we try to access specific product pages"""
        response = self.client.get(
            reverse("product_details", kwargs={"id": self.product1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_details.html")

    def test_get_category_products(self):
        """Test when we try to access specific category pages"""
        response = self.client.get(
            reverse(
                "category_products",
                kwargs={"id": Category.objects.get(name="boissons").id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/category.html")


class FavoritesView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product2 = Product.objects.create(
            name="Petits Beurre",
            brand="Lu",
            description="Gateaux",
            stores="Franprix",
            url="www.lu.com",
            image="image",
            nutriscore="100",
        )

        cls.credentials = {"email": "products@gmail.com",
                           "password": "password"}
        cls.user = User.objects.create_user("products@gmail.com", "password")

    def setUp(self):
        self.client.post(reverse("login"), self.credentials)
        self.client_user = auth.get_user(self.client)

    def test_get_favorites_if_no_favorites(self):
        """User gets fav page even if there is no favorites to display"""
        self.assertEqual(self.user.favorites.count(), 0)
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/favorites.html")

    def test_get_favorites(self):
        """Test that the logged user can access favorites"""
        self.user.favorites.add(self.product2)
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/favorites.html")
