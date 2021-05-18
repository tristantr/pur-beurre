import requests
import sys
from django.core.management.base import BaseCommand
from products.models import Product, Category

from datetime import datetime

from tqdm import tqdm


class Command(BaseCommand):
    help = "Fill the database"

    def __get_products(self):
        """ Get products from Openfoodfacts API"""
        number_of_pages = range(1, 20)
        raw_products = []
        print("Data recovery from Openfoodfacts")
        for i in tqdm(number_of_pages):
            payload = {"action": "process",
                       "json": "true",
                       "page": i,
                       "page_size": 50}
            try:
                r = requests.get(
                    "https://fr.openfoodfacts.org/cgi/search.pl",
                    params=payload
                )
                if not r.ok:
                    raise Exception
                else:
                    r_json = r.json()
                    products_from_this_page = r_json["products"]
                    raw_products.extend(products_from_this_page)
            except Exception:
                print("ERROR: Your connexion has failed. Please try again")
                sys.exit(0)

        return raw_products

    def __check_products(self, raw_products):
        """ Check if products have needed informations """
        product_names = []
        products = []
        for raw_product in raw_products:
            if (
                raw_product.get("product_name")
                and raw_product.get("brands")
                and raw_product.get("categories")
                and raw_product.get("stores")
                and raw_product.get("code")
                and raw_product.get("nutriscore_grade")
                and raw_product.get("ingredients_text")
                and raw_product.get("image_front_url")
            ):
                if raw_product["product_name"] not in product_names:
                    product_names.append(raw_product["product_name"])
                    products.append(raw_product)

        return product_names, products

    def __get_categories(self, products):
        """ Get products categories """
        categories = []
        for product in products:
            product_categories = []
            lowered_categories = product["categories"].lower().split(", " and ",")
            for lowered_category in lowered_categories:
                category = lowered_category.strip()
                if category.startswith("en") or category.startswith("fr"):
                    pass
                else:
                    product_categories.append(category)
                    if category not in categories:
                        categories.append(category)
            product["categories"] = product_categories

        return categories

    def __set_products(self, products):
        """ format Product objects  """
        cleaned_products = []
        for product in products:
            if product["categories"] != []:
                product_data = {}
                product_data["name"] = product["product_name"].lower()
                product_data["brand"] = product["brands"]
                product_data["categories"] = product["categories"]
                product_data["description"] = product["ingredients_text"]
                product_data["stores"] = product["stores"]
                product_data["nutriscore"] = product["nutriscore_grade"]
                product_data["url"] = "https://fr.openfoodfacts.org/produit/{}".format(
                    product["code"]
                )
                product_data["image"] = product["image_front_url"]
                cleaned_products.append(product_data)

        return cleaned_products

    def __get_cleaned_products_and_categories(self):
        """ Get cleaned products and category names """
        raw_products = self.__get_products()
        product_names, products = self.__check_products(raw_products)
        categories = self.__get_categories(products)
        cleaned_products = self.__set_products(products)
        return categories, cleaned_products

    def __add_categories_to_database(self, categories):
        """ Add categories to database """
        print("Adding categories to database")
        for category in categories:
            category_in_db, created = Category.objects.get_or_create(name=category)
        print("SUCCESS")

    def __add_product_to_database(self, cleaned_products):
        """ Add products to database """
        print("Adding products to database")
        for clean_product in tqdm(cleaned_products):
            product, created = Product.objects.get_or_create(
                name=clean_product["name"],
                brand=clean_product["brand"],
                description=clean_product["description"],
                stores=clean_product["stores"],
                nutriscore=ord(clean_product["nutriscore"]),
                url=clean_product["url"],
                image=clean_product["image"],
            )
            for category in clean_product["categories"]:
                category_id = Category.objects.get(name=category).id
                product.categories.add(category_id)

        print("SUCCESS")
        print("------------------------")
        print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))

    def handle(self, *args, **kwargs):
        """ Command to use with manage.py """
        categories, cleaned_products = self.__get_cleaned_products_and_categories()
        self.__add_categories_to_database(categories)
        self.__add_product_to_database(cleaned_products)
