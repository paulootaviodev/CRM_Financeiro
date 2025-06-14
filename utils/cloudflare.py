from django.conf import settings
import requests

def validate_turnstile(response_token):
    """Validates the Turnstile token with the Cloudflare API."""
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        "secret": settings.CLOUDFLARE_TURNSTILE_SECRET_KEY,
        "response": response_token,
    }
    try:
        result = requests.post(url, data=data).json()
        return result.get("success", False)
    except Exception:
        return False
