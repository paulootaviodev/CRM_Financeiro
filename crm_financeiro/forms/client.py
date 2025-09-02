from .editable_fields import EditableFieldsMixin
from crm_financeiro.models import Client
from django import forms


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
        })
    )

    birth_date_final = forms.DateField(
        label="Data de Nascimento - Final:",
        widget=forms.DateInput(attrs={
            'id': 'birth_date_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    client_since_initial = forms.DateField(
        label="Cliente Desde - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'client_since_initial',
            'class': 'form-control',
            'type': 'date'
        })
    )

    client_since_final = forms.DateField(
        label="Cliente Desde - Final:",
        widget=forms.DateInput(attrs={
            'id': 'client_since_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    is_active = forms.ChoiceField(
        choices=[('true', 'Sim'), ('false', 'Não')],
        label="Cliente ativo:",
        widget=forms.Select(attrs={
            'id': 'is_active',
            'class': 'form-control'
        })
    )

    marked_for_deletion = forms.ChoiceField(
        choices=[('false', 'Não'), ('true', 'Sim')],
        label="Marcado para exclusão:",
        widget=forms.Select(attrs={
            'id': 'marked_for_deletion',
            'class': 'form-control'
        })
    )

    class Meta:
        fields = [
            'state', 'marital_status', 'birth_date_initial', 'birth_date_final',
            'employment_status', 'client_since_initial', 'client_since_final',
            'is_active', 'marked_for_deletion'
        ]
