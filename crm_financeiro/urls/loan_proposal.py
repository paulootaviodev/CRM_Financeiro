from django.urls import path
from crm_financeiro.views import (
    CreateLoanProposal,
    DetailLoanProposal,
    ListLoanProposals,
    LoanProposalCancellationView,
    LoanProposalPaymentView,
    LoanProposalsCSVExportView,
    LoanProposalsFormActionRouter,
    ReplyLoanProposalView,
    SendLoanProposalEmailView
)

urlpatterns = [
    path("criar-proposta/<slug:slug>/", CreateLoanProposal.as_view(), name="create_loan_proposal"),
    path("listar-propostas/", ListLoanProposals.as_view(), name="list_loan_proposals"),
    path("exportar-propostas/", LoanProposalsCSVExportView.as_view(), name="export_loan_proposals"),
    path("proposta/<slug:slug>/", DetailLoanProposal.as_view(), name="detail_loan_proposal"),
    path("delete-loan-proposal/<slug:slug>/", LoanProposalCancellationView.as_view(), name="delete_loan_proposal"),
    path("pay-loan-proposal/<slug:slug>/", LoanProposalPaymentView.as_view(), name="pay_loan_proposal"),
    path("response/<token>/<str:action>/<slug:slug>/", ReplyLoanProposalView.as_view(), name="reply_loan_proposal"),
    path("enviar-proposta/<slug:slug>/", SendLoanProposalEmailView.as_view(), name="send_loan_proposal"),
    path("loan-proposals-action-router/", LoanProposalsFormActionRouter.as_view(), name="loan_proposals_action_router")
]
