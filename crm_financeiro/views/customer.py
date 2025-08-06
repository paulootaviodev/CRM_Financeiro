from ..forms import ClientFilterForm, UpdateClientForm
from landing_page.forms import CreditSimulationForm
from utils.encrypted_lead_search_engine import encrypted_search
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Client, Installment
from landing_page.models import CreditSimulationLead
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib import messages
from django.utils.timezone import now
from django.urls import reverse
from django.shortcuts import redirect

import csv
from urllib.parse import urlencode


class RegisterCustomerFromSimulation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        simulation = get_object_or_404(CreditSimulationLead, slug=kwargs['slug'])
        client = Client.objects.order_by('-id').filter(cpf_hash=simulation.cpf_hash).first()

        if client:
            messages.error(request, "Esse CPF já está cadastrado.")
            return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))

        fields_to_copy = [
            'full_name', 'cpf', 'phone', 'email', 'city', 'state',
            'marital_status', 'employment_status', 'birth_date', 'privacy_policy'
        ]

        client_data = {field: getattr(simulation, field) for field in fields_to_copy}
        client = Client.objects.create(**client_data)

        messages.success(request, "Cliente cadastrado com sucesso.")
        return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))


class RegisterCustomer(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/register_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = CreditSimulationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CreditSimulationForm(request.POST)
        
        if form.is_valid():
            client = Client(**form.cleaned_data)
            client.save()

            detail_url = reverse('detail_customer', kwargs={'slug': client.slug})
            return JsonResponse({"success": True, "redirect_url": detail_url}, status=200)
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)    


class ClientFormActionRouter(LoginRequiredMixin, View):
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
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return encrypted_search(search_params, base_queryset)
        
        # Return empty queryset if no search input
        return self.model.objects.none()


class ClientCSVExportView(LoginRequiredMixin, View):
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
        base_queryset = Client.objects.order_by('-id').all()
        search_result = encrypted_search(self.request.GET, base_queryset)
        return search_result


class DetailCustomer(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_customer.html"
    model = Client
    context_object_name = 'client'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class UpdateCustomer(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/update_customer.html"

    def get_client(self):
        return get_object_or_404(Client, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_client()
        context['client_form'] = UpdateClientForm(instance=client)

        return context
    
    def post(self, request, *args, **kwargs):
        client = self.get_client()
        form = UpdateClientForm(request.POST, instance=client)
        
        if form.is_valid():
            client = form.save(commit=False)
            client.phone = form.cleaned_data['phone']
            client.email = form.cleaned_data['email']
            client.save()

            detail_url = reverse('detail_customer', kwargs={'slug': client.slug})
            return JsonResponse({"success": True, "redirect_url": detail_url}, status=200)
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)


class CustomerDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client = get_object_or_404(Client, slug=kwargs['slug'])

        has_unpaid_installments = Installment.objects.filter(
            loan_proposal__client=client,
            is_paid=False
        ).exists()

        if has_unpaid_installments:
            messages.error(
                request,
                "Não é possível marcar o cliente para exclusão. Existem parcelas não quitadas associadas a ele."
            )
            return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))

        if client.marked_for_deletion == False:
            client.marked_for_deletion = True
            client.is_active = False
            client.deletion_request_date = now().date()
            messages.success(request, "Cliente marcado para exclusão com sucesso.")
        else:
            client.marked_for_deletion = False
            client.deletion_request_date = None
            messages.success(request, "Exclusão do cliente cancelada com sucesso.")
            
        client.save()
        return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))


class CustomerDeactivateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client = get_object_or_404(Client, slug=kwargs['slug'])

        has_unpaid_installments = Installment.objects.filter(
            loan_proposal__client=client,
            is_paid=False
        ).exists()

        if has_unpaid_installments:
            messages.error(
                request,
                "Não é possível desativar o cliente. Existem parcelas não quitadas associadas a ele."
            )
            return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))
        
        if client.marked_for_deletion == True:
            messages.error(
                request,
                "Não é possível ativar o cliente. Está conta já foi marcada para exclusão."
            )
            return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))
        
        client.is_active = False if client.is_active == True else True
        client.save()

        if client.is_active == True:
            messages.success(request, "Cliente ativado com sucesso.")
        else:
            messages.success(request, "Cliente desativado com sucesso.")

        return redirect(reverse('detail_customer', kwargs={"slug": client.slug}))
