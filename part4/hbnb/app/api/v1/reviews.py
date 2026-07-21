#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_post_response = api.model('Review post marshal', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
    'user_id': fields.String,
    'place_id': fields.String,
})

review_list_response = api.model('Review list marshal', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
})

review_update_response = api.model('Review update marshal', {
    'text': fields.String,
    'rating': fields.Integer
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_post_response)
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        place = facade.get_place(review_data["place_id"])
        if not place:
            return {"error": "PLace not found"}, 404

        review_data["user_id"] = current_user
        
        if place.owner_id == current_user:
            api.abort(400, "Uh uh, thats your place, no fraud please")
        for review in place.reviews:
            if review.user.id == current_user:
                api.abort(400, "You have already reviewed this place")

        new_review = facade.create_review(review_data)
        if not new_review:
            return {"error": "Invalid input data"}
        return new_review, 201

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_list_response)
    def get(self):
        reviews = facade.get_all_reviews()
        return reviews


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_post_response)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    @api.expect(review_update_response)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information, check if it is users"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if review.user.id != current_user and not get_jwt()['is_admin']:
            return {"error": "Unauthorised action"}, 403
        review = facade.update_review(review_id, api.payload)
        if not review:
            return {'error': 'Review not found'}, 404
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if review.user.id != current_user and not get_jwt()['is_admin']:
            return {"error": "Unauthorised action"}, 403
       
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
