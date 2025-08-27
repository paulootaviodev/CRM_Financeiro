from django.urls import path
from crm_financeiro.views import (
    ClientFormActionRouter,
    ClientCSVExportView,
    CustomerDeactivateView,
    CustomerDeleteView,
    DetailCustomer,
    ListCustomers,
    RegisterCustomer,
    RegisterCustomerFromSimulation,
    UpdateCustomer
)

urlpatterns = [
    path("cadastrar-cliente/", RegisterCustomer.as_view(), name="register_customer"),
    path("cadastrar-cliente-simulacao/<slug:slug>/", RegisterCustomerFromSimulation.as_view(),
         name="register_customer_from_simulation"),
    path("listar-clientes/", ListCustomers.as_view(), name="list_customers"),
    path("exportar-clientes/", ClientCSVExportView.as_view(), name="export_customers"),
    path("cliente/<slug:slug>/", DetailCustomer.as_view(), name="detail_customer"),
    path("delete-customer/<slug:slug>/", CustomerDeleteView.as_view(), name="delete_customer"),
    path("deactivate-customer/<slug:slug>/", CustomerDeactivateView.as_view(), name="deactivate_customer"),
    path("update-customer/<slug:slug>/", UpdateCustomer.as_view(), name="update_customer"),
    path("client-action-router/", ClientFormActionRouter.as_view(), name="client_action_router")
]
