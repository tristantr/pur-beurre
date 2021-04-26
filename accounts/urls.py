from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register"),
    path("login", views.log_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("my_account", views.get_my_account, name="my_account"),
]
