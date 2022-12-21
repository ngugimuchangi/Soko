#!/usr/bin/python3
"""Saved items endpoint module
"""
from api.customer.v1.views import user_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.customer import Customer
from models.saved_item import SavedItem


@user_views.route("/saved/<item_id>",
                  methods=["GET", "DELETE"],
                  strict_slashes=False)
def manage_saved_items(item_id):
    """Saved items endpoint for get and delete
       saved items
       Args: item_id (str) - saved item id
       Return: jsonified dictionary representation of
               saved object on get or update. Empty
               dictionary representation on delete
        file: saved_items.yml
    """
    # Saved item search and validation
    saved_item = storage.search(SavedItem, item_id)
    if not saved_item:
        abort(404)

    # Get saved item
    if request.method == 'GET':
        return jsonify(modify_saved_item_output(saved_item))

    # Delete saved item
    storage.delete(saved_item)
    return jsonify({})


@user_views.route("/customers/<customer_id>/saved", methods=["GET", "POST"],
                  strict_slashes=False)
def create_and_view_saved_items(customer_id):
    """Saved items endpoint for getting all saved items for a
       specified user and adding a new item to their
       wish list
       Args: customer_id (str) - customer's id
       Return: jsonified dictionary with a list of all saved
               items belonging to specified user
       file: saved_items.yml
    """
    # Customer search and validation
    customer = storage.search(Customer, customer_id)
    if not customer:
        abort(404)

    # Get all saved items
    if request.method == "GET":
        saved_items = customer.saved_items
        saved_items = {"count": len(saved_items), "saved items":
                       [modify_saved_item_output(item)
                        for item in saved_items]}
        return jsonify(saved_items)

    # Create new saved item
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(SavedItem, key)}
    try:
        new_saved_item = SavedItem(**kwargs)
    except Exception:
        abort(400)
    new_saved_item.save()
    return make_response(jsonify(modify_saved_item_output(
                         new_saved_item)), 201)


def modify_saved_item_output(item):
    """ Formats dictionary representation of each
        saved item
        Args: item (object) - saved item object
        Return: dictionary represention of saved item
    """
    item_dict = item.to_dict()
    item_dict.pop("customer_id")
    return item_dict
