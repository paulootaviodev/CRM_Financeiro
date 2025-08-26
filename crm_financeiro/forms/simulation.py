from .client import ClientFilterForm
from django import forms


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
