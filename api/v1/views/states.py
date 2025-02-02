#!/usr/bin/python3

"""Api routes for state resource."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states():
    """State routes.

    This route accepts GET http method

    GET: get all the states available in the data storage

    Args:
        state_id: id of the states resource
    """
    all_state = list(map(lambda state: state.to_dict(),
                         storage.all(State).values()))
    return jsonify(all_state), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """State routes.

    This route accepts POST http method

    POST: create and add a new state to the data storage

    Args:
        state_id: id of the states resource
    """
    new_state = request.get_json(silent=True)

    if new_state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in new_state:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**new_state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def state(state_id: str):
    """State routes.

    This route accepts GET http method

    GET: retrieves a single state object matching
    the state id passed. If it is unable to find the state it return a 404
    status code of not found.

    Args:
        state_id: id of the states resource
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id: str):
    """State routes.

    This route accepts DELETE http method

    DELETE: deletes the state object matching
    the state id passed. If it is unable to find the state it return a 404
    status code of not found.

    Args:
        state_id: id of the states resource
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id: str):
    """State routes.

    This route accepts UPDATE http method

    PUT: updates the state object matching
    the state id passed. If it is unable to find the state it return a 404
    status code of not found.

    Args:
        state_id: id of the states resource
    """
    ignore = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in data.items():
        if k in ignore:
            continue
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
