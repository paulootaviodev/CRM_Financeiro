from django import forms
from django.contrib.auth.models import Permission, Group


class UserFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(
            label="Nome de usuário:",
            widget=forms.TextInput(attrs={
                'id': 'id_username',
                'class': 'form-control',
                'placeholder': 'Seu nome de usuário...',
                'required': True
            }),
            help_text="Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas."
        )
        self.fields['email'] = forms.EmailField(
            label="E-mail:",
            widget=forms.TextInput(attrs={
                'id': 'id_email',
                'class': 'form-control',
                'placeholder': 'Seu e-mail...',
                'required': True
            })
        )
        self.fields['password1'] = forms.CharField(
            label="Senha:",
            widget=forms.PasswordInput(attrs={
                'type': 'password',
                'class': 'form-control form-control-user',
                'id': 'id_password1',
                'name': 'password1',
                'placeholder': '********',
                'required': True
            }),
            help_text="""
            <ul class="pl-4">
            <li>Sua senha não pode ser muito parecida com o resto das suas informações pessoais.</li>
            <li>Sua senha precisa conter pelo menos 8 caracteres.</li>
            <li>Sua senha não pode ser uma senha comumente utilizada.</li>
            <li>Sua senha não pode ser inteiramente numérica.</li>
            </ul>
        """
        )
        self.fields['password2'] = forms.CharField(
            label="Confirmação da senha:",
            widget=forms.PasswordInput(attrs={
                'type': 'password',
                'class': 'form-control form-control-user',
                'id': 'id_password2',
                'name': 'password2',
                'placeholder': '********',
                'required': True
            }),
            help_text="Informe a mesma senha informada anteriormente, para verificação."
        )
        self.fields['is_staff'] = forms.BooleanField(
            label="É da equipe:",
            required=False,
            widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_staff'
            })
        )
        self.fields['is_superuser'] = forms.BooleanField(
            label="É superusuário:",
            required=False,
            widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_superuser'
            })
        )
        self.fields['groups'] = forms.ModelMultipleChoiceField(
            queryset=Group.objects.all(),
            label='Grupos',
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )
        self.fields['user_permissions'] = forms.ModelMultipleChoiceField(
            queryset=Permission.objects.filter(
                content_type__app_label__in=[
                    'auth',
                    'blog',
                    'crm_financeiro',
                    'landing_page'
                ]
            ),
            label="Permissões:",
            widget=forms.CheckboxSelectMultiple()
        )
