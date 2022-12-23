""" Init file for api views
"""
from flask import Blueprint

product_views = Blueprint("product_views", __name__,
                          url_prefix="/api/v1")
from api.product.v1.views import (categories, subcategories, products,
                                  products_search, reviews)
