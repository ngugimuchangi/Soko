#!/usr/bin/python3
"""Products endpoint module
"""
from api.product.v1.views import product_views
from flask import (abort, jsonify, make_response,
                   request, url_for)
from models import storage
from models.product import Product
from models.subcategory import Subcategory
from models.product_image import ProductImage
from os import getenv, makedirs, remove, path
from werkzeug.utils import secure_filename


@product_views.route("/products/<product_id>",
                     methods=["GET", "DELETE", "PUT"],
                     strict_slashes=False)
def manage_product(product_id):
    """Product endpoint for get, update and delete
       products
       Args: product_id (str) - product's id
       Return: jsonified dictionary representation of
               product object on get or update. Empty
               dictionary representation on delete
        file: product.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]
    product_files_directory = getenv("PRODUCT_IMAGES")

    # Product search and validation
    product = storage.search(Product, product_id)
    if not product:
        abort(404)

    # Get product
    if request.method == 'GET':
        return jsonify(modify_product_output(product))

    # Delete product
    if request.method == 'DELETE':
        images = product.images
        for image in images:
            if path.exists(image.file_path) and image.status != "default":
                remove(image.file_path)
        storage.delete(product)
        return jsonify({})

    # Update product
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    for key, value in data:
        if hasattr(product, key) and key not in attr_ignore:
            setattr(product, key, value)
    storage.save()
    return jsonify(modify_product_output(product))


@product_views.route("/subcategories/<subcategory_id>/products",
                     methods=["GET", "POST"],
                     strict_slashes=False)
def create_or_view_products(subcategory_id):
    """Product endpoint for getting all product s for a
       specified user and adding a new  to their
       product
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all product
               s belonging to specified user
       file: product.yml
    """
    # Subcategory search and validation
    subcategory = storage.search(Subcategory, subcategory_id)
    if not subcategory:
        abort(404)

    # Get all products
    if request.method == "GET":
        # Get all products
        products = subcategory.products
        products = {"count": len(products), "products":
                    [modify_product_output(product)
                    for product in products]}
        return jsonify(products)

    # Create new product
    data = request.form
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(Product, key)}
    kwargs.update({"subcategory_id": subcategory_id,
                  "seller_id": request.cookies.get('seller_id')})
    try:
        new_product = Product(**kwargs)
    except Exception:
        abort(400)
    new_product.save()

    # Save files
    product_files_directory = getenv("PRODUCT_IMAGES")
    product_directory = path.join(product_files_directory,
                                  new_product.id)
    makedirs(product_directory)

    files = request.files
    for file in files.items():
        file_path = path.join(product_directory,
                              secure_filename(file.filename))
        file.save(file_path)
        new_image = ProductImage(**{"product_id": new_product.id,
                                 "file_path": file_path})
        new_image.save()

    return make_response(jsonify(modify_product_output(new_product)), 201)


def modify_product_output(product):
    """ Formats dictionary representation of each
        product
        Args: product (object) - product object
        Return: dictionary represention of product
    """
    host_domain = getenv("HOST_DOMAIN")
    product_dict = product.to_dict()
    shop_status = product.seller.shop_status
    reviews = ["{}{}".format(host_domain,
               url_for("product_views.get_reviews",
                       review_id=review.id))
               for review in product.reviews]
    images = [image.file_path for image in product.images]
    url = "{}{}".format(host_domain, url_for(
                        "product_views.manage_product"))
    product_dict.upadate({"images": images, "reviews": reviews,
                          "shop_status": shop_status,
                          "url": url})
    return product_dict
