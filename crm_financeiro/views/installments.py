from ..models import Installment
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from ..forms import InstallmentFilterForm
from utils.search_queryset import search
from django.utils.timezone import now
from django.urls import reverse
from django.shortcuts import redirect

import csv
from urllib.parse import urlencode

class InstallmentFormActionRouter(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', 'filter')

        if action == 'export':
            # Redirect to export view, keeping filters
            return redirect(f"{reverse('export_installments')}?{urlencode(request.GET)}")
        else:
            # Redirect to list view with filters
            return redirect(f"{reverse('list_installments')}?{urlencode(request.GET)}")


class ListInstallments(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_installments.html"
    model = Installment
    context_object_name = 'installments'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InstallmentFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return search(search_params, base_queryset, 'loan_proposal__client')
        
        # Return empty queryset if no search input
        return self.model.objects.none()
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('crm_financeiro.view_installment'):
            raise PermissionDenied("Você não tem permissão para visualizar parcelas.")
        return super().dispatch(request, *args, **kwargs)


class InstallmentsCSVExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="parcelas-{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Nome do cliente', 'CPF do cliente', 'Status da proposta', 'Status de pagamento da proposta',
            'Número da parcela', 'Data de vencimento', 'Data de pagamento', 'Valor', 'Pago',
            'Está cancelado', 'Data Criado', 'Data Atualizado',
        ])

        for installment in queryset:
            writer.writerow([
                installment.loan_proposal.client.full_name,
                installment.loan_proposal.client.cpf,
                installment.loan_proposal.status,
                installment.loan_proposal.payment_status,
                installment.installment_number,
                installment.due_date,
                installment.payment_date,
                installment.amount,
                installment.is_paid,
                installment.is_canceled,
                installment.created_at,
                installment.updated_at
            ])

        return response

    def get_queryset(self):
        base_queryset = Installment.objects.all()
        return search(self.request.GET, base_queryset, 'loan_proposal__client')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('crm_financeiro.view_installment'):
            raise PermissionDenied("Você não tem permissão para visualizar parcelas.")
        return super().dispatch(request, *args, **kwargs)


class DetailInstallment(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_installments.html"
    model = Installment
    context_object_name = 'installment'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('crm_financeiro.view_installment'):
            raise PermissionDenied("Você não tem permissão para visualizar parcelas.")
        return super().dispatch(request, *args, **kwargs)
