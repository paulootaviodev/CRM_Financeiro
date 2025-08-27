from django.urls import path
from crm_financeiro.views import (
    DetailInstallment,
    InstallmentFormActionRouter,
    InstallmentsCSVExportView,
    ListInstallments
)

urlpatterns = [
    path("installments-action-router/", InstallmentFormActionRouter.as_view(), name="installments_action_router"),
    path("exportar-parcelas/", InstallmentsCSVExportView.as_view(), name="export_installments"),
    path("parcela/<slug:slug>/", DetailInstallment.as_view(), name="detail_installment"),
    path("listar-parcelas/", ListInstallments.as_view(), name="list_installments")
]
