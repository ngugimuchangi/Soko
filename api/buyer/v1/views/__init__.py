""" Init file for api views
"""
from flask import Blueprint

user_views = Blueprint("user_views", __name__, url_prefix="/api/v1")
