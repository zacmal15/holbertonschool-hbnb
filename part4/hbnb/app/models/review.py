#!/usr/bin/python3
"""Review model."""

from app.models.baseclass import BaseModel
from app.models.user import User
from app.models.place import Place
from app.extensions import db


class Review(BaseModel):
    """Review class for place reviews."""
    __tablename__ = 'reviews'

    __table_args__ = (db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),)

    text = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
