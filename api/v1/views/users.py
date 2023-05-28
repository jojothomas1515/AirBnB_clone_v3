#!/usr/bin/python3
"""
This module contains users view routes for api v1
"""
from api.v1.helpers import del_keys
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.user import User
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/users', methods=["GET", "POST"])
def users():
    """User routes for getting all users and creating a new one"""
    if request.method == "POST":
        try:
            data = request.get_json()
            check_list = ["email", "password"]
            for check in check_list:
                if not data.get(check, None):
                    response = jsonify({"error": "Missing {}".format(check)})
                    return make_response(response, 404)
            email = data.get("email")
            password = data.get("password")
            user = User(email=email, password=password)
            user.save()
            response = jsonify(user.to_dict())
            return make_response(response, 201)

        except BadRequest:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)

    all_users = storage.all(User).values()
    response = jsonify([obj.to_dict() for obj in all_users])
    return make_response(response, 200)


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    """User route to retrieve, update or delete a user."""
    user = storage.get(User, user_id)
    if not user:
        raise NotFound
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        try:
            data = request.get_json()
            cols_ignore = ["id", "email", "created_at", "updated_at"]
            del_keys(cols_ignore, data)
            for col, value in data.items():
                if hasattr(user, col):
                    setattr(user, col, value)
            user.save()
        except BadRequest:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)
    response = jsonify(user.to_dict())
    return make_response(response, 200)
