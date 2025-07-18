from os import getenv

from json import JSONDecodeError
import requests

from .forms import CreditSimulationForm
from .models import CreditSimulationLead
from django.http import JsonResponse
from utils.request_rate_limit import rate_limited_view
from django.conf import settings
from django.views.generic import TemplateView
from utils.cloudflare_captcha_validator import validate_turnstile

API_URL = getenv('API_URL')


def create_credit_simulation_lead_object(
        form_data,
        released_value=None,
        number_of_installments=None,
        value_of_installments=None,
        api_status=None
    ):
    """
    Saves a new CreditSimulationLead object to the database using form data and API results.
    """
    lead = CreditSimulationLead()

    # Assign form values
    lead.full_name = form_data.cleaned_data['full_name']
    lead.cpf = form_data.cleaned_data['cpf']
    lead.city = form_data.cleaned_data['city']
    lead.state = form_data.cleaned_data['state']
    lead.marital_status = form_data.cleaned_data['marital_status']
    lead.birth_date = form_data.cleaned_data['birth_date']
    lead.employment_status = form_data.cleaned_data['employment_status']
    lead.phone = form_data.cleaned_data['phone']
    lead.email = form_data.cleaned_data['email']
    lead.privacy_policy = form_data.cleaned_data['privacy_policy']

    # Assign API response values or defaults
    lead.released_value = released_value or 0
    lead.number_of_installments = number_of_installments or 0
    lead.value_of_installments = value_of_installments or 0
    lead.api_status = api_status or 500
    
    lead.save()


class LandingPage(TemplateView):
    template_name = 'landing_page/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreditSimulationForm()
        context['turnstile_sitekey'] = settings.CLOUDFLARE_TURNSTILE_SITE_KEY
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handles form submission:
        - Validates CAPTCHA
        - Calls external API
        - Saves data to database
        - Returns appropriate JSON response
        """
        # Rate-limiting check
        rate_limit_response = rate_limited_view(request)
        if rate_limit_response:
            return rate_limit_response
        
        # CAPTCHA validation using Cloudflare Turnstile
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        if not validate_turnstile(turnstile_response):
            return JsonResponse({"success": False}, status=400)
        
        # Validate form data
        form = CreditSimulationForm(request.POST)
        if form.is_valid():
            try:
                # Prepare headers for the API request
                headers = {"Accept": "application/json", "Content-Type": "application/json"}

                # Prepare payload with cleaned form data
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
                # Make the API request
                response = requests.post(API_URL, json=payload, headers=headers)
                http_status_code = response.status_code

                # If successful response
                if http_status_code == 200:
                    response_data = response.json()
                    response_released_value = response_data.get('released_value', 0.00)
                    response_number_of_installments = response_data.get('number_of_installments', 0.00)
                    response_value_of_installments = response_data.get('value_of_installments', 0.00)

                    # Saves encrypted data to the database
                    create_credit_simulation_lead_object(
                        form,
                        response_released_value,
                        response_number_of_installments,
                        response_value_of_installments,
                        api_status=http_status_code
                    )

                    # Format Brazilian currency output
                    formatted_value = f"{float(response_released_value):,.2f}" \
                        .replace(",", "X") \
                        .replace(".", ",") \
                        .replace("X", ".")

                    # Return response
                    return JsonResponse(
                        {"success": True, "data": f"R$ {formatted_value}"},
                        status=http_status_code
                    )
                # If the API returns error
                else:
                    create_credit_simulation_lead_object(form, api_status=http_status_code)
                    return JsonResponse({"success": False}, status=http_status_code)
            
            # API call or response parsing failed
            except (requests.RequestException, JSONDecodeError):
                return JsonResponse({"success": False}, status=500)
            
        # If form is invalid, return detailed errors
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)
