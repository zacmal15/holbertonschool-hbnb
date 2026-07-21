#!/usr/bin/python3
"""Amenity model."""

from app.models.baseclass import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    """Amenity class fir place amenities."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
