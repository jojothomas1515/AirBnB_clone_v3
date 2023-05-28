#!/usr/bin/python3

"""Api routes for state resource."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["POST", "GET"])
@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=["DELETE", "GET", "PUT"])
def states(state_id: str = None):
    """State routes.

    This route accepts GET, POST, PUT, DELETE http methods

    GET: is use to get the state resources from the database,
    if an id is passed to it the it gets a single state object matching
    the state id passed. If it is unable to find the state it return a 404
    status code of not found.
    If no is is passed, it returns all the states in the storage

    POST: this methos is us to create a new state object in the storage,
    it doesnt support state id

    DELETE: this method deleete object matching it id from the storage in use,
    this method requires the state id

    PUT: this method is use to update resource or object already in the storage
    in use, and it requires the state id

    Args:
        state_id: id of the states resource
    """
    if request.method == "GET":
        if state_id:
            state = storage.get(State, state_id)
            return (jsonify(state.to_dict()), 200) if state else abort(404)
        all_state = list(map(lambda state: state.to_dict(),
                             storage.all(State).values()))
        return jsonify(all_state), 200

    elif request.method == "DELETE":
        state = storage.get(State, state_id)
        if not state:
            return abort(404)
        else:
            state.delete()
            storage.save()
            return jsonify({}), 200

    elif request.method == "POST":
        try:
            new_state = request.get_json()

            if 'name' not in new_state:
                return jsonify(message="Missing name"), 400
            else:
                new_state = State(**new_state)
                new_state.save()
                return jsonify(new_state.to_dict()), 201

        except Exception:
            # will throw an exception if the data passed is not a valid
            # json object
            return jsonify(error="Not a JSON"), 400

    elif request.method == "PUT":
        ignore = ['id', 'created_at', 'updated_at']
        try:
            state = storage.get(State, state_id)

            if not state:
                abort(404)
            else:
                data = request.get_json()

                for k, v in data.items():
                    if k in ignore:
                        continue
                    setattr(state, k, v)

                state.save()
                return jsonify(state.to_dict()), 200
        except Exception:
            # will throw an exception if the data passed is not a valid
            # json object
            return jsonify(error="Not a JSON"), 400
