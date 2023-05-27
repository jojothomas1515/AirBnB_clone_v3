#!/usr/bin/python3

"""Api version 1 index views."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Return the status the api."""
    ans = {'status': 'OK'}
    return jsonify(ans)
