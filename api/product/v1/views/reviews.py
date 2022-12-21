#!/usr/bin/python3
"""Product endpoint module
"""
from api.product.v1.views import product_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.product import Product
from models.review import Review


@product_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """Review endpoint for get a review by its id
       Args: review_id (str) - review's id
       Return: jsonified dictionary representation of
               product object on get or update. Empty
               dictionary representation on delete
        file: review.yml
    """
    # Review search and validation
    review = storage.search(Review, review_id)
    if not review:
        abort(404)

    # Get review
    return jsonify(review.to_dict())


@product_views.route("/products/<product_id>/reviews", methods=["GET",
                     "POST"], strict_slashes=False)
def create_or_view_products(product_id):
    """Product endpoint for getting all reviews of a specific product
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all reviews
               s belonging to specified product
       file: review.yml
    """
    # Product search and validation
    product = storage.search(Product, product_id)
    if not product:
        abort(404)

    # Get all reviews
    if request.method == "GET":
        reviews = product.reviews
        reviews = {"count": len(reviews), "products": [reviews.to_dict()
                   for review in reviews]}
        return jsonify(reviews)

    # Create new review
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(Product, key)}
    try:
        new_product = Product(**kwargs)
    except Exception:
        abort(400)
    new_product.save()
    return make_response(jsonify(new_product.to_dict()), 201)
