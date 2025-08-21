from os import getenv

from ..models import Client, LoanProposal, Installment
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import LoanProposal
from ..forms import LoanProposalFilterForm
from utils.search_queryset import search
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from utils.credit_simulation_api_request import send_data_to_api
from django.urls import reverse
from django.shortcuts import redirect
from utils.email_sender import send_email_response, check_custom_token
from django.core import signing
from django.db.models import Q
from django.shortcuts import render

import csv
from urllib.parse import urlencode
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_URL = getenv('API_URL')

def create_loan_proposal_object(client, simulation):
    """Create the loan proposal in the database."""

    loan_proposal = LoanProposal()
    loan_proposal.client = client
    loan_proposal.status = '0001'
    loan_proposal.payment_status = '0001'
    loan_proposal.released_value = simulation.get('released_value')
    loan_proposal.number_of_installments = simulation.get('number_of_installments')
    loan_proposal.value_of_installments = simulation.get('value_of_installments')
    loan_proposal.save()

    return loan_proposal

def create_installment_object(loan_proposal):
    """Create all installments of the loan proposal in the database."""

    created_at = datetime.today()
    new_due_date = (created_at + relativedelta(months=1)).replace(day=10)

    for i in range(1, loan_proposal.number_of_installments + 1, 1):
        installment = Installment()
        installment.loan_proposal = loan_proposal
        installment.installment_number = i
        installment.due_date = new_due_date.date()
        installment.amount = loan_proposal.value_of_installments
        installment.is_paid = False
        installment.save()

        # Next month
        new_due_date += relativedelta(months=1)


class CreateLoanProposal(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client = get_object_or_404(Client, slug=kwargs['slug'])

        restrictions = Installment.objects.order_by('-id').select_related('loan_proposal').filter(
            Q(loan_proposal__payment_status__in=["0003", "0004"]),
            loan_proposal__client=client,
            due_date__lt=now().date(),
            is_canceled=False
        ).exists() or client.marked_for_deletion or not client.is_active

        if restrictions:
            messages.error(
                request,
                "Não é possível gerar propostas para o cliente. O cliente possui restrições."
            )
            return redirect(reverse('detail_customer', kwargs={'slug': client.slug}))
        
        # Prepare payload with cleaned form data
        payload = {
            "full_name": client.full_name,
            "cpf": client.cpf,
            "city": client.city,
            "state": client.state,
            "marital_status": client.marital_status,
            "birth_date": client.birth_date,
            "employment_status": client.employment_status,
            "phone": client.phone,
            "email": client.email,
            "privacy_policy": client.privacy_policy,
        }
        # Make the API request
        simulation = send_data_to_api(payload, API_URL)
        
        # Create Loan Proposal
        loan_proposal = create_loan_proposal_object(client, simulation)

        messages.success(request, "Proposta gerada com sucesso.")
        return redirect(reverse('detail_loan_proposal', kwargs={'slug': loan_proposal.slug}))


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoanProposalFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_params = self.request.GET

        # Check if any search parameter is present
        if search_params:
            base_queryset = super().get_queryset()
            return search(search_params, base_queryset, 'client')
        
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
            'Valor das parcelas', 'Nome completo', 'CPF', 'Telefone', 'E-mail', 'Cidade',
            'Data criado', 'Data atualizado'
        ])

        for loan_proposal in queryset:
            writer.writerow([
                loan_proposal.get_status_display(),
                loan_proposal.get_payment_status_display(),
                loan_proposal.released_value,
                loan_proposal.number_of_installments,
                loan_proposal.value_of_installments,
                loan_proposal.client.full_name,
                loan_proposal.client.cpf,
                loan_proposal.client.phone,
                loan_proposal.client.email,
                loan_proposal.client.city,
                loan_proposal.created_at,
                loan_proposal.updated_at,
            ])

        return response

    def get_queryset(self):
        base_queryset = LoanProposal.objects.all()
        return search(self.request.GET, base_queryset, 'client')


class DetailLoanProposal(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_loan_proposal.html"
    model = LoanProposal
    context_object_name = 'loan_proposal'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class LoanProposalCancellationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        loan_proposal = get_object_or_404(LoanProposal, slug=kwargs['slug'])

        Installment.objects.order_by('-id').filter(
            loan_proposal=loan_proposal
        ).update(is_canceled=True)

        loan_proposal.status = "0006"
        loan_proposal.save()

        messages.success(request, "Proposta cancelada com sucesso.")
        return redirect(reverse('detail_loan_proposal', kwargs={"slug": loan_proposal.slug}))


class LoanProposalPaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Here you can implement your payment logic.
        loan_proposal = get_object_or_404(LoanProposal, slug=kwargs['slug'])
        create_installment_object(loan_proposal)
        loan_proposal.status = "0008"
        loan_proposal.save()

        messages.success(request, "Proposta paga com sucesso.")
        return redirect(reverse('detail_loan_proposal', kwargs={"slug": loan_proposal.slug}))


class SendLoanProposalEmailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        loan_proposal = get_object_or_404(LoanProposal, slug=kwargs['slug'])
        send_email_response(request, loan_proposal)
        loan_proposal.status = "0002"
        loan_proposal.save()

        messages.success(request, "Proposta enviada com sucesso.")
        return redirect(reverse('detail_loan_proposal', kwargs={"slug": loan_proposal.slug}))


class ReplyLoanProposalView(View):
    def get(self, request, *args, **kwargs):
        try:
            pk, slug, cpf_hash = check_custom_token(kwargs['token'])
            
            client = Client.objects.order_by('-id').get(
                pk=pk, slug=slug, cpf_hash=cpf_hash
            )
            loan_proposal = LoanProposal.objects.order_by('-id').get(
                client=client, slug=kwargs['slug'], status='0002'
            )
        except (signing.BadSignature, ValueError, Client.DoesNotExist, LoanProposal.DoesNotExist):
            return render(request, "crm_financeiro/email_response_error.html")

        status_map = {
            'accept': '0003',
            'refuse': '0004'
        }

        new_status = status_map.get(kwargs['action'])
        if not new_status:
            return HttpResponse("Ação inválida.", status=400)

        loan_proposal.status = new_status
        loan_proposal.save(update_fields=['status'])
        return render(request, "crm_financeiro/email_response.html")
