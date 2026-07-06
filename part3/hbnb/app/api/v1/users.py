#!/usr/bin/python3
"""User API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(
        required=True,
        description='Email of the user'
    ),
    'password': fields.String(
        required=True,
        description='Password of the user'
    )
})

user_lamb = api.model('User marshal', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
})


@api.route('/')
class UserList(Resource):
    """User list resource."""

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user."""
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"error": "Admin privileges required"}, 403
        
        user_data = api.payload

        if facade.get_user_by_email(user_data['email']):
            return {"error": 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        if new_user is None:
            api.abort(400, 'Invalid input data')

        return {
            'id': new_user.id,
            'message': 'User registered successfully'
        }, 201

    @api.response(200, 'User list retrieved successfully')
    @api.marshal_list_with(user_lamb)
    def get(self):
        """Get all users."""
        users = facade.get_user_list()
        return users, 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Single user resource."""

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID."""
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User does not exist')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_lamb)
    @jwt_required()
    def put(self, user_id):
        """Update user info."""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        user_data = request.json
        email = user_data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
        
        user = facade.update_user(user_id, api.payload)
        if not user:
            return {'error': 'User not found'}, 404
#        if 'email' in user or 'password' in user:
#            return {'error': 'You cannot modify email or password'}, 400
        return user, 200


@api.route('/<user_id>/reviews')
class UserReviewList(Resource):
    """User review list resource."""

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all reviews for a specific user."""
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        reviews = facade.get_reviews_by_user(user_id)

        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200
