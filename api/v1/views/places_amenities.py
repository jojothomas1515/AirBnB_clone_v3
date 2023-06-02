#!/usr/bin/python3

"""Api route point for place amenities."""

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", strict_slashes=True, methods=["GET"])
def place_amenity(place_id: str):
    """Get all the amenities associated with a place."""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if storage_t == 'db':
        amenities = place.amenities
        amenities = list(map(lambda x: x.to_dict(), amenities))
        return jsonify(amenities), 200
    else:
        amenity_ids = place.amenity_ids
        amenities = list(map(lambda a_id: storage.get(Amenity, a_id).to_dict(),
                             amenity_ids))
        return jsonify(amenities), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=True, methods=["POST"])
def add_place_amenity(place_id: str, amenity_id: str):
    """Adds an amenity to place."""

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
        place.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=True, methods=["DELETE"])
def delete_place_amenity(place_id: str, amenity_id: str):
    """Delete an amenity from place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200
    else:
        if amenity.id in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
        place.save()
        return jsonify({}), 200
