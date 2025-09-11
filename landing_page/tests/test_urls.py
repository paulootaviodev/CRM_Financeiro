from django.test import Client, TestCase
from django.urls import reverse


class LandingPageURLsTest(TestCase):
    """Test landing page URLs status code"""

    def test_landing_page_url_status_code_200_ok(self):
        """Test landing page status code is 200 ok"""
        
        client = Client()
        response = client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)
