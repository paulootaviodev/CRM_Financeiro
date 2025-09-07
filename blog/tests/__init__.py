from .test_urls import BlogURLsTest
from .test_models import BlogPostModelTest, ViewsPerMonthModelTest
from .test_live_server import BlogSeleniumE2ETest
from .test_forms import BlogFormsTest

__all__ = [
    'BlogURLsTest',
    'BlogPostModelTest',
    'ViewsPerMonthModelTest',
    'BlogSeleniumE2ETest',
    'BlogFormsTest'
]
