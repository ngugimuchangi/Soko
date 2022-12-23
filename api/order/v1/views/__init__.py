""" Init file for api views
"""
from flask import Blueprint

order_views = Blueprint("views", __name__, url_prefix="/api/v1")
from api.order.v1.views import orders
