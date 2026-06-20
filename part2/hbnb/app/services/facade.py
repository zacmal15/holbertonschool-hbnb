#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

###############################

  # Placeholder method for creating a user
    def create_user(self, user_data):
        if not User._valid_email(self, user_data['email']):
            return None
        existing_user = self.get_user_by_email(user_data['email'])
        if existing_user:
            return None

        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_user_list(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(data)
        return user

##########################################

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

############################################

# Placeholder method for fetching a place by ID
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            return None

        place = Place(**place_data)
        place.owner = owner
        place.amenities = []
        for amen in place_data['amenities_id']:
            amenity = self.amenity_repo.get(amen)
            if not amenity:
                return None
            place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if 'amenities_id' in place_data:
            amenities = []
            for amen in place_data['amenities_id']:
                amenity = self.amenity_repo.get(amen)
                if not amenity:
                    return None
                amenities.append(amenity)
            place_data['amenities'] = amenities

        place.update(place_data)
        return place

############################################

    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])

        if not user or not place:
            return None

        try:
            review = Review(**review_data)
        except (ValueError, TypeError):
            return None

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        pass
