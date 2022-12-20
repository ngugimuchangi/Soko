""" Init file for api views
"""
from flask import Blueprint

seller_views = Blueprint("seller_views", __name__, url_prefix="/api/v1")
