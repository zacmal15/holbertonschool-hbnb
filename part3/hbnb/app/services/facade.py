#!/usr/bin/python3

from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

###############################

  # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

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
        return self.user_repo.get_user_by_email(email)

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

        # Amenity ids were a pain in the arse so they go POP
        amenity_ids = place_data.pop("amenities_id", [])

        place = Place(**place_data)
        # lets put amenities back, BRUTE FORCE BABYYYY
        for ids in amenity_ids:
            amenity = self.amenity_repo.get(ids)
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
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews
    
    def get_reviews_by_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return user.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        if review in review.user.reviews:
            review.user.reviews.remove(review)
        self.review_repo.delete(review_id)
        return review
