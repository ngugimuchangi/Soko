#!/usr/bin/python3
"""Subcategory endpoint
"""
from api.product.v1.views import product_views
from flask import abort, jsonify, make_response, request, url_for
from models import storage
from models.category import Category
from models.subcategory import Subcategory


@product_views.route("/subcategories/<subcategory_id>",
                     methods=["GET", "DELETE", "PUT"],
                     strict_slashes=False)
def manage_subcategory(subcategory_id):
    """Subcategory endpoint for get, update and delete
       subcategory items
       Args: item_id (str) - subcategory item id
       Return: jsonified dictionary representation of
               subcategory object on get or update. Empty
               dictionary representation on delete
        file: subcategory.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Subcategory item search and validation
    subcategory = storage.search(subcategory, subcategory_id)
    if not subcategory:
        abort(404)

    # Get subcategory
    if request.method == 'GET':
        return jsonify(modify_subcategory_output(subcategory))

    # Delete subcategory
    if request.method == 'DELETE':
        storage.delete(subcategory)
        return jsonify({})

    # Update subcategory
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    for key, value in data.items():
        if hasattr(subcategory, key) and key not in attr_ignore:
            setattr(subcategory, key, value)
    storage.save()
    return jsonify(modify_subcategory_output(subcategory))


@product_views.route("/categories/<category_id>/subcategories/",
                     methods=["GET", "POST"],
                     strict_slashes=False)
def create_or_view_subcategories(category_id):
    """subcategory endpoint for getting all subcategory items for a
       specified user and adding a new item to their
       subcategory
       Args: category_id (str) - category's id
       Return: jsonified dictionary with a list of all subcategory
               items belonging to specified user
       file: subcategory.yml
    """
    # category search and validation
    category = storage.search(Category, category_id)
    if not category:
        abort(404)

    # Get all subcategory items
    if request.method == "GET":
        # Get all subcategory items
        subcategory_items = category.subcategories
        subcategory_items = {"count": len(subcategory_items),
                             "subcategory items":
                             [modify_subcategory_output(item)
                              for item in subcategory_items]}
        return jsonify(subcategory_items)

    # Create new subcategory item
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(Subcategory, key)}
    try:
        new_subcategory = Subcategory(**kwargs)
    except Exception:
        abort(400)
    new_subcategory.save()
    return make_response(jsonify(
        modify_subcategory_output(new_subcategory)), 201)


def modify_subcategory_output(subcategory):
    """ Formats dictionary representation of each
        subcategory
        Args: subcategory (object) - subcategory object
        Return: dictionary represention of subcategory
    """
    subcategory_dict = subcategory.to_dict()
    products = [url_for("product_views.manage_product", product_id=product.id)
                for product in subcategory.products]
    subcategory_dict.update({"products": products})
    return subcategory_dict
