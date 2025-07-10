from django import forms
from django.contrib.auth.forms import AuthenticationForm
from landing_page.forms import CreditSimulationForm
from crm_financeiro.models import STATE_CHOICES, EMPLOYMENT_STATUS, MARITAL_STATUS


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


class ClientForm(CreditSimulationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].widget.attrs.update({'class': 'form-control'})


class ClientFilterForm(forms.Form):
    state = forms.ChoiceField(
        choices=[('', 'Selecione um estado')] + STATE_CHOICES,
        label="Estado:",
        widget=forms.Select(attrs={
            'id': 'state',
            'class': 'form-control'
        }),
        required=False
    )

    marital_status = forms.ChoiceField(
        choices=[('', 'Selecione um estado civil')] + MARITAL_STATUS,
        label="Estado civil:",
        widget=forms.Select(attrs={
            'id': 'marital_status',
            'class': 'form-control'
        }),
        required=False
    )

    birth_date_initial = forms.DateField(label="Data de Nascimento - Inicial:", widget=forms.DateInput(attrs={
            'id': 'birth_date_initial',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    birth_date_final = forms.DateField(label="Data de Nascimento - Final:", widget=forms.DateInput(attrs={
            'id': 'birth_date_final',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    employment_status = forms.ChoiceField(
        choices=[('', 'Selecione sua situação empregatícia')] + EMPLOYMENT_STATUS,
        label="Situação Empregatícia:",
        widget=forms.Select(attrs={
            'id': 'employment_status',
            'class': 'form-control'
        }),
        required=False
    )

    client_since_initial = forms.DateField(label="Cliente Desde - Inicial:", widget=forms.DateInput(attrs={
            'id': 'client_since_initial',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    client_since_final = forms.DateField(label="Cliente Desde - Final:", widget=forms.DateInput(attrs={
            'id': 'client_since_final',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )


class SimulationFilterForm(ClientFilterForm):
    created_at_initial = forms.DateField(label="Criado em - Inicial:", widget=forms.DateInput(attrs={
            'id': 'created_at_initial',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    created_at_final = forms.DateField(label="Criado em - Final:", widget=forms.DateInput(attrs={
            'id': 'created_at_final',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    class Meta:
        fields = [
            'state', 'marital_status', 'birth_date_initial', 'birth_date_final',
            'employment_status', 'created_at_initial', 'created_at_final'
        ]
