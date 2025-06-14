from django.http import JsonResponse
from django.core.cache import cache
from django.utils.timezone import now

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def rate_limited_view(request):
    """Enforces request limit per IP for POST requests."""
    ip = get_client_ip(request)
    cache_key = f"rate_limit_POST_{ip}"
    client_requests, timestamp = cache.get(cache_key, (0, now()))
    elapsed_time = (now() - timestamp).seconds

    # Fixed limit of 3 POST requests per minute
    if elapsed_time < 60 and client_requests >= 3:
        return JsonResponse(
            {"error": "Too many POST requests. Try again later."},
            status=429
        )

    # Reset or increment the request count
    cache.set(cache_key, (1 if elapsed_time >= 60 else client_requests + 1, now()), timeout=60)

    return None  # Indicates that the limit has not been exceeded
