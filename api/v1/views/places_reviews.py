#!/usr/bin/python3
"""
This module contains reviews view routes for api v1
"""
from api.v1.helpers import del_keys
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from werkzeug.exceptions import NotFound


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"])
def reviews(place_id):
    """Review routes for getting all reviews and creating a new one"""
    print("Request recieved")
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound
    if request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)
        check_list = ["user_id", "text"]
        for check in check_list:
            if not data.get(check, None):
                response = jsonify({"error": "Missing {}".format(check)})
                return make_response(response, 400)
        user_id = data.get("user_id")
        text = data.get("text")
        user = storage.get(User, user_id)
        if not user:
            raise NotFound
        review = Review(user_id=user_id, text=text, place_id=place_id)
        review.save()
        response = jsonify(review.to_dict())
        return make_response(response, 201)

    all_reviews = storage.all(Review).values()
    response = jsonify([obj.to_dict()
                       for obj in all_reviews if obj.place_id == place_id])
    return make_response(response, 200)


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def review(review_id):
    """Review route to retrieve, update or delete a review."""
    review = storage.get(Review, review_id)
    if not review:
        raise NotFound
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if not data:
            response = jsonify({"error": "Not a JSON"})
            return make_response(response, 400)
        cols_ignore = ["id", "user_id",
                       "place_id", "created_at", "updated_at"]
        del_keys(cols_ignore, data)
        for col, value in data.items():
            if hasattr(review, col):
                setattr(review, col, value)
        review.save()
    response = jsonify(review.to_dict())
    return make_response(response, 200)
