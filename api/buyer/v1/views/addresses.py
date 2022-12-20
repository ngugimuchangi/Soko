#!/usr/bin/python3
""" Shipping Address endpoint
"""
from api.buyer.v1.views import user_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.buyer import Buyer
from models.shipping_address import ShippingAddress


@user_views.route("/addresses/<address_id>", method=["GET",
                  "PUT", "DELETE"], strict_slashes=False)
def manage_address(address_id):
    """Shipping Address endpoint for get, update and delete
       cart items
       Args: item_id (str) - cart item id
       Return: jsonified dictionary representation of
               shipping address object on get or update. Empty
               dictionary representation on delete
        file: shipping_address.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Shipping address search and validation
    shipping_address = storage.search(ShippingAddress, address_id)
    if not shipping_address:
        abort(404)

    # Get shipping address item
    if request.method == 'GET':
        return jsonify(modify_address_output(shipping_address))

    # Delete shipping address
    if request.method == 'DELETE':
        storage.delete(shipping_address)
        return jsonify({})

    # Update shipping address
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    for key, value in data.items():
        if hasattr(ShippingAddress, key) and key not in attr_ignore:
            setattr(shipping_address, key, value)
    storage.save()
    return jsonify(modify_address_output(shipping_address))


@user_views.route("/buyer/<buyer_id>/addresses", methods=["GET",
                  "POST"], strict_slashes=False)
def get_and_add_cart_items(buyer_id):
    """Addresses endpoint for getting all cart items for a
       specified user and adding new seller
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all cart
               items belonging to specified user
       file: cart.yml
    """
    # Buyer search and validation
    buyer = storage.search(Buyer, buyer_id)
    if not buyer:
        abort(404)

    # Get all addressess
    if request.method == "GET":
        # Get all cart items
        addresses = buyer.addresses
        addresses = {"count": len(addresses), "addresses":
                     [modify_address_output(address) for address in addresses]}
        return jsonify(addresses)

    # Create address
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(ShippingAddress, key)}
    kwargs.update({"buyer_id": buyer_id})
    try:
        new_address = ShippingAddress(**kwargs)
    except Exception:
        abort(400)
    new_address.save()
    return make_response(jsonify(modify_address_output(new_address)), 201)


def modify_address_output(address):
    """ Formats dictionary representation of each
        shipping address
        Args: item (object) - shipping address object
        Return: dictionary represention of shipping address
    """
    address_dict = address.to_dict()
    address_dict.pop("buyer_id")
    return address_dict
