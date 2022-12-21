""" Init file for api views
"""
from flask import Blueprint

customer_views = Blueprint("customer_views", __name__, url_prefix="/api/v1")
