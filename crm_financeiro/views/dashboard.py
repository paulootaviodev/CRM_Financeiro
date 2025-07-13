from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/index.html"
