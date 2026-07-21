#!/usr/bin/python3


from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
amenity_post_response = api.model('Amenity Marshal', {
    'id': fields.String,
    'name': fields.String,
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_post_response)
    @jwt_required()

    def post(self):
        """Register a new amenity"""
        if not get_jwt()['is_admin']:
            return {'error': 'Administrator privileges required'}, 403
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            api.abort(400, str(e))
        return new_amenity, 201

    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_post_response)
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        if not get_jwt()['is_admin']:
            return {'error': 'Admin privileges required'}, 403
        updated_amenity= facade.update_amenity(amenity_id, api.payload)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {"message": "Amenity updated succesfully"}, 200
