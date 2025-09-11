from ._base import generate_simulation_data
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from landing_page.models import CreditSimulationLead


class LandingPageModelsTest(TestCase):
    """Test landing page models validations"""

    def setUp(self):
        """Initial setup for each individual test."""

        self.simulation_data = generate_simulation_data()
        self.simulation1 = CreditSimulationLead(**self.simulation_data)
        self.simulation1.save()
        self.simulation1.refresh_from_db()

    def test_object_is_created_with_valid_data(self):
        """Test if credit simulation object is created when data is valid"""

        for field in self.simulation_data.keys():
            with self.subTest(field=field):
                self.assertEqual(
                    self.simulation1.__getattribute__(field),
                    self.simulation_data.get(field)
                )

    def test_validation_error_when_creating_object_with_missing_data(self):
        """Test if validation error is raised when creating an object with missing data"""

        simulation_data = generate_simulation_data()
        del simulation_data['full_name']
        del simulation_data['cpf']
        del simulation_data['email']
        del simulation_data['phone']
        
        for field in simulation_data:
            with self.subTest(field=field):
                missing_data = simulation_data.copy()
                del missing_data[field]

                with self.assertRaises(ValidationError):
                    simulation = CreditSimulationLead(**missing_data)
                    simulation.full_clean()
        
        simulation_data['_encrypted_full_name'] = ''
        simulation_data['_encrypted_cpf'] = ''
        simulation_data['_encrypted_email'] = ''
        simulation_data['_encrypted_phone'] = ''

        with self.assertRaises(ValidationError):
            simulation = CreditSimulationLead(**simulation_data)
            simulation.full_clean()
    
    def test_slug_is_unique(self):
        """Test if the slug is unique when two objects are created with the same data"""

        simulation2 = CreditSimulationLead(**self.simulation_data)
        simulation2.save()
        simulation2.refresh_from_db()

        self.assertIsNotNone(self.simulation1.slug)
        self.assertIsNotNone(simulation2.slug)
        self.assertNotEqual(self.simulation1.slug, simulation2.slug)

        with self.assertRaises(IntegrityError):
            simulation2.slug = self.simulation1.slug
            simulation2.save()
    
    def test_duplicate_cpf_hash_is_allowed(self):
        """Test if duplicate cpf_hash is allowed"""

        try:
            simulation2 = CreditSimulationLead(**self.simulation_data)
            simulation2.save()
            simulation2.refresh_from_db()
        except IntegrityError:
            self.fail("It should be possible to create two objects with the same cpf_hash.")
        
        self.assertEqual(CreditSimulationLead.objects.filter(cpf_hash=self.simulation1.cpf_hash).count(), 2)
