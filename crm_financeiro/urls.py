from django.urls import path
from .views import Dashboard
from .views import CustomLoginView, CustomLogoutView, RegisterCustomer
from .views import ListCustomers, ClientCSVExportView, DetailCustomer
from .views import ListSimulations, SimulationsCSVExportView, DetailSimulation
from .views import ClientFormActionRouter, SimulationFormActionRouter

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path("cadastrar-cliente/", RegisterCustomer.as_view(), name="register_customer"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('client-action-router/', ClientFormActionRouter.as_view(), name='client_action_router'),
    path('listar-clientes/', ListCustomers.as_view(), name="list_customers"),
    path('exportar-clientes/', ClientCSVExportView.as_view(), name="export_customers"),
    path('cliente/<slug:slug>/', DetailCustomer.as_view(), name='detail_customer'),
    path('simulation-action-router/', SimulationFormActionRouter.as_view(), name='simulation_action_router'),
    path('listar-simulacoes/', ListSimulations.as_view(), name="list_simulations"),
    path('exportar-simulacoes/', SimulationsCSVExportView.as_view(), name="export_simulations"),
    path('simulacao/<slug:slug>/', DetailSimulation.as_view(), name='detail_simulation')
]
