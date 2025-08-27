from django.urls import path
from crm_financeiro.views import (
    DetailSimulation,
    ListSimulations,
    SimulationDeleteView,
    SimulationFormActionRouter,
    SimulationsCSVExportView
)

urlpatterns = [
    path("listar-simulacoes/", ListSimulations.as_view(), name="list_simulations"),
    path("exportar-simulacoes/", SimulationsCSVExportView.as_view(), name="export_simulations"),
    path("simulacao/<slug:slug>/", DetailSimulation.as_view(), name="detail_simulation"),
    path("delete-simulation/<slug:slug>/", SimulationDeleteView.as_view(), name="delete_simulation"),
    path("simulation-action-router/", SimulationFormActionRouter.as_view(), name="simulation_action_router")
]
