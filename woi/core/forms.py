from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Tag


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username'), max_length=150,
        widget=forms.TextInput(attrs={'class': 'input is-primary'})
    )
    password = forms.CharField(
        label=_('Password'), max_length=150,
        widget=forms.PasswordInput(attrs={'class': 'input is-primary'})
    )


class ArticleForm(forms.Form):
    title = forms.CharField(
        label=_('Title'), max_length=100,
        widget=forms.TextInput(attrs={'class': 'input is-primary'})
    )
    image = forms.FileField(
        label=_('Image'), required=False,
        widget=forms.FileInput(attrs={'class': 'file-input'})
    )
    raw = forms.CharField(
        label=_('Markdown Text'),
        widget=forms.Textarea(attrs={'class': 'textarea is-primary'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('tag'),
        label=_('Tag(s)'), required=False,
        widget=forms.CheckboxSelectMultiple
    )
    comments_allowed = forms.BooleanField(
        label=_('Allow comments'), required=False, initial=True
    )
    publish = forms.BooleanField(
        label=_('Publish'), required=False, initial=False
    )
