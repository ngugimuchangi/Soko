""" Init file for api views
"""
from flask import Blueprint

product_views = Blueprint("product_views", __name__, url_prefix="/api/v1")
