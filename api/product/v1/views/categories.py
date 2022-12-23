#!/usr/bin/python3
"""Category endpoint module
"""
from api.product.v1.views import product_views
from flask import abort, jsonify, make_response, request, url_for
from models import storage
from models.category import Category
from os import getenv


@product_views.route("/categories/<category_id>", methods=["GET", "PUT",
                     "DELETE"], strict_slashes=False)
def manage_category(category_id):
    """ Category endpoint to get, update, or delete a specific category
        Args: category_id (str) - cartegory's id
        Return: dictionary representation of category
        file: category.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Category search and validation
    category = storage.search(Category, category_id)
    if not category:
        abort(404)

    # Get specified category
    if request.method == "GET":
        return jsonify(modify_category_output(category))

    # Delete specified category
    if request.method == "DELETE":
        storage.delete(category)
        return jsonify({})

    # Update specified category
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    for key, value in data.items():
        if hasattr(Category, key) and key not in attr_ignore:
            setattr(category, key, value)
    storage.save()
    return jsonify(modify_category_output(category))


@product_views.route("/categories", methods=["GET", "POST"],
                     strict_slashes=False)
def create_or_view_categories():
    """ Category endpoint for getting all categories
        Args: None
        Return: jsonified dictionary with a list of categories
                dictionary representations
        file: category.yml
    """
    # Get all categories
    if request.method == "GET":
        categories = storage.search(Category)
        categories_details = []

        # Modifiy output adding urls to subcategories
        for category in categories:
            categories_details.append(modify_category_output(category))
        categories_dict = {"count": len(categories),
                           "categories": categories_details}
        return jsonify(categories_dict)

    # Add new category
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(404)

    kwargs = {key: value for key, value in data.items()
              if hasattr(Category, key)}
    try:
        new_category = Category(**kwargs)
    except Exception:
        abort(404)
    new_category.save()
    return make_response(jsonify(modify_category_output(new_category)), 201)


def modify_category_output(category):
    """ Formats dictionary representation of each
        category
        Args: category (object) - category object
        Return: dictionary represention of category
    """
    category_dict = category.to_dict()
    subcategories = ["{}{}".format(getenv("HOST_DOMAIN"),
                     url_for("product_views.manage_subcategory",
                     subcategory_id=sub_cat.id))
                     for sub_cat in category.subcategories]
    category_dict.update({"subcategories": subcategories})
    return category_dict
