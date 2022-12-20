#!/usr/bin/python3
"""Cart endpoint module
"""
from api.buyer.v1.views import user_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.buyer import Buyer
from models.cart import Cart


@user_views.route("/cart/<item_id>",
                  methods=["GET", "DELETE", "PUT"],
                  strict_slashes=False)
def manage_cart(item_id):
    """Cart endpoint for get, update and delete
       cart items
       Args: item_id (str) - cart item id
       Return: jsonified dictionary representation of
               cart object on get or update. Empty
               dictionary representation on delete
        file: cart.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Cart item search and validation
    cart_item = storage.search(Cart, item_id)
    if not cart_item:
        abort(404)

    # Get cart item
    if request.method == 'GET':
        return jsonify(modify_cart_output(cart_item))

    # Delete cart item
    if request.method == 'DELETE':
        storage.delete(cart_item)
        return jsonify({})

    # Update cart item
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    for key, value in data.items():
        if hasattr(Cart, key) and key not in attr_ignore:
            setattr(cart_item, key, value)
    storage.save()
    return jsonify(modify_cart_output(cart_item))


@user_views.route("/buyer/<buyer_id>/cart", methods=["GET", "POST"],
                  strict_slashes=False)
def create_and_view_cart_items(buyer_id):
    """Cart endpoint for getting all cart items for a
       specified user and adding a new item to their
       cart
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all cart
               items belonging to specified user
       file: cart.yml
    """
    # Buyer search and validation
    buyer = storage.search(Buyer, buyer_id)
    if not buyer:
        abort(404)

    # Get all cart items
    if request.method == "GET":
        cart_items = buyer.cart
        cart_items = {"count": len(cart_items), "cart items":
                      [modify_cart_output(item) for item in cart_items]}
        return jsonify(cart_items)

    # Create new cart item
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(Cart, key)}
    kwargs.update({"buyer_id": buyer_id})
    try:
        new_cart_item = Cart(**kwargs)
    except Exception:
        abort(400)
    new_cart_item.save()
    return make_response(jsonify(modify_cart_output(new_cart_item)), 201)


def modify_cart_output(item):
    """ Formats dictionary representation of each
        cart item
        Args: item (object) - cart item object
        Return: dictionary represention of cart item
    """
    item_dict = item.to_dict()
    item_dict.pop("buyer_id")
    return item_dict
