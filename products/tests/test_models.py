from django.test import TestCase

from products.models import Product


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="Petits écoliers",
            brand="Lu",
            description="Gâteaux de mon enfance",
            stores="Franprix",
            url="www.lu.com",
            image="image",
            nutriscore="98",
        )

    def test_name_label(self):
        field_label = self.product._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.product._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_brand_label(self):
        field_label = self.product._meta.get_field("brand").verbose_name
        self.assertEqual(field_label, "brand")

    def test_brand_max_length(self):
        max_length = self.product._meta.get_field("brand").max_length
        self.assertEqual(max_length, 200)

    def test_description_label(self):
        field_label = self.product._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_description_max_length(self):
        max_length = self.product._meta.get_field("description").max_length
        self.assertEqual(max_length, 200)

    def test_stores_label(self):
        field_label = self.product._meta.get_field("stores").verbose_name
        self.assertEqual(field_label, "stores")

    def test_stores_max_length(self):
        max_length = self.product._meta.get_field("stores").max_length
        self.assertEqual(max_length, 200)

    def test_url_label(self):
        field_label = self.product._meta.get_field("url").verbose_name
        self.assertEqual(field_label, "url")

    def test_url_max_length(self):
        max_length = self.product._meta.get_field("url").max_length
        self.assertEqual(max_length, 200)

    def test_image_label(self):
        field_label = self.product._meta.get_field("image").verbose_name
        self.assertEqual(field_label, "image")

    def test_nutriscore_label(self):
        field_label = self.product._meta.get_field("nutriscore").verbose_name
        self.assertEqual(field_label, "nutriscore")

    def test_get_substitutes(self):
        self.assertEqual(
            self.product.get_substitutes(),
            "/products/1/substitutes")

    def test_get_product_details(self):
        self.assertEqual(self.product.get_product_details(), "/products/1")
