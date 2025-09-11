from datetime import date
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from landing_page.forms import CreditSimulationForm
from ._base import generate_simulation_data


class LandingPageFormsTest(TestCase):
    """Test landing page forms validations"""

    def setUp(self):
        """Initial setup for each individual test."""
        self.simulation_data = generate_simulation_data()

    def test_form_is_valid_with_valid_data(self):
        """Test if form is valid with valid data"""

        form = CreditSimulationForm(data=self.simulation_data)
        self.assertTrue(form.is_valid())
    
    def test_validation_error_with_missing_data(self):
        """Test if validation error is raised when data is missing"""

        # This data is not used in the forms
        del self.simulation_data['released_value']
        del self.simulation_data['number_of_installments']
        del self.simulation_data['value_of_installments']
        del self.simulation_data['api_status']

        # Test each individual fields
        for field in self.simulation_data.keys():
            missing_data = self.simulation_data.copy()
            del missing_data[field]

            with self.subTest(field=field):
                form = CreditSimulationForm(data=missing_data)
                self.assertFalse(form.is_valid())
    
    def test_invalid_cpf_raises_validation_error(self):
        """Test if invalid CPF raises validation error"""

        self.simulation_data['cpf'] = '111.111.111-11'
        form = CreditSimulationForm(data=self.simulation_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_birth_date_raises_validation_error(self):
        """Test if validation error is raised when age is not between 18 and 80"""

        self.simulation_data['birth_date'] = date.today() - relativedelta(years=17)
        form = CreditSimulationForm(data=self.simulation_data)
        self.assertFalse(form.is_valid())

        self.simulation_data['birth_date'] = date.today() + relativedelta(years=81)
        form = CreditSimulationForm(data=self.simulation_data)
        self.assertFalse(form.is_valid())
    
    def test_privacy_policy_not_agreed_raises_validation_error(self):
        """Test if validation error is raised when privacy_policy is false"""

        self.simulation_data['privacy_policy'] = False
        form = CreditSimulationForm(data=self.simulation_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_phone_number_raises_validation_error(self):
        """Test if validation error is raised when phone number is invalid"""

        self.simulation_data['phone'] = '358888777'
        form = CreditSimulationForm(data=self.simulation_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_email_address_raises_validation_error(self):
        """Test if validation error is raised when email address is invalid"""

        self.simulation_data['email'] = 'test@email'
        form = CreditSimulationForm(self.simulation_data)
        self.assertFalse(form.is_valid())
