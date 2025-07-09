from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomLoginForm, ClientForm, ClientFilterForm
from django.utils.timezone import now
from urllib.parse import urlencode
from django.shortcuts import redirect
from .models import Client
import csv


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

            detail_url = reverse('detail_customer', kwargs={'slug': client.slug})
            return JsonResponse({"success": True, "redirect_url": detail_url}, status=200)
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)    


class ClientFormActionRouter(View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', 'filter')

        if action == 'export':
            # Redirect to export view, keeping filters
            return redirect(f"{reverse('export_customers')}?{urlencode(request.GET)}")
        else:
            # Redirect to list view with filters
            return redirect(f"{reverse('list_customers')}?{urlencode(request.GET)}")


class ListCustomers(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_customers.html"
    model = Client
    context_object_name = 'clients'
    paginate_by = 50
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_result = encrypted_search(self.request.GET, queryset)
        return search_result


class ClientCSVExportView(View):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="clients-{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Nome Completo', 'CPF', 'Telefone', 'Email', 'Cidade', 'Estado', 'Estado Civil',
            'Situação Empregatícia', 'Data de Nascimento', 'Cliente Desde',
            'Política de Privacidade', 'Cliente ativo'
        ])

        for client in queryset:
            writer.writerow([
                client.full_name,
                client.cpf,
                client.phone,
                client.email,
                client.city,
                client.get_state_display(),
                client.get_marital_status_display(),
                client.get_employment_status_display(),
                client.birth_date,
                client.client_since.strftime('%Y-%m-%d_%H-%M-%S'),
                client.privacy_policy,
                client.is_active
            ])

        return response

    def get_queryset(self):
        queryset = Client.objects.order_by('-id').all()
        search_result = encrypted_search(self.request.GET, queryset)
        return search_result


class DetailCustomer(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_customer.html"
    model = Client
    context_object_name = 'client'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


@staticmethod
def encrypted_search(params, queryset):
    search = params.get('search')
    state = params.get('state')
    marital_status = params.get('marital_status')
    employment_status = params.get('employment_status')

    birth_date_initial = params.get('birth_date_initial')
    birth_date_final = params.get('birth_date_final')
    client_since_initial = params.get('client_since_initial')
    client_since_final = params.get('client_since_final')

    if search:
        decrypted_matches = Client.objects.none()

        for obj in Client.objects.order_by('-id').iterator(chunk_size=128):
            try:
                fields = [obj.full_name, obj.cpf, obj.phone, obj.email, obj.city]
                if any(search.lower() in field.lower() for field in fields):
                    decrypted_matches |= Client.objects.order_by('-id').filter(pk=obj.pk)
            except Exception:
                continue  # Ignore decryption errors for invalid records

        # Replace queryset with decrypted search results
        queryset = decrypted_matches

    if state:
        queryset = queryset.filter(state=state)

    if marital_status:
        queryset = queryset.filter(marital_status=marital_status)

    if employment_status:
        queryset = queryset.filter(employment_status=employment_status)

    if birth_date_initial and birth_date_final:
        queryset = queryset.filter(birth_date__range=[birth_date_initial, birth_date_final])
    elif birth_date_initial:
        queryset = queryset.filter(birth_date__gte=birth_date_initial)
    elif birth_date_final:
        queryset = queryset.filter(birth_date__lte=birth_date_final)

    if client_since_initial and client_since_final:
        queryset = queryset.filter(client_since__range=[client_since_initial, client_since_final])
    elif client_since_initial:
        queryset = queryset.filter(client_since__gte=client_since_initial)
    elif client_since_final:
        queryset = queryset.filter(client_since__lte=client_since_final)

    return queryset
