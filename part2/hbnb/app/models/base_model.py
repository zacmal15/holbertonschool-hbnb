#!/usr/bin/python3
"""Base model for all HBnB entities."""

import uuid
from datetime import datetime


class BaseModel:
    """Base class containing common attributes/methods for models."""

    def __init__(self):
        """Initialise id, created at, and updated at."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes using a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()
