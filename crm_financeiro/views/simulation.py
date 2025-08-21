from landing_page.models import CreditSimulationLead
from utils.search_queryset import search
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils.timezone import now
from django.urls import reverse
from django.shortcuts import redirect
from ..forms import SimulationFilterForm

import csv
from urllib.parse import urlencode


class SimulationFormActionRouter(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', 'filter')

        if action == 'export':
            # Redirect to export view, keeping filters
            return redirect(f"{reverse('export_simulations')}?{urlencode(request.GET)}")
        else:
            # Redirect to list view with filters
            return redirect(f"{reverse('list_simulations')}?{urlencode(request.GET)}")


class ListSimulations(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_simulations.html"
    model = CreditSimulationLead
    context_object_name = 'simulations'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SimulationFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return search(search_params, base_queryset)

        # Return empty queryset if no search input
        return self.model.objects.none()


class SimulationsCSVExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="simulations-{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Nome Completo', 'CPF', 'Telefone', 'Email', 'Cidade', 'Estado', 'Estado Civil',
            'Situação Empregatícia', 'Data de Nascimento', 'Valor liberado', 'Criado em',
            'Política de Privacidade'
        ])

        for simulation in queryset:
            writer.writerow([
                simulation.full_name,
                simulation.cpf,
                simulation.phone,
                simulation.email,
                simulation.city,
                simulation.get_state_display(),
                simulation.get_marital_status_display(),
                simulation.get_employment_status_display(),
                simulation.birth_date,
                simulation.released_value,
                simulation.created_at.strftime('%Y-%m-%d_%H-%M-%S'),
                simulation.privacy_policy
            ])

        return response

    def get_queryset(self):
        base_queryset = CreditSimulationLead.objects.all()
        return search(self.request.GET, base_queryset)


class DetailSimulation(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_simulation.html"
    model = CreditSimulationLead
    context_object_name = 'simulation'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class SimulationDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        simulation = get_object_or_404(CreditSimulationLead, slug=kwargs['slug'])
        simulation.delete()

        messages.success(request, "Simulação deletada com sucesso.")
        return redirect(reverse('list_simulations'))
