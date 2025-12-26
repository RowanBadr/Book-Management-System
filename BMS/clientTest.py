# Example of an integration test using Django's test client
from django.test import TestCase
from django.urls import reverse

class ServiceDiscoveryIntegrationTests(TestCase):
    def test_service_communication(self):
        response = self.client.get(reverse('call-inventory-service'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
