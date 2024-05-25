#!/usr/bin/python3
"""
Route for handling the link between Place objects and Amenity objects.
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenities = []
    if storage_type == 'db':
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
    elif storage_type == 'fs':
        for amenity_id in place.amenity_ids:
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or (storage_type == 'db' and amenity not in place.amenities) or (storage_type == 'fs' and amenity_id not in place.amenity_ids):
        abort(404)

    if storage_type == 'db':
        place.amenities.remove(amenity)
    elif storage_type == 'fs':
        place.amenity_ids.remove(amenity_id)

    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if storage_type == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    elif storage_type == 'fs':
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()

    return jsonify(amenity.to_dict()), 201

