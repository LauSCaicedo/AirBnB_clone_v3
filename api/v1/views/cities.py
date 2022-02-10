#!/usr/bin/python3
<<<<<<< HEAD
"""city"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id=None):
    """all City"""
    all_cities = []
    state_obj = storage.get("State", state_id)
    if state_obj:
        for city_obj in state_obj.cities:
            all_cities.append(city_obj.to_dict())
        return jsonify(all_cities)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """City object"""
    city_obj = storage.get("City", city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """deletes a City object"""
    city_obj = storage.get("City", city_id)
    if city_obj:
        storage.delete(city_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city object"""
    state_obj = storage.get("State", state_id)
    obj_request = request.get_json()
    if state_obj:
        if obj_request:
            if 'name' in obj_request:
                new_city_obj = City(**obj_request)
                setattr(new_city_obj, "state_id", state_id)
                new_city_obj.save()
                return (jsonify(new_city_obj.to_dict()), 201)
            else:
                return "Missing name", 400
        else:
            return "Not a JSON", 400
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def updates_city(city_id):
    """updates a city object"""
    city_obj = storage.get("City", city_id)
    obj_request = request.get_json()
    if city_obj:
        if obj_request:
            if 'name' in obj_request:
                for key, value in obj_request.items():
                    ignore = ["id", "state_id", "created_at", "updated_at"]
                    if key != ignore:
                        setattr(city_obj, key, value)
                city_obj.save()
                return jsonify(city_obj.to_dict())
            else:
                return "Missing name", 400
        else:
            return "Not a JSON", 400
    else:
        abort(404)
=======
""" objects that handles all default RestFul API actions for cities """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities(state_id):
    """
    Retrieves the list of all cities objects
    of a specific State, or a specific city
    """
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a specific city based on id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a city based on id provided
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def post_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """
    Updates a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
>>>>>>> ca3c23b7c7c40809fa756105a35f50791fa28820
