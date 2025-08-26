from django import forms
from utils.field_validations import remove_non_numeric, validate_email_format
from utils.field_choices import (
    STATE_CHOICES,
    EMPLOYMENT_STATUS,
    MARITAL_STATUS
)


class EditableFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['city'] = forms.CharField(
            max_length=128,
            label="Cidade:",
            widget=forms.TextInput(attrs={
                'id': 'city',
                'class': 'form-control',
                'placeholder': 'A cidade onde você mora...',
                'required': True
            })
        )

        self.fields['state'] = forms.ChoiceField(
            choices=[('', 'Selecione um estado')] + STATE_CHOICES,
            label="Estado:",
            widget=forms.Select(attrs={
                'id': 'state',
                'class': 'form-control',
                'required': True
            })
        )

        self.fields['marital_status'] = forms.ChoiceField(
            choices=[('', 'Selecione um estado civil')] + MARITAL_STATUS,
            label="Estado civil:",
            widget=forms.Select(attrs={
                'id': 'marital_status',
                'class': 'form-control',
                'required': True
            })
        )

        self.fields['employment_status'] = forms.ChoiceField(
            choices=[('', 'Selecione sua situação empregatícia')] + EMPLOYMENT_STATUS,
            label="Situação Empregatícia:",
            widget=forms.Select(attrs={
                'id': 'employment_status',
                'class': 'form-control',
                'required': True
            })
        )

        self.fields['phone'] = forms.CharField(
            max_length=15,
            label="Telefone:",
            widget=forms.TextInput(attrs={
                'id': 'phone',
                'class': 'form-control',
                'placeholder': '(xx)xxxxx-xxxx',
                'required': True
            })
        )

        self.fields['email'] = forms.EmailField(
            max_length=128,
            label="E-mail:",
            widget=forms.EmailInput(attrs={
                'id': 'email',
                'class': 'form-control',
                'placeholder': 'Seu e-mail...',
                'required': True
            })
        )

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
