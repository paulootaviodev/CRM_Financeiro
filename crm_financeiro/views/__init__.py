from .login import CustomLoginView, CustomLogoutView
from .dashboard import Dashboard
from .customer import RegisterCustomer, ClientFormActionRouter, ListCustomers, ClientCSVExportView
from .customer import DetailCustomer, CustomerDeleteView, CustomerDeactivateView, UpdateCustomer
from .simulation import SimulationFormActionRouter, ListSimulations, SimulationsCSVExportView
from .simulation import DetailSimulation, SimulationDeleteView
from .loan_proposal import ListLoanProposals, LoanProposalsCSVExportView, LoanProposalsFormActionRouter
from .loan_proposal import CreateLoanProposal, DetailLoanProposal, LoanProposalCancellationView
from .loan_proposal import LoanProposalPaymentView, ReplyLoanProposalView, SendLoanProposalEmailView

__all__ = [
    "CustomLoginView",
    "CustomLogoutView",
    "Dashboard",
    "RegisterCustomer",
    "ClientFormActionRouter",
    "ListCustomers",
    "ClientCSVExportView",
    "DetailCustomer",
    "CustomerDeleteView",
    "CustomerDeactivateView",
    "UpdateCustomer",
    "SimulationFormActionRouter",
    "ListSimulations",
    "SimulationsCSVExportView",
    "DetailSimulation",
    "SimulationDeleteView",
    "ListLoanProposals",
    "LoanProposalsCSVExportView",
    "LoanProposalsFormActionRouter",
    "CreateLoanProposal",
    "DetailLoanProposal",
    "LoanProposalCancellationView",
    "LoanProposalPaymentView",
    "ReplyLoanProposalView",
    "SendLoanProposalEmailView"
]
