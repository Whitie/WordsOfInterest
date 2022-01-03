from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username'), max_length=150,
        widget=forms.TextInput(attrs={'class': 'input is-success'})
    )
    password = forms.CharField(
        label=_('Password'), max_length=150,
        widget=forms.PasswordInput(attrs={'class': 'input is-success'})
    )
