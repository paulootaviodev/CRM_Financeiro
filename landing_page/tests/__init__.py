from .test_urls import LandingPageURLsTest
from .test_models import LandingPageModelsTest
from .test_live_server import LandingPageSeleniumE2ETest
from .test_forms import LandingPageFormsTest

__all__ = [
    'LandingPageURLsTest',
    'LandingPageModelsTest',
    'LandingPageSeleniumE2ETest',
    'LandingPageFormsTest'
]
