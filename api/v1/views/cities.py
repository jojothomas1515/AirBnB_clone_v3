#!/usr/bin/python3

"""Api routes for city resource."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from werkzeug.exceptions import BadRequest


@app_views.route("/cities/<string:city_id>", strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def cities(city_id: str):
    """City routes.

    This route accepts GET, POST, PUT, DELETE http methods

    GET: is use to get the city resources from the database,
    if an id is passed to it the it gets a single city object matching
    the city id passed. If it is unable to find the city it return a 404
    status code of not found.

    DELETE: this method deleete object matching it id from the storage in use,
    this method requires the city id

    PUT: this method is use to update resource or object already in the storage
    in use, and it requires the city id

    Args:
        city_id: id of the cities resource
    """
    if request.method == "GET":
        city = storage.get(City, city_id)
        return (jsonify(city.to_dict()), 200) if city else abort(404)

    elif request.method == "DELETE":
        city = storage.get(City, city_id)
        if not city:
            return abort(404)
        city.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        ignore = ['id', 'created_at', 'updated_at']
        try:
            city = storage.get(City, city_id)

            if not city:
                abort(404)
            else:
                data = request.get_json()

                for k, v in data.items():
                    if k in ignore:
                        continue
                    setattr(city, k, v)

                city.save()
                return jsonify(city.to_dict()), 200
        except BadRequest:
            return jsonify(error="Not a JSON"), 400


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=["GET", "POST"])
def state_cities(state_id: str):
    """
    Cities of a State

    GET: retrieve all the cities associated with a state on the storage

    POST: add a city to the state referenced by state_id

    Args:
       state_id: id  of the state the retrieved or added city is
           associated with.
    """

    if request.method == "GET":
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities = list(
            map(lambda city: city.to_dict(),
                state.cities)
            )
        return jsonify(cities), 200

    elif request.method == "POST":
        state = storage.get(State, state_id)

        if not state:
            abort(404)
        try:
            data = request.get_json()

            if 'name' not in data:
                return jsonify(error="Missing name"), 400
            data['state_id'] = state_id
            city = City(**data)
            city.save()

            return jsonify(city.to_dict()), 201
        except BadRequest:
            return jsonify(error="Not a JSON"), 400
