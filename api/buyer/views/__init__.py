""" Init file for api views
"""
from flask import Blueprint

app_views = Blueprint("views", __name__, url_prefix="/api/")