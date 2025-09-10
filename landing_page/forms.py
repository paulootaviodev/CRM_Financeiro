from datetime import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from crm_financeiro.forms import EditableFieldsMixin
from utils.field_validations import remove_non_numeric, validate_cpf


class CreditSimulationForm(EditableFieldsMixin, forms.Form):
    full_name = forms.CharField(
        max_length=255,
        label="Nome completo:",
        widget=forms.TextInput(attrs={
            'id': 'full_name',
            'class': 'form-control',
            'placeholder': 'Seu nome completo...',
            'required': True
        })
    )

    cpf = forms.CharField(
        max_length=14,
        label="CPF:",
        widget=forms.TextInput(attrs={
            'id': 'cpf',
            'class': 'form-control',
            'placeholder': 'xxx.xxx.xxx-xx',
            'required': True
        })
    )

    birth_date = forms.DateField(
        label="Data de Nascimento:",
        widget=forms.DateInput(attrs={
            'id': 'birth_date',
            'class': 'form-control',
            'type': 'date',
            'required': True,
        })
    )

    privacy_policy = forms.BooleanField(
        required=True,
        label="",
        widget=forms.CheckboxInput(attrs={
            'id': 'privacy_policy',
            'class': 'form-check-input',
            'required': True,
            'checked': False
        })
    )

    def clean_cpf(self):
        """Check if the CPF number is valid."""
        cpf = self.cleaned_data.get('cpf', '')
        cleaned_cpf = remove_non_numeric(cpf)

        if not validate_cpf(cleaned_cpf):
            raise forms.ValidationError("Número de CPF inválido.")
        
        return cleaned_cpf

    def clean_birth_date(self):
        """Check if age is between 18 and 80 years old using date of birth."""
        date_of_birth = self.cleaned_data.get("birth_date")
        current_date = datetime.now().date()
        age = relativedelta(current_date, date_of_birth).years

        if age < 18 or age > 80:
            raise forms.ValidationError("Você precisa ter entre 18 e 80 anos.")

        return date_of_birth

    def clean_privacy_policy(self):
        """Check if the user has agreed to the privacy policy."""
        agreed = self.cleaned_data.get("privacy_policy")

        if not agreed:
            raise forms.ValidationError(
                "Você precisa concordar com a política de privacidade e uso de dados."
            )

        return agreed
    
    class Meta:
        fields = [
            'full_name', 'cpf', 'birth_date', 'city', 'state', 'marital_status',
            'employment_status', 'phone', 'email', 'privacy_policy'
        ]
