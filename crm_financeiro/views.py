from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'crm_financeiro/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/index.html"
