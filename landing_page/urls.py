from .views import LandingPage
from django.urls import path

urlpatterns = [
    path('', LandingPage.as_view(), name='landing_page'),
]
