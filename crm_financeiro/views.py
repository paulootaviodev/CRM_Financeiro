from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomLoginForm, ClientForm
from .models import Client


class CustomLoginView(LoginView):
    template_name = 'crm_financeiro/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/index.html"


class RegisterCustomer(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/register_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = ClientForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = Client()

            client.full_name = form.cleaned_data['full_name']
            client.cpf = form.cleaned_data['cpf']
            client.city = form.cleaned_data['city']
            client.state = form.cleaned_data['state']
            client.marital_status = form.cleaned_data['marital_status']
            client.birth_date = form.cleaned_data['birth_date']
            client.employment_status = form.cleaned_data['employment_status']
            client.phone = form.cleaned_data['phone']
            client.email = form.cleaned_data['email']
            client.privacy_policy = form.cleaned_data['privacy_policy']
            client.save()

            return JsonResponse({"success": True}, status=200)
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)    
