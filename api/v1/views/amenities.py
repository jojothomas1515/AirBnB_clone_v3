#!/usr/bin/python3

"""Api routes for amenities resource."""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/amenities", strict_slashes=False, methods=["GET", "POST"])
@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def amenities(amenity_id: str = None):
    """
    Execute different operations on the amenities resource depending on \
    which HTTP method was used.

    GET: Retrives one or all amenities in the data storage depending on wether
       amenity id was passed or not

    Args:
        amenity_id: the is the of a single amenity
   n """
    if request.method == "GET":
        if not amenity_id:
            all_amenities = list(
                map(lambda amenity: amenity.to_dict(),
                    storage.all(Amenity).values()
                    )
            )
            return jsonify(all_amenities), 200
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return (jsonify(amenity.to_dict()), 200)
    elif request.method == "DELETE":
        if not amenity_id:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        amenity.delete()
        storage.save()
        return (jsonify({}), 200)

    elif request.method == "POST":
        try:
            data = request.get_json()

            if 'name' not in data.keys():
                return jsonify({"error": "Missing name"}), 400

            amenity = Amenity(**data)
            amenity.save()
            return (jsonify(amenity.to_dict()), 201)
        except Exception:
            jsonify({"error": "Not a JSON"}), 400

    elif request.method == "PUT":
        if not amenity_id:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        try:
            ignore = ['id', 'created_at', 'updated_at']
            data = request.get_json()

            for k, v in data.items():
                if k in ignore:
                    continue
                setattr(amenity, k, v)
            amenity.save()

            return jsonify(amenity.to_dict()), 200
        except Exception:
            jsonify({"error": "Not a JSON"}), 400
