#!/usr/bin/python3

"""Api version 1 index views."""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route("/status")
def status():
    """Return the status the api."""
    ans = {'status': 'OK'}
    return jsonify(ans)


@app_views.route("/stats")
def stats():
    """Returns the stats of all tables."""
    storage.reload()
    stats = {k: storage.count(v) for k, v in classes.items()}
    return jsonify(stats)
