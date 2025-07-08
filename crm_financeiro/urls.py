from django.urls import path
from .views import Dashboard
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView, RegisterCustomer

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path("cadastrar-cliente/", RegisterCustomer.as_view(), name="register_customer"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
