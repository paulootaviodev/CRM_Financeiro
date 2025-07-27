from django.contrib.auth.forms import AuthenticationForm
from .models import Client
from django import forms
from utils.field_validations import remove_non_numeric, validate_email_format
from utils.field_choices import (
    STATE_CHOICES,
    EMPLOYMENT_STATUS,
    MARITAL_STATUS,
    LOAN_PROPOSAL_STATUS,
    PAYMENT_STATUS
)


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


class UpdateClientForm(EditableFieldsMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['phone'].initial = self.instance.phone
            self.fields['email'].initial = self.instance.email

    class Meta:
        model = Client
        fields = ['city', 'state', 'marital_status', 'employment_status']


class ClientFilterForm(EditableFieldsMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            field.widget.attrs.pop('required', None)

    birth_date_initial = forms.DateField(
        label="Data de Nascimento - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'birth_date_initial',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    birth_date_final = forms.DateField(
        label="Data de Nascimento - Final:",
        widget=forms.DateInput(attrs={
            'id': 'birth_date_final',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    client_since_initial = forms.DateField(
        label="Cliente Desde - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'client_since_initial',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    client_since_final = forms.DateField(
        label="Cliente Desde - Final:",
        widget=forms.DateInput(attrs={
            'id': 'client_since_final',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    is_active = forms.ChoiceField(
        choices=[('true', 'Sim'), ('false', 'Não')],
        label="Cliente ativo:",
        widget=forms.Select(attrs={
            'id': 'is_active',
            'class': 'form-control'
        }),
        required=False
    )

    marked_for_deletion = forms.ChoiceField(
        choices=[('false', 'Não'), ('true', 'Sim')],
        label="Marcado para exclusão:",
        widget=forms.Select(attrs={
            'id': 'marked_for_deletion',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        fields = [
            'state', 'marital_status', 'birth_date_initial', 'birth_date_final',
            'employment_status', 'client_since_initial', 'client_since_final',
            'is_active', 'marked_for_deletion'
        ]


class SimulationFilterForm(ClientFilterForm):
    created_at_initial = forms.DateField(
        label="Criado em - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'created_at_initial',
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    created_at_final = forms.DateField(
        label="Criado em - Final:",
        widget=forms.DateInput(attrs={
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


class LoanProposalFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            field.widget.attrs.pop('required', None)

    status = forms.ChoiceField(
        choices=[('', 'Selecione um status')] + LOAN_PROPOSAL_STATUS,
        label="Status:",
        widget=forms.Select(attrs={
            'id': 'status',
            'class': 'form-control'
        })
    )

    payment_status = forms.ChoiceField(
        choices=[('', 'Selecione um status de pagamento')] + PAYMENT_STATUS,
        label="Status de pagamento:",
        widget=forms.Select(attrs={
            'id': 'payment_status',
            'class': 'form-control'
        })
    )

    released_value_min = forms.DecimalField(
        label="Valor mínimo liberado:",
        widget=forms.NumberInput(attrs={
            'id': 'released_value_min',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    released_value_max = forms.DecimalField(
        label="Valor máximo liberado:",
        widget=forms.NumberInput(attrs={
            'id': 'released_value_max',
            'class': 'form-control',
            'step': '0.01'
        })
    )

    number_of_installments_min = forms.DecimalField(
        label="Quantidade mínima de parcelas:",
        widget=forms.NumberInput(attrs={
            'id': 'number_of_installments_min',
            'class': 'form-control',
        })
    )

    number_of_installments_max = forms.DecimalField(
        label="Quantidade máxima de parcelas:",
        widget=forms.NumberInput(attrs={
            'id': 'number_of_installments_max',
            'class': 'form-control',
        })
    )

    value_of_installments_min = forms.DecimalField(
        label="Valor mínimo das parcelas:",
        widget=forms.NumberInput(attrs={
            'id': 'value_of_installments_min',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    value_of_installments_max = forms.DecimalField(
        label="Valor máximo das parcelas:",
        widget=forms.NumberInput(attrs={
            'id': 'value_of_installments_max',
            'class': 'form-control',
            'step': '0.01'
        })
    )


class InstallmentFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            field.widget.attrs.pop('required', None)

    due_date_initial = forms.DateField(
        label="Data de vencimento - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'due_date_initial',
            'class': 'form-control',
            'type': 'date'
        })
    )

    due_date_final = forms.DateField(
        label="Data de vencimento - Final:",
        widget=forms.DateInput(attrs={
            'id': 'due_date_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    payment_date_initial = forms.DateField(
        label="Data de pagamento - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'payment_date_initial',
            'class': 'form-control',
            'type': 'date'
        })
    )

    payment_date_final = forms.DateField(
        label="Data de pagamento - Final:",
        widget=forms.DateInput(attrs={
            'id': 'payment_date_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    amount_min = forms.DecimalField(
        label="Valor mínimo:",
        widget=forms.NumberInput(attrs={
            'id': 'amount_min',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    amount_max = forms.DecimalField(
        label="Valor máximo:",
        widget=forms.NumberInput(attrs={
            'id': 'amount_max',
            'class': 'form-control',
            'step': '0.01'
        })
    )

    is_paid = forms.ChoiceField(
        choices=[('false', 'Não'), ('true', 'Sim')],
        label="Está pago:",
        widget=forms.Select(attrs={
            'id': 'is_paid',
            'class': 'form-control'
        })
    )

    is_canceled = forms.ChoiceField(
        choices=[('false', 'Não'), ('true', 'Sim')],
        label="Está cancelado:",
        widget=forms.Select(attrs={
            'id': 'is_canceled',
            'class': 'form-control'
        })
    )
