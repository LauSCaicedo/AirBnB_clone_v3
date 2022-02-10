#!/usr/bin/python3
<<<<<<< HEAD
"""Users"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users",
                 methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects: GET /api/v1/users"""
    list = []
    user_obj = storage.all(User).values()
    for a in user_obj:
        list.append(a.to_dict())
    return jsonify(list)


@app_views.route("/users/<user_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object: GET /api/v1/users/<user_id>"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    """Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    user_obj = storage.get(User, user_id)
    if user_obj:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users",
                 methods=['POST'],
                 strict_slashes=False)
def create_users():
    """Creates a User: POST /api/v1/users"""
    obj_request = request.get_json()
    if obj_request:
        if 'email' not in obj_request.keys():
            return "Missing email", 400
        if 'password' not in obj_request.keys():
            return "Missing password", 400

        new_user_obj = User(**obj_request)
        storage.new(new_user_obj)
        storage.save()
        current_state = storage.get(User, new_user_obj.id)
        return jsonify(current_state.to_dict()), 201
    else:
        return "Not a JSON", 400


@app_views.route("/users/<user_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def updates_users(user_id):
    """Updates a User object: PUT /api/v1/users/<user_id>"""
    user_obj = storage.get(User, user_id)
    obj_request = request.get_json()
    if user_obj:
        if obj_request:
            for key, value in obj_request.items():
                ignore = ["id", "email", "created_at", "updated_at"]
                if key not in ignore:
                    setattr(user_obj, key, value)
            storage.save()
            return (jsonify(user_obj.to_dict()), 200)
        else:
            return "Not a JSON", 400
    else:
        abort(404)
=======
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
>>>>>>> ca3c23b7c7c40809fa756105a35f50791fa28820
