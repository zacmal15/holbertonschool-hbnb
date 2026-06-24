import unittest
from app.api.v1 import create_app
from test_helper import unique_email

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_bad_email_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_user(self):
        response = self.client.get(
            '/api/v1/users/00000000-0000-0000-0000-000000000000'
        )
        self.assertEqual(response.status_code, 404)
