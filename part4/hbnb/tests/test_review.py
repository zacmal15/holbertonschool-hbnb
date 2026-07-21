import unittest
from app.api.v1 import create_app
from test_helper import unique_email

class TestReviewEndpoints(unittest.TestCase):
     
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a reviewer (not the place owner) for the happy-path tests.
        reviewer_response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": unique_email("jane.smith")
        })
        self.reviewer_id = reviewer_response.json["id"]
        # Create a separate owner and their place.
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email("john.doe")
        })
        self.owner_id = owner_response.json["id"]
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.place_id = place_response.json["id"]
 
    def test_create_valid_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay, very clean and comfortable!",
            "rating": 5,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
 
    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
 
    def test_create_review_invalid_references(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Fake review for testing",
            "rating": 3,
            "user_id": "00000000-0000-0000-0000-000000000000",
            "place_id": "00000000-0000-0000-0000-000000000000"
        })
        self.assertEqual(response.status_code, 400)
 
    def test_owner_cannot_review_own_place(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Reviewing my own place, this should fail",
            "rating": 5,
            "user_id": self.owner_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
