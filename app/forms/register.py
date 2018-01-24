from django import forms
from django.forms import widgets


class RegisterForm(forms.Form):

    username = forms.CharField(max_length=100)
    password1 = forms.CharField(
        min_length=8,
        widget=widgets.PasswordInput
    )
    password2 = forms.CharField(
        min_length=8,
        widget=widgets.PasswordInput
    )
