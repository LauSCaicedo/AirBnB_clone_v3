#!/usr/bin/python3
<<<<<<< HEAD
"""palce"""

from crypt import methods
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id=None):
    """retrieves the list of all City objects"""
    all_places = []
    city_obj = storage.get("City", city_id)
    if city_obj:
        for place_obj in city_obj.places:
            all_places.append(place_obj.to_dict())
        return jsonify(all_places)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id=None):
    """retrieves a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """deletes a Place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a city object"""
    city_obj = storage.get("City", city_id)
    obj_request = request.get_json()
    try:
        if city_obj:
            if obj_request:
                if 'name' in obj_request and 'user_id' in obj_request:
                    new_place_obj = Place(**obj_request)
                    setattr(new_place_obj, "city_id", city_id)
                    new_place_obj.save()
                    return (jsonify(new_place_obj.to_dict()), 201)
                else:
                    if 'user_id' not in obj_request:
                        abort(400, "Missing user_id")
                    if 'name' not in obj_request:
                        abort(400, "Missing name")
            else:
                abort(400, "Not a JSON")
        else:
            abort(404)
    except IntegrityError:
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """updates a city object"""
    place_onj = storage.get(Place, place_id)
    obj_request = request.get_json()
    if place_onj:
        if obj_request:
            if 'name' in obj_request:
                for key, value in obj_request.items():
                    ignore = ["id", "user_id", "city_id",
                              "created_at", "updated_at"]
                    if key != ignore:
                        setattr(place_onj, key, value)
                place_onj.save()
                return jsonify(place_onj.to_dict()), 200
            else:
                return "Missing name", 400
        else:
            return "Not a JSON", 400
    else:
        abort(404)
=======
""" objects that handle all default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place Object
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
>>>>>>> ca3c23b7c7c40809fa756105a35f50791fa28820
