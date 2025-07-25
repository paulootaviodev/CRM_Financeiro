from django.http import HttpResponse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import LoanProposal
from ..forms import LoanProposalFilterForm
from utils.encrypted_lead_search_engine import encrypted_search
from django.utils.timezone import now
from django.urls import reverse
from django.shortcuts import redirect

import csv
from urllib.parse import urlencode


class LoanProposalsFormActionRouter(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', 'filter')

        if action == 'export':
            # Redirect to export view, keeping filters
            return redirect(f"{reverse('export_loan_proposals')}?{urlencode(request.GET)}")
        else:
            # Redirect to list view with filters
            return redirect(f"{reverse('list_loan_proposals')}?{urlencode(request.GET)}")


class ListLoanProposals(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_loan_proposals.html"
    model = LoanProposal
    context_object_name = 'loan_proposals'
    paginate_by = 50
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoanProposalFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return encrypted_search(search_params, base_queryset, 'Client')
        
        # Return empty queryset if no search input
        return self.model.objects.none()


class LoanProposalsCSVExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="propostas-{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Status', 'Status do pagamento', 'Valor liberado', 'Quantidade de parcelas',
            'Valor das parcelas', 'Nome completo', 'CPF', 'Telefone', 'E-mail', 'Cidade'
        ])

        for loan_proposal in queryset:
            writer.writerow([
                loan_proposal.status,
                loan_proposal.payment_status,
                loan_proposal.released_value,
                loan_proposal.number_of_installments,
                loan_proposal.value_of_installments,
                loan_proposal.client.full_name,
                loan_proposal.client.cpf,
                loan_proposal.client.phone,
                loan_proposal.client.email,
                loan_proposal.client.city
            ])

        return response

    def get_queryset(self):
        base_queryset = LoanProposal.objects.order_by('-id').all()
        search_result = encrypted_search(self.request.GET, base_queryset, 'Client')
        return search_result
