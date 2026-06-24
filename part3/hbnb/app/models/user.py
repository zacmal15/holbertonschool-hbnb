#!/usr/bin/python3
"""User model."""

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """User class for HBnB users."""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialise a User instance."""
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be 50 characters or less.")

        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be 50 characters or less.")

        if not email or not self._valid_email(email):
            raise ValueError("Valid email is required")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def _valid_email(self, email):
        """Validate email frmat."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None
