from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("search/", views.SearchResultsView.as_view(), name="search_results"),

    path("products/<int:id>/substitutes",views.get_substitutes, name="substitutes"),

    path("products/<int:id>",views.get_product_details, name="product_details"),

######

    path("products/favorites/", views.manage_favorites, name="fav"),

#####


    path("products/favorites", views.get_favorites, name="favorites"),

    path("categories/<int:id>", views.get_category_products, name="category_products"),

    path("legals/", views.get_legals, name="legals"),
]
