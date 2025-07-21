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
]
