from django import forms
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import STATE_CHOICES, EMPLOYMENT_STATUS, MARITAL_STATUS
import re

def remove_non_numeric(value: str) -> str:
    """Remove all non-numeric characters from the input string."""
    return re.sub(r'\D', '', value)

def validate_cpf(cpf: str) -> bool:
    """Validate CPF number by checking its structure and check digits."""
    if not re.fullmatch(r"\d{11}", cpf):
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    for i in range(9, 11):
        sum_digits = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        check_digit = ((sum_digits * 10) % 11) % 10
        if check_digit != int(cpf[i]):
            return False
    return True

def validate_email_format(email):
    """Valida o formato do e-mail usando regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)


class CreditSimulationForm(forms.Form):
    full_name = forms.CharField(max_length=255, label="Nome completo:", widget=forms.TextInput(attrs={
            'id': 'full_name',
            'class': 'form-control',
            'placeholder': 'Seu nome completo...',
            'required': True
        })
    )

    cpf = forms.CharField(max_length=14, label="CPF:", widget=forms.TextInput(attrs={
            'id': 'cpf',
            'class': 'form-control',
            'placeholder': 'xxx.xxx.xxx-xx',
            'required': True
        })
    )

    city = forms.CharField(max_length=128, label="Cidade:", widget=forms.TextInput(attrs={
            'id': 'city',
            'class': 'form-control',
            'placeholder': 'A cidade onde você mora...',
            'required': True
        })
    )

    state = forms.ChoiceField(
        choices=[('', 'Selecione um estado')] + STATE_CHOICES,
        label="Estado:",
        widget=forms.Select(attrs={
            'id': 'state',
            'class': 'form-control',
            'required': True
        })
    )

    marital_status = forms.ChoiceField(
        choices=[('', 'Selecione um estado civil')] + MARITAL_STATUS,
        label="Estado civil:",
        widget=forms.Select(attrs={
            'id': 'marital_status',
            'class': 'form-control',
            'required': True
        })
    )

    birth_date = forms.DateField(label="Data de Nascimento:", widget=forms.DateInput(attrs={
            'id': 'birth_date',
            'class': 'form-control',
            'type': 'date',
            'required': True,
        })
    )

    employment_status = forms.ChoiceField(
        choices=[('', 'Selecione sua situação empregatícia')] + EMPLOYMENT_STATUS,
        label="Situação Empregatícia:",
        widget=forms.Select(attrs={
            'id': 'employment_status',
            'class': 'form-control',
            'required': True
        })
    )

    phone = forms.CharField(max_length=15, label="Telefone:", widget=forms.TextInput(attrs={
            'id': 'phone',
            'class': 'form-control',
            'placeholder': '(xx)xxxxx-xxxx',
            'required': True
        })
    )

    email = forms.EmailField(max_length=128, label="E-mail:", widget=forms.EmailInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'Seu e-mail...',
            'required': True
        })
    )

    privacy_policy = forms.BooleanField(
        required=True,
        label="",
        widget=forms.CheckboxInput(attrs={
            'id': 'privacy-policy',
            'class': 'form-check-input',
            'required': True,
            'checked': False
        })
    )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        cleaned_cpf = remove_non_numeric(cpf)
        if not validate_cpf(cleaned_cpf):
            raise forms.ValidationError("Número de CPF inválido.")
        return cleaned_cpf

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        cleaned_phone = remove_non_numeric(phone)
        if len(cleaned_phone) < 10 or len(cleaned_phone) > 11:
            raise forms.ValidationError("Número de telefone inválido.")
        return cleaned_phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not validate_email_format(email):
            raise forms.ValidationError("Endereço de e-mail inválido.")
        return email

    def clean_birth_date(self):
        date_of_birth = self.cleaned_data.get("birth_date")
        current_date = datetime.now().date()
        age = relativedelta(current_date, date_of_birth).years

        if age < 18 or age > 80:
            raise forms.ValidationError("Você precisa ter entre 18 e 80 anos.")

        return date_of_birth

    def clean_privacy_policy(self):
        agreed = self.cleaned_data.get("privacy_policy")

        if not agreed:
            raise forms.ValidationError("Você precisa concordar com a política de privacidade e uso de dados.")

        return agreed
