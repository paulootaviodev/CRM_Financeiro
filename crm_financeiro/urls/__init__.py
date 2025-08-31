from django.urls import path, include

# Import URL patterns from each module
from .authentication import urlpatterns as authentication_urls
from .dashboard import urlpatterns as dashboard_urls
from .client import urlpatterns as client_urls
from .simulations import urlpatterns as simulations_urls
from .loan_proposal import urlpatterns as loan_proposal_urls
from .installment import urlpatterns as installment_urls
from .blog import urlpatterns as blog_urls
from .users import urlpatterns as users_urls

# Combine all URL patterns into a single list
urlpatterns = [
    path('auth/', include((authentication_urls))),
    path('', include((dashboard_urls))),
    path('clients/', include((client_urls))),
    path('simulations/', include((simulations_urls))),
    path('proposals/', include((loan_proposal_urls))),
    path('installments/', include((installment_urls))),
    path('blog/', include((blog_urls))),
    path('users/', include((users_urls))),
]

# Explicitly define what is exported when someone uses `from crm_financeiro.urls import *`
__all__ = [
    'authentication_urls',
    'dashboard_urls',
    'client_urls',
    'simulations_urls',
    'loan_proposal_urls',
    'installment_urls',
    'blog_urls',
    'users_urls',
    'urlpatterns'  # Also export the combined urlpatterns for direct use
]
