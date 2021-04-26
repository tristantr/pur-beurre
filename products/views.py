from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect

from .models import Category, Product


def index(request):
    """View function for home page of site."""
    return render(request, "index.html")


def get_substitutes(request, id=None):
    """View to call to access the substitution algorithm and get substitutes"""
    my_product = get_object_or_404(Product, id=id)
    my_categories = my_product.categories.all()

    substitutes = []

    better_products = Product.objects.filter(
        categories__in=my_categories, nutriscore__lt=my_product.nutriscore
    )

    if better_products:
        common_categories = {}
        common_categories_keys = []
        product_instances = []

        for product in better_products:
            product_instances.append(product.pk)

        for product in sorted(set(product_instances)):
            number_of_common_categories = product_instances.count(product)

            if number_of_common_categories not in common_categories_keys:
                common_categories[number_of_common_categories] = []
                common_categories_keys.append(number_of_common_categories)
                common_categories[number_of_common_categories].append(product)
            else:
                common_categories[number_of_common_categories].append(product)

        substitute_ids = []

        for i in sorted(common_categories_keys, reverse=True):
            for j in common_categories[i]:
                substitute_ids.append(j)

        substitutes = []
        best_substitute = Product.objects.get(pk=substitute_ids[0])
        substitute_ids.pop(0)

        for id in substitute_ids:
            substitutes.append(Product.objects.get(pk=id))

        for product in substitutes + [my_product, best_substitute]:
            product.nutriscore = (
                "assets/img/" + chr(product.nutriscore).upper() + "." + "png"
            )
            if product.favorites.filter(id=request.user.id).exists():
                product.is_favorite = True
            else:
                product.is_favorite = False

        p = Paginator(substitutes, 6)
        page_num = request.GET.get("page", 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            "substitutes": page,
            "best_substitute": best_substitute,
            "my_product": my_product,
        }

    else:
        context = {"substitutes": [], "my_product": my_product}

    return render(request, "products/substitutes.html", context=context)


def get_product_details(request, id=None):
    """View to access specific product information"""
    product = get_object_or_404(Product, id=id)
    product.nutriscore = "assets/img/" + \
        chr(product.nutriscore).upper() + "." + "png"
    categories = product.categories.all()

    if product.favorites.filter(id=request.user.id).exists():
        product.is_favorite = True
    else:
        product.is_favorite = False

    context = {"product": product, "categories": categories}

    return render(request, "products/product_details.html", context=context)


@login_required()
def manage_favorite(request, id):
    """Add a product to favorites or remove a product from favorites"""
    product = get_object_or_404(Product, id=id)
    if product.favorites.filter(id=request.user.id).exists():
        product.favorites.remove(request.user)
    else:
        product.favorites.add(request.user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required()
def get_favorites(request):
    """Get favorites products"""
    user = request.user
    favorites = user.favorites.all()

    for product in favorites:
        product.is_favorite = True
        product.nutriscore = (
            "assets/img/" + chr(product.nutriscore).upper() + "." + "png"
        )

    p = Paginator(favorites, 9)
    page_num = request.GET.get("page", 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {"products": page}
    return render(request, "products/favorites.html", context=context)


def get_category_products(request, id=None):
    """Get all products for a specific category"""
    category = get_object_or_404(Category, id=id)
    products = category.products.all()

    for product in products:
        product.nutriscore = (
            "assets/img/" + chr(product.nutriscore).upper() + "." + "png"
        )
        if product.favorites.filter(id=request.user.id).exists():
            product.is_favorite = True
        else:
            product.is_favorite = False

    p = Paginator(products, 6)
    page_num = request.GET.get("page", 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {"products": page, "category": category}

    return render(request, "products/category.html", context=context)


def get_legals(request):
    return render(request, "legals.html")


class SearchResultsView(generic.ListView):
    """Class to implement the Search section"""

    model = Product
    template_name = "products/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Product.objects.filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        )
