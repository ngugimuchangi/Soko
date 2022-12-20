""" Init file for api views
"""
from flask import Blueprint

notification_views = Blueprint("notification_views", __name__,
                               url_prefix="/api/v1")
