from django.urls import path
from crm_financeiro.views import Dashboard

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard')
]
