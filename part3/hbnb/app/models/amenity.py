#!/usr/bin/python3
"""Amenity model."""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class fir place amenities."""

    def __init__(self, name):
        """Initialise an Amenity instance."""
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Name is required and must be 50 characters or less.")

        self.name = name
