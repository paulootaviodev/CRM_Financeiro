from django import forms


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
