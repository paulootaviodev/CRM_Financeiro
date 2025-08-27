from .editable_fields import EditableFieldsMixin
from django import forms


class BlogPostFilterForm(EditableFieldsMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            field.widget.attrs.pop('required', None)

    created_at_initial = forms.DateField(
        label="Data Criado - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'created_at_initial',
            'class': 'form-control',
            'type': 'date'
        })
    )

    created_at_final = forms.DateField(
        label="Data Criado - Final:",
        widget=forms.DateInput(attrs={
            'id': 'created_at_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    updated_at_initial = forms.DateField(
        label="Data Atualizado - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'updated_at_initial',
            'class': 'form-control',
            'type': 'date'
        })
    )

    updated_at_final = forms.DateField(
        label="Data Atualizado - Final:",
        widget=forms.DateInput(attrs={
            'id': 'updated_at_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        fields = [
            'created_at_initial',
            'created_at_final',
            'updated_at_initial',
            'updated_at_final'
        ]
