#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_lamb1 = api.model('Review Marshal 1', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
    'user_id': fields.String(attribute='user.id'),
    'place_id': fields.String(attribute='place.id')
})

review_lamb2 = api.model('Review Marshal 1', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
})

review_lamb3 = api.model('Review marshal 3', {
    'text': fields.String,
    'rating': fields.Integer
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_lamb1)
    def post(self):
        """Register a new review"""
        review_data = api.payload
        new_review = facade.create_review(review_data)

        if not new_review:
            api.abort(400, 'Invalid input data')

        return new_review, 201

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_lamb2)
    def get(self):
        reviews = facade.get_all_reviews()
        return reviews


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_lamb1)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    @api.expect(review_lamb3)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review = facade.update_review(review_id, api.payload)
        if not review:
            return {'error': 'Review not found'}, 404
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
