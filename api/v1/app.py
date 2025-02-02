#!/usr/bin/python3

"""Api views."""

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, origins="0.0.0.0", resources="/*")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """Close database session."""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Error Handler for not found errors."""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    from os import getenv

    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')

    HOST = HOST if HOST else '0.0.0.0'
    PORT = int(PORT) if PORT else 5000

    app.run(HOST, port=PORT, threaded=True)
