#!/usr/bin/python3
"""
This module contains places view routes for api v1
"""
from api.v1.helpers import del_keys
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=["GET", "POST"])
def places(city_id):
    """
    Place routes for getting all places and creating a new one

    Methods:
    Accepts GET and POST method

    Args:
    city_id: The id of the city to create the place under.
    for post request
    """
    print("Request recieved")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)
        check_list = ["user_id", "name"]
        for check in check_list:
            if not data.get(check, None):
                response = jsonify({"error": "Missing {}".format(check)})
                return make_response(response, 400)
        user_id = data.get("user_id")
        name = data.get("password")
        user = storage.get(User, user_id)
        if not user:
            return abort(404)
        place = Place(user_id=user_id, name=name, city_id=city_id)
        place.save()
        response = jsonify(place.to_dict())
        return make_response(response, 201)

    all_places = storage.all(Place).values()
    response = jsonify([obj.to_dict()
                       for obj in all_places if obj.city_id == city_id])
    return make_response(response, 200)


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["GET", "PUT", "DELETE"])
def place(place_id):
    """
    Place route to retrieve, update or delete a place.

    Methods:
        Accepts GET, PUT and DELETE requests

    Args:
        place_id: The ID of the place to retrieve, update or delete
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if not data:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)
        cols_ignore = ["id", "user_id",
                       "city_id", "created_at", "updated_at"]
        del_keys(cols_ignore, data)
        for col, value in data.items():
            if hasattr(place, col):
                setattr(place, col, value)
        place.save()

    response = jsonify(place.to_dict())
    return make_response(response, 200)
