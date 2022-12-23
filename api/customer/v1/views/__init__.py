""" Init file for api views
"""
from flask import Blueprint
customer_views = Blueprint("customer_views", __name__, url_prefix="/api/v1")
from api.customer.v1.views import (addresses, cards, cart,
                                   customers, saved_items)
