from django.urls import path
from .views import (
    Dashboard,
    RegisterCustomer,
    CustomLoginView,
    CustomLogoutView,
    ClientFormActionRouter,
    ListCustomers,
    ClientCSVExportView,
    DetailCustomer,
    CustomerDeleteView,
    CustomerDeactivateView,
    UpdateCustomer,
    SimulationFormActionRouter,
    ListSimulations,
    SimulationsCSVExportView,
    DetailSimulation,
    SimulationDeleteView,
    ListLoanProposals,
    LoanProposalsCSVExportView,
    LoanProposalsFormActionRouter,
    CreateLoanProposal,
    DetailLoanProposal,
    LoanProposalCancellationView,
    LoanProposalPaymentView,
    ReplyLoanProposalView,
    SendLoanProposalEmailView,
    InstallmentFormActionRouter,
    InstallmentsCSVExportView,
    DetailInstallment,
    ListInstallments,
    CreateBlogPost,
    ListBlogPosts,
    DetailBlogPost,
    EditBlogPost
)

urlpatterns = [
    # Authentication
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Dashboard
    path('', Dashboard.as_view(), name='dashboard'),

    # Client
    path("cadastrar-cliente/", RegisterCustomer.as_view(), name="register_customer"),
    path("listar-clientes/", ListCustomers.as_view(), name="list_customers"),
    path("exportar-clientes/", ClientCSVExportView.as_view(), name="export_customers"),
    path("cliente/<slug:slug>/", DetailCustomer.as_view(), name="detail_customer"),
    path("delete-customer/<slug:slug>/", CustomerDeleteView.as_view(), name="delete_customer"),
    path("deactivate-customer/<slug:slug>/", CustomerDeactivateView.as_view(), name="deactivate_customer"),
    path("update-customer/<slug:slug>/", UpdateCustomer.as_view(), name="update_customer"),
    path("client-action-router/", ClientFormActionRouter.as_view(), name="client_action_router"),

    # Simulations
    path("listar-simulacoes/", ListSimulations.as_view(), name="list_simulations"),
    path("exportar-simulacoes/", SimulationsCSVExportView.as_view(), name="export_simulations"),
    path("simulacao/<slug:slug>/", DetailSimulation.as_view(), name="detail_simulation"),
    path("delete-simulation/<slug:slug>/", SimulationDeleteView.as_view(), name="delete_simulation"),
    path("simulation-action-router/", SimulationFormActionRouter.as_view(), name="simulation_action_router"),

    # Loan proposal
    path("criar-proposta/<slug:slug>/", CreateLoanProposal.as_view(), name="create_loan_proposal"),
    path("listar-propostas/", ListLoanProposals.as_view(), name="list_loan_proposals"),
    path("exportar-propostas/", LoanProposalsCSVExportView.as_view(), name="export_loan_proposals"),
    path("proposta/<slug:slug>/", DetailLoanProposal.as_view(), name="detail_loan_proposal"),
    path("delete-loan-proposal/<slug:slug>/", LoanProposalCancellationView.as_view(), name="delete_loan_proposal"),
    path("pay-loan-proposal/<slug:slug>/", LoanProposalPaymentView.as_view(), name="pay_loan_proposal"),
    path("response/<token>/<str:action>/<slug:slug>/", ReplyLoanProposalView.as_view(), name="reply_loan_proposal"),
    path("enviar-proposta/<slug:slug>/", SendLoanProposalEmailView.as_view(), name="send_loan_proposal"),
    path("loan-proposals-action-router/", LoanProposalsFormActionRouter.as_view(), name="loan_proposals_action_router"),

    # Installment
    path("installments-action-router/", InstallmentFormActionRouter.as_view(), name="installments_action_router"),
    path("exportar-parcelas/", InstallmentsCSVExportView.as_view(), name="export_installments"),
    path("parcela/<slug:slug>/", DetailInstallment.as_view(), name="detail_installment"),
    path("listar-parcelas/", ListInstallments.as_view(), name="list_installments"),

    # Blog
    path("criar-postagem/", CreateBlogPost.as_view(), name="create_blog_post"),
    path("listar-postagens/", ListBlogPosts.as_view(), name="list_blog_posts"),
    path("detalhar-postagem/<slug:slug>/", DetailBlogPost.as_view(), name="detail_blog_post"),
    path("editar-postagem/<slug:slug>/", EditBlogPost.as_view(), name="update_blog_post")
]
