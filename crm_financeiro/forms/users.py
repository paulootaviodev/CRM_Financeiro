from django import forms
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .user_fields import UserFieldsMixin


class UserRegisterForm(UserFieldsMixin, UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'is_staff',
            'is_superuser', 'groups', 'user_permissions'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_permissions'].label_from_instance = self.translate_permission

    def translate_permission(self, perm):
        model_meta = perm.content_type.model_class()._meta
        model_verbose_name = model_meta.verbose_name

        app_config = apps.get_app_config(perm.content_type.app_label)
        app_verbose_name = app_config.verbose_name

        # Extracts the action and model name from perm.name
        # Example: "Can add views per month" -> action="add", model="views per month"
        parts = perm.name.split(' ', 2)
        if len(parts) >= 2 and parts[0] == 'Can':
            action = parts[1]
            # Translates the action
            action_translations = {
                'add': _('Pode adicionar'),
                'change': _('Pode alterar'),
                'delete': _('Pode excluir'),
                'view': _('Pode visualizar'),
            }
            translated_action = action_translations.get(action, _(action))
            # Match the translated action with the verbose_name of the model
            translated_permission_name = f'{translated_action} {model_verbose_name}'
        else:
            # Fallback to the original translated name
            translated_permission_name = _(perm.name)

        return f'{app_verbose_name} | {translated_permission_name}'


class UserFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            field.widget.attrs.pop('required', None)
    
    is_active = forms.ChoiceField(
        choices=[('true', 'Sim'), ('false', 'Não')],
        label="Usuário ativo:",
        widget=forms.Select(attrs={
            'id': 'is_active',
            'class': 'form-control'
        })
    )

    is_superuser = forms.ChoiceField(
        choices=[('true', 'Sim'), ('false', 'Não')],
        label="É administrador:",
        widget=forms.Select(attrs={
            'id': 'is_superuser',
            'class': 'form-control'
        })
    )

    is_staff = forms.ChoiceField(
        choices=[('true', 'Sim'), ('false', 'Não')],
        label="Faz parte da equipe:",
        widget=forms.Select(attrs={
            'id': 'is_staff',
            'class': 'form-control'
        })
    )

    date_joined_initial = forms.DateField(
        label="Data Criado - Inicial:",
        widget=forms.DateInput(attrs={
            'id': 'date_joined_initial',
            'class': 'form-control',
            'type': 'date'
        })
    )

    date_joined_final = forms.DateField(
        label="Data Criado - Final:",
        widget=forms.DateInput(attrs={
            'id': 'date_joined_final',
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        fields = [
            'is_active', 'is_superuser', 'is_staff',
            'date_joined_initial', 'date_joined_final'
        ]


class UserUpdateForm(UserFieldsMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions'
        ]


class ChangePasswordForm(UserFieldsMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['email']
        del self.fields['is_staff']
        del self.fields['is_superuser']
        del self.fields['groups']
        del self.fields['user_permissions']
    
    class Meta:
        fields = [
            'username', 'password1', 'password2'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if new_password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário não encontrado.")
        return username
