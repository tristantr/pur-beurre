from django.db import models
from django.urls import reverse

# from accounts.models import User


class Category(models.Model):
    """Class defining the brand model, derived from the Model class."""

    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Category object (in Admin site etc.)."""
        return self.name

    def get_products(self):
        """Returns the url to access the list of products from a category"""
        return reverse("category_products", kwargs={"id": self.id})


class Product(models.Model):
    """Class defining the product model, derived from the Model class."""

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    stores = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    image = models.TextField(default=None)
    nutriscore = models.IntegerField()
    categories = models.ManyToManyField("Category", related_name="products")
    favorites = models.ManyToManyField(
        "accounts.User", related_name="favorites", blank=True
    )

    def __str__(self):
        """String for representing the Product object (in Admin site etc.)"""
        return self.name

    def get_substitutes(self):
        """Returns the url to access substitutes of a specific product."""
        return reverse("substitutes", kwargs={"id": self.id})

    def get_product_details(self):
        """Returns the url to access a detail record for this product."""
        return reverse("product_details", kwargs={"id": self.id})
