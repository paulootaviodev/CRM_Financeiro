from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control form-control-user',
            'id': 'username',
            'name': 'username',
            'placeholder': 'Seu usuário...',
            'required': True,
            'autofocus': True,
        }),
        label='Usuário'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control form-control-user',
            'id': 'password',
            'name': 'password',
            'placeholder': '********',
            'required': True,
        }),
        label='Senha'
    )
