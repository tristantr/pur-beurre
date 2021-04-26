from django import template
from django.template.loader import get_template

register = template.Library()


def display_product(product):
    my_product = product
    return {"product": my_product}


products_template = get_template("products/product.html")
register.inclusion_tag(products_template)(display_product)
