from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserForm(UserCreationForm):
    """Form used to register a new user"""

    email = forms.EmailField(
        max_length=282,
        widget=forms.TextInput(
            attrs={
                "id": "email",
                "class": "form-control",
                "placeholder": "Adresse email",
                "style": "font-size: 1.1rem",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(
            attrs={
                "id": "password1",
                "class": "form-control",
                "placeholder": "Mot de passe",
                "style": "font-size: 1.1rem",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(
            attrs={
                "id": "password2",
                "class": "form-control",
                "placeholder": "Confirmer le mot de passe",
                "style": "font-size: 1.1rem",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(forms.Form):
    """Form used to log a user"""

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "id": "login_email",
                "class": "form-control",
                "placeholder": "Adresse email",
                "style": "font-size: 1.1rem",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "login_password",
                "class": "form-control",
                "placeholder": "Mot de passe",
                "style": "font-size: 1.1rem",
            }
        )
    )
