from ..forms import CustomLoginForm
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'crm_financeiro/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'
