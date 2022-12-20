#!/usr/bin/python3
""" user endpoint
"""
from api.buyer.v1.views import user_views
from flask import abort, jsonify, make_response, request, url_for
from hashlib import sha256
from models import storage
from models.buyer import Buyer


@user_views.route("/user/<user_id>",
                  methods=["GET", "PUT"],
                  strict_slashes=False)
def manage_user(user_id):
    """user endpoint for read and update ops related
       to user details
       Args: user_id
       Return: jsonified dictionary representation of
               user on success
       file: user.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # User search and validation
    user = storage.search(Buyer, user_id)
    if not user:
        abort(404)

    # Get specific user
    if request.method == "GET":
        return make_response(jsonify(modify_user_output(user)), 200)

    # Update user account
    data = request.get_json()
    if not data:
        abort(400)

    # a. Updated password
    if "new_password" in data.keys():
        new_password = data.get("new_password")
        old_password = data.get("old_password")
        if not new_password or not old_password:
            abort(401)

        old_password = sha256("{}{}".format(old_password, user.salt).
                              encode('utf-8')).hexdigest()
        if old_password != user.password:
            abort(401)
        user.password = sha256("{}{}".format(new_password, user.salt).
                               encode('utf-8')).hexdigest()
        storage.save()
        return jsonify({"status": "Success"})

    # b. Update other attributes
    for key, value in data.items():
        if hasattr(user, key) and key not in attr_ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(modify_user_output(user))


@user_views.route("/user", strict_slashes=False)
def get_all_users():
    """user endpoint for creating new user
       Args: None
       Return: jsonified dictionary representation of
               created user
    file: user.yml
    """
    data = storage.all(Buyer)
    users = {"count": len(data), "users":
             [modify_user_output(user) for user in data]}
    return jsonify(users)


def modify_user_output(user):
    """ Formats dictionary representation of each
        user
        Args: user (object) - user object
        Return: dictionary represention of user
    """

    user_dict = user.to_dict()
    user_dict.pop("id")
    user_dict.pop("password")
    addresses = [url_for("views.manage_address", address_id=address.id)
                 for address in user.addresses]
    cards = [url_for("views.manage_card", card_id=card.id)
             for card in user.cards]
    user_dict.update({"shipping addresseses": addresses, "cards": cards})
    return user_dict
