from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages


def register_user(request):
    """View called when a new user creates an account"""
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "index.html")
        else:
            print(form.errors)
            for field in form.errors:
                print(field)

    context = {"form": form}
    return render(request, "register.html", context)


def log_user(request):
    """View called when a user logs to the website"""
    form = LoginForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return render(request, "index.html")
        else:
            messages.info(request, "Email OR password is incorrect")

    context = {"form": form}
    return render(request, "login.html", context)


@login_required()
def get_my_account(request):
    """View called when a user wants to access its account details"""
    current_user = request.user
    context = {"user": current_user}
    return render(request, "my_account.html", context)


@login_required()
def logout_user(request):
    """View called when the user logs out"""
    logout(request)
    return redirect("login")
