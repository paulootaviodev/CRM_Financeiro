from ._base import BaseClassForLiveServerTesting
from landing_page.forms import CreditSimulationForm
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep


class LandingPageSeleniumE2ETest(BaseClassForLiveServerTesting):
    """Performs tests with LiveServerTestCase on landing page."""

    def test_form_is_displayed(self):
        """Test if form is displayed."""

        self.driver.get(f"{self.live_server_url}{reverse("landing_page")}")

        form = CreditSimulationForm()
        labels_list = [field.label for _, field in form.fields.items()]

        for label in labels_list:
            with self.subTest(label=label):
                form_content = self.driver.find_element(By.ID, "credit-simulation-form").text
                self.assertIn(label, form_content)
    
    def test_form_is_working(self):
        """Test if form data is sent and result is received"""

        self.driver.get(f"{self.live_server_url}{reverse("landing_page")}")
        self.simulation_data['birth_date'] = '01/01/2000'

        type_fields = ['full_name', 'cpf', 'phone', 'email', 'city', 'birth_date']
        select_fields = ['state', 'marital_status', 'employment_status']

        for id in type_fields:
            form_field = self.driver.find_element(By.ID, id)
            form_field.send_keys(self.simulation_data[id])

        for id in select_fields:
            form_field = self.driver.find_element(By.ID, id)
            form_field = Select(form_field)
            form_field.select_by_value(self.simulation_data[id])

        privacy_policy_checkbox = self.driver.find_element(By.ID, 'privacy_policy')
        submit_btn = self.driver.find_element(By.ID, 'submit-form-btn')
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", privacy_policy_checkbox)
        sleep(2)
        
        privacy_policy_checkbox.click()
        submit_btn.click()

        sleep(4)
        simulation_result = self.driver.find_element(By.CLASS_NAME, 'form-container').text
        self.assertIn('Sucesso!', simulation_result)
