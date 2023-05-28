#!/usr/bin/python3
"""
This module contains places view routes for api v1
"""
from api.v1.helpers import del_keys
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"])
def places(city_id):
    """Place routes for getting all places and creating a new one"""
    print("Request recieved")
    city = storage.get(City, city_id)
    if not city:
        raise NotFound
    if request.method == "POST":
        try:
            data = request.get_json()
            check_list = ["user_id", "name"]
            for check in check_list:
                if not data.get(check, None):
                    response = jsonify({"error": "Missing {}".format(check)})
                    return make_response(response, 404)
            user_id = data.get("user_id")
            name = data.get("password")
            user = storage.get(User, user_id)
            if not user:
                raise NotFound
            place = Place(user_id=user_id, name=name, city_id=city_id)
            place.save()
            response = jsonify(place.to_dict())
            return make_response(response, 201)

        except BadRequest:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)

    all_places = storage.all(Place).values()
    response = jsonify([obj.to_dict()
                       for obj in all_places if obj.city_id == city_id])
    return make_response(response, 200)


@app_views.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"])
def place(place_id):
    """Place route to retrieve, update or delete a place."""
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        try:
            data = request.get_json()
            cols_ignore = ["id", "user_id",
                           "city_id", "created_at", "updated_at"]
            del_keys(cols_ignore, data)
            for col, value in data.items():
                setattr(place, col, value)
            place.save()
        except BadRequest:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)
    response = jsonify(place.to_dict())
    return make_response(response, 200)
