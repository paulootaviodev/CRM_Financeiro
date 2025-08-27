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
from utils.credit_simulation_api_request import send_data_to_api
from crm_financeiro.templatetags.custom_filters import format_currency

API_URL = getenv('API_URL')


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
                # Prepare payload with cleaned form data
                fields = [
                    "full_name", "cpf", "city", "state", "marital_status", "birth_date",
                    "employment_status", "phone", "email", "privacy_policy"
                ]
                payload = {field: form.cleaned_data[field] for field in fields}
                
                # Make the API request
                response = send_data_to_api(payload, API_URL)
                http_status_code = response.status_code

                # If successful response
                if http_status_code == 200:
                    response_data = response.json()
                    response_released_value = response_data.get('released_value', 0.00)
                    response_number_of_installments = response_data.get('number_of_installments', 0.00)
                    response_value_of_installments = response_data.get('value_of_installments', 0.00)

                    # Saves encrypted data to the database
                    self.create_credit_simulation_lead_object(
                        form,
                        response_released_value,
                        response_number_of_installments,
                        response_value_of_installments,
                        http_status_code
                    )

                    # Format Brazilian currency output
                    formatted_released_value = format_currency(response_released_value)
                    formatted_value_of_installments = format_currency(response_value_of_installments)

                    # Return response
                    return JsonResponse(
                        {
                            "success": True, "data": f"R$ {formatted_released_value}"
                            f" em {response_number_of_installments}x"
                            f" de {formatted_value_of_installments}."
                        },
                        status=http_status_code
                    )
                # If the API returns error
                else:
                    self.create_credit_simulation_lead_object(form, api_status=http_status_code)
                    return JsonResponse({"success": False}, status=http_status_code)
            
            # API call or response parsing failed
            except (requests.RequestException, JSONDecodeError):
                return JsonResponse({"success": False}, status=500)
            
        # If form is invalid, return detailed errors
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "errors": errors}, status=400)

    @staticmethod
    def create_credit_simulation_lead_object(
            form_data,
            released_value=None,
            number_of_installments=None,
            value_of_installments=None,
            api_status=None
        ) -> None:
        """
        Saves a new CreditSimulationLead object to the database using form data and API results.
        """
        lead = CreditSimulationLead()

        # List of form fields that will be assigned to the lead
        form_fields = [
            'full_name', 'cpf', 'city', 'state', 'marital_status', 'birth_date',
            'employment_status', 'phone', 'email', 'privacy_policy'
        ]

        # Assign form fields to the lead
        for field in form_fields:
            setattr(lead, field, form_data.cleaned_data[field])

        # Assign API values ​​or defaults
        lead.released_value = released_value or 0
        lead.number_of_installments = number_of_installments or 0
        lead.value_of_installments = value_of_installments or 0
        lead.api_status = api_status or 500

        lead.save()
