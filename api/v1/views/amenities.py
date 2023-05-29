#!/usr/bin/python3

"""Api routes for amenities resource."""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def amenities():
    """
    Execute different operations on the amenities resource depending on \
    which HTTP method was used.

    GET: Retrives all amenities in the data storage

    Args:
        amenity_id: the is the of a single amenity
    """

    all_amenities = list(
        map(lambda amenity: amenity.to_dict(),
            storage.all(Amenity).values()
            )
    )
    return jsonify(all_amenities), 200


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id: str):
    """
    Execute different operations on the amenities resource depending on \
    which HTTP method was used.

    GET: Retrives one amenity in the data storage

    Args:
        amenity_id: the is the of a single amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return (jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id: str):
    """
    Execute different operations on the amenities resource depending on \
    which HTTP method was used.

    DELETE: Delete one amenity in the data storage

    Args:
        amenity_id: the is the of a single amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def add_amenity():
    """
    Execute different operations on the amenities resource depending on \
    which HTTP method was used.

    POST: Add an amenity to the data storage

    Args:
        amenity_id: the is the of a single amenity
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="Not a JSON"), 400

    if 'name' not in data.keys():
        return jsonify(error="Missing name"), 400

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id: str):
    """
    Execute different operations on the amenities resource depending on \
    which HTTP method was used.

    POST: Update amenity in the data storage

    Args:
        amenity_id: the is the of a single amenity
    """

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json(silent=True)
    if not data:
        jsonify(error="Not a JSON"), 400
    for k, v in data.items():
        if k in ignore:
            continue
        setattr(amenity, k, v)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
