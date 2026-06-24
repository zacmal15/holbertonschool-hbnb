#!/usr/bin/python3
"""Review model."""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review class for place reviews."""

    def __init__(self, text, rating, place, user):
        """Initialise aReview instance."""
        super().__init__()

        if not text:
            raise ValueError("Review text is required")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance.")

        if not isinstance(user, User):
            raise ValueError("User must be a User instance.")

        self.text = text
        self.rating = int(rating)
        self.place = place
        self.user = user

        place.reviews.append(self)
        user.reviews.append(self)
