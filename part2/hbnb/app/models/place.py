#!/usr/bin/python3
"""Place model."""

from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Place class for property listings."""

    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Title is required and must be 100 characters or less.")

        if price <= 0:
            raise ValueError("Price must be a positive value.")

        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")

        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
            
#        if not isinstance(owner_id, User):
#            raise ValueError("Owner must be a User instance")

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

        owner_id.places.append(self)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an empty amenity to the place."""
        self.amenities.append(amenity)
        self.save()
