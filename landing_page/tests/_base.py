from datetime import date
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.cpf_generator import generate_cpf

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def generate_simulation_data() -> dict:
    simulation_data = {
        "full_name": "Test Case",
        "cpf": generate_cpf(),
        "phone": "35988887777",
        "email": "testcase@email.com",
        "city": "São Paulo",
        "state": "SP",
        "birth_date": date(2000, 1, 1),
        "marital_status": "S",
        "employment_status": "2",
        "privacy_policy": True,
        "released_value": 1200.00,
        "number_of_installments": 48,
        "value_of_installments": 50.00,
        "api_status": 200
    }
    return simulation_data


class BaseClassForLiveServerTesting(StaticLiveServerTestCase):
    """Base class that can be used in all LiveServerTestCase tests."""

    def setUp(self):
        """Initial setup for each individual test."""

        self.simulation_data = generate_simulation_data()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def tearDown(self):
        """Terminates the driver after each test."""
        self.driver.quit()
