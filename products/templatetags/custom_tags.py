from django import template
from django.template.loader import get_template

register = template.Library()


def display_product(product, user):
    my_product = product
    user = user
    return {"product": my_product, "logged_user": user}


products_template = get_template("products/product.html")
register.inclusion_tag(products_template)(display_product)
