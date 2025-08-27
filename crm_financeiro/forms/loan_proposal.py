from django import forms
from utils.field_choices import (
    LOAN_PROPOSAL_STATUS,
    PAYMENT_STATUS
)


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
