#!/usr/bin/python3
""" Seller endpoint module
"""
from api.seller.v1.views import seller_views
from flask import abort, jsonify, make_response, request
from hashlib import sha256
from models import storage
from models.order_detail import OrderDetail
from models.seller import Seller


@seller_views.route("/sellers/<seller_id>",
                    methods=["GET", "DELETE", "PUT"],
                    strict_slashes=False)
def manage_seller(seller_id):
    """seller endpoint for read, update, delete ops related
       to seller details
       Args: seller_id
       Return: jsonified dictionary representation of
               seller on success
       file: seller.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Seller search and validation
    seller = storage.search(Seller, seller_id)
    if not seller:
        abort(404)
    # Get specific seller
    if request.method == "GET":
        return make_response(jsonify(modify_seller_output(seller)), 200)

    # Delete seller account
    if request.method == "DELETE":
        storage.delete(seller)
        return make_response(jsonify({}), 200)

    # Update seller account
    data = request.get_json()
    if not data:
        abort(400)
    # a. Updated password
    if "new_password" in data.keys():
        new_password = data.get("new_password")
        old_password = data.get("old_password")
        if not new_password or not old_password:
            abort(401)

        old_password = sha256("{}{}".format(old_password, seller.salt).
                              encode('utf-8')).hexdigest()
        if old_password != seller.password:
            abort(401)
        seller.password = sha256("{}{}".format(new_password, seller.salt).
                                 encode('utf-8')).hexdigest()
        storage.save()
        return jsonify({"status": "Success"})

    for key, value in data.sellers():
        if hasattr(seller, key) and key not in attr_ignore:
            setattr(seller, key, value)
    storage.save()
    return make_response(jsonify(modify_seller_output(seller)), 200)


@seller_views.route("/sellers", strict_slashes=False)
def create_or_view_sellers():
    """seller endpoint for creating new seller
       Args: None
       Return: jsonified dictionary representation of
               created seller
    file: seller.yml
    """

    data = storage.all(Seller)
    sellers = {"count": len(data), "sellers":
               [modify_seller_output(seller) for seller in data]}
    return jsonify(sellers)


def modify_seller_output(seller):
    """ Formats dictionary representation of each
        seller
        Args: seller (object) - seller object
        Return: dictionary represention of seller
    """
    seller_dict = seller.to_dict()
    seller_dict.pop("id")
    products = [product.id for product in seller.products]
    seller_dict.update({"products": products})
    return seller_dict
