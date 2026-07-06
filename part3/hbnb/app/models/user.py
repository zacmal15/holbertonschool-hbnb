#!/usr/bin/python3
"""User model."""

import re
from app.models.base_model import BaseModel
from app.extensions import bcrypt, db

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

#
#    """User class for HBnB users."""
#
#    def __init__(self, first_name, last_name, email, password, is_admin=False):
#        """Initialise a User instance."""
#        super().__init__()
#
 #       if not first_name or len(first_name) > 50:
#            raise ValueError("First name is required and must be 50 characters or less.")
#
#        if not last_name or len(last_name) > 50:
#            raise ValueError("Last name is required and must be 50 characters or less.")
#
#        if not email or not self._valid_email(email):
#            raise ValueError("Valid email is required")
#
#        if not password:
#            raise ValueError("Password is required.")
#
 #       if not isinstance(is_admin, bool):
#           raise ValueError("is_admin must be a boolean.")
#        self.first_name = first_name
#        self.last_name = last_name
#        self.email = email
#        self.hash_password(password)
#        self.is_admin = is_admin
#        self.places = []
#        self.reviews = []
#
    def _valid_email(self, email):
        """Validate email frmat."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None
