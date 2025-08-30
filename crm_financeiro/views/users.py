from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from crm_financeiro.forms.users import UserRegisterForm, UserFilterForm, UserUpdateForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import View, UpdateView, ListView, DetailView, DeleteView
from django.utils.timezone import now
from utils.user_search import user_search
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from crm_financeiro.forms import ChangePasswordForm

import csv
from urllib.parse import urlencode


class RegisterUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'crm_financeiro/register_user.html'

    def form_valid(self, form):
        user = form.save()
        user.groups.set(form.cleaned_data['groups'])
        user.user_permissions.set(form.cleaned_data['user_permissions'])
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Usuário criado com sucesso.")
        return reverse('detail_user', kwargs={"username": self.object.username})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.add_user'):
            raise PermissionDenied("Você não tem permissão para criar usuários.")
        return super().dispatch(request, *args, **kwargs)


class UserFormActionRouter(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', 'filter')

        if action == 'export':
            # Redirect to export view, keeping filters
            return redirect(f"{reverse('export_users')}?{urlencode(request.GET)}")
        else:
            # Redirect to list view with filters
            return redirect(f"{reverse('list_users')}?{urlencode(request.GET)}")


class ListUsers(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_users.html"
    model = User
    context_object_name = 'users'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return user_search(search_params, base_queryset)
        
        # Return empty queryset if no search input
        return self.model.objects.none()
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.view_user'):
            raise PermissionDenied("Você não tem permissão para visualizar usuários.")
        return super().dispatch(request, *args, **kwargs)


class UsersCSVExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="users-{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Nome de usuário', 'E-mail', 'É da equipe', 'É administrador', 'Está ativo', 'Data criado'
        ])

        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.is_staff,
                user.is_superuser,
                user.is_active,
                user.date_joined
            ])

        return response

    def get_queryset(self):
        base_queryset = User.objects.all()
        return user_search(self.request.GET, base_queryset)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.view_user'):
            raise PermissionDenied("Você não tem permissão para visualizar usuários.")
        return super().dispatch(request, *args, **kwargs)


class DetailUser(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_user.html"
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.view_user'):
            raise PermissionDenied("Você não tem permissão para visualizar usuários.")
        return super().dispatch(request, *args, **kwargs)


class UpdateUser(LoginRequiredMixin, UpdateView):
    template_name = "crm_financeiro/update_user.html"
    model = User
    form_class = UserUpdateForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def form_valid(self, form):
        user = form.save()
        user.groups.set(form.cleaned_data['groups'])
        user.user_permissions.set(form.cleaned_data['user_permissions'])
        user.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, "Usuário atualizado com sucesso.")
        return reverse('detail_user', kwargs={"username": self.object.username})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.change_user'):
            raise PermissionDenied("Você não tem permissão para editar usuários.")
        return super().dispatch(request, *args, **kwargs)


class DeleteUser(LoginRequiredMixin, DeleteView):
    template_name = 'crm_financeiro/delete_user.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        messages.success(self.request, "Usuário excluido com sucesso.")
        return reverse('list_users')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.delete_user'):
            raise PermissionDenied("Você não tem permissão para excluir usuários.")
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'crm_financeiro/change_user_password.html'
    form_class = ChangePasswordForm

    def get_success_url(self):
        return reverse('change_user_password')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Apenas administradores podem acessar esta página.")
        return super().handle_no_permission()

    def form_valid(self, form):
        username = form.cleaned_data['username']
        new_password = form.cleaned_data['password1']
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        messages.success(self.request, f'Senha do usuário {username} alterada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao alterar a senha. Verifique os dados.')
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.change_user'):
            raise PermissionDenied("Você não tem permissão para editar usuários.")
        return super().dispatch(request, *args, **kwargs)
