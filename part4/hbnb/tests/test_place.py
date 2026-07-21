import unittest
from app.api.v1 import create_app
from test_helper import unique_email

class TestPlaceEndpoints(unittest.TestCase):
 
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a fresh owner for each test so Place creation has a
        # valid owner_id to reference, independent of test order.
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email("owner")
        })
        self.owner_id = user_response.json["id"]
 
    def test_create_valid_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
 
    def test_create_place_negative_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Price Place",
            "description": "Should fail validation",
            "price": -50.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
 
    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Latitude Place",
            "description": "Should fail validation",
            "price": 100.0,
            "latitude": 95.0,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
 
    def test_create_place_invalid_longitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Longitude Place",
            "description": "Should fail validation",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -200.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
 
    def test_create_place_empty_title(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "Should fail validation",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
 
    def test__get_nonexistent_place(self):
        response = self.client.get(
            '/api/v1/places/00000000-0000-0000-0000-000000000000'
        )
        self.assertEqual(response.status_code, 404)
