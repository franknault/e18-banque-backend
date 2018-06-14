from django.test import TestCase


class GetTest(TestCase):

    def test_clients_get(self):
        response = self.client.get('/api/clients')
        self.assertEqual(response.status_code, 200)

    def test_clients_entreprises_get(self):
        response = self.client.get('/api/clients/particuliers')
        self.assertEqual(response.status_code, 200)

    def test_clients_entreprises_get(self):
        response = self.client.get('/api/clients/entreprises')
        self.assertEqual(response.status_code, 200)
