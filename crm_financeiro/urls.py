from django.urls import path
from .views import Dashboard
from .views import CustomLoginView, CustomLogoutView, RegisterCustomer
from .views import ListCustomers, DetailCustomer

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path("cadastrar-cliente/", RegisterCustomer.as_view(), name="register_customer"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('listar-clientes/', ListCustomers.as_view(), name="list_customers"),
    path('cliente/<slug:slug>/', DetailCustomer.as_view(), name='detail_customer'),
]
