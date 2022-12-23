#!/usr/bin/python3
""" Shipping Address endpoint
"""
from api.customer.v1.views import customer_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.customer import Customer
from models.shipping_address import ShippingAddress


@customer_views.route("/addresses/<address_id>", methods=["GET",
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


@customer_views.route("/customers/<customer_id>/addresses", methods=["GET",
                      "POST"], strict_slashes=False)
def get_and_add_cart_items(customer_id):
    """Addresses endpoint for getting all cart items for a
       specified customer and adding new seller
       Args: customer_id (str) - customer's id
       Return: jsonified dictionary with a list of all cart
               items belonging to specified customer
       file: cart.yml
    """
    # Customer search and validation
    customer = storage.search(Customer, customer_id)
    if not customer:
        abort(404)

    # Get all addressess
    if request.method == "GET":
        # Get all cart items
        addresses = customer.addresses
        addresses = {"count": len(addresses), "addresses":
                     [modify_address_output(address) for address in addresses]}
        return jsonify(addresses)

    # Create address
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(ShippingAddress, key)}
    kwargs.update({"customer_id": customer_id})
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
    address_dict.pop("customer_id")
    return address_dict
