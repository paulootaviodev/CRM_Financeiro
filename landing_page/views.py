from json import JSONDecodeError
import requests
from .forms import CreditSimulationForm
from .models import CreditSimulationLead
from django.http import JsonResponse
from os import getenv
from django.conf import settings
from django.views.generic import TemplateView
from utils.rate_limit import rate_limited_view # type: ignore
from utils.cloudflare import validate_turnstile # type: ignore

API_URL = getenv('API_URL')


def create_credit_simulation_lead_object(
        form_data, released_value=None, number_of_installments=None,
        value_of_installments=None, api_status=None
    ):
    lead = CreditSimulationLead()

    lead.full_name = form_data.cleaned_data['full_name']
    lead.cpf = form_data.cleaned_data['cpf']
    lead.city = form_data.cleaned_data['city']
    lead.state = form_data.cleaned_data['state']
    lead.marital_status = form_data.cleaned_data['marital_status']
    lead.birth_date = form_data.cleaned_data['birth_date']
    lead.employment_status = form_data.cleaned_data['employment_status']
    lead.phone = form_data.cleaned_data['phone']
    lead.email = form_data.cleaned_data['email']
    lead.released_value = released_value or 0
    lead.number_of_installments = number_of_installments or 0
    lead.value_of_installments = value_of_installments or 0
    lead.privacy_policy = form_data.cleaned_data['privacy_policy']
    lead.api_status = api_status or 500
    
    lead.save()


class LandingPage(TemplateView):
    template_name = 'landing_page_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreditSimulationForm()
        context['turnstile_sitekey'] = settings.CLOUDFLARE_TURNSTILE_SITE_KEY
        return context
    
    def post(self, request, *args, **kwargs):
        rate_limit_response = rate_limited_view(request)
        if rate_limit_response:
            return rate_limit_response
        
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        if not validate_turnstile(turnstile_response):
            return JsonResponse({"success": False}, status=400)
        
        form = CreditSimulationForm(request.POST)
        if form.is_valid():
            try:
                # Prepare headers for the API request
                headers = {"Accept": "application/json", "Content-Type": "application/json"}

                # Make the request to the API
                payload = {
                    "full_name": form.cleaned_data["full_name"],
                    "cpf": form.cleaned_data["cpf"],
                    "city": form.cleaned_data["city"],
                    "state": form.cleaned_data["state"],
                    "marital_status": form.cleaned_data["marital_status"],
                    "birth_date": form.cleaned_data["birth_date"],
                    "employment_status": form.cleaned_data["employment_status"],
                    "phone": form.cleaned_data["phone"],
                    "email": form.cleaned_data["email"],
                    "privacy_policy": form.cleaned_data["privacy_policy"],
                }
                response = requests.post(API_URL, json=payload, headers=headers)

                http_status_code = response.status_code
                if http_status_code == 200:
                    response_data = response.json()
                    response_released_value = response_data.get('released_value', 0.00)
                    response_number_of_installments = response_data.get('number_of_installments', 0.00)
                    response_value_of_installments = response_data.get('value_of_installments', 0.00)

                    # Saves encrypted data to the database
                    create_credit_simulation_lead_object(
                        form, response_released_value, response_number_of_installments,
                        response_value_of_installments, api_status=http_status_code
                    )

                    formatted_value = f"{float(response_released_value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    return JsonResponse({"success": True, "data": f"R$ {formatted_value}"}, status=http_status_code)
                else:
                    create_credit_simulation_lead_object(form, api_status=http_status_code)
                    return JsonResponse({"success": False}, status=http_status_code)
                
            except (requests.RequestException, JSONDecodeError):
                return JsonResponse({"success": False}, status=500)
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)
