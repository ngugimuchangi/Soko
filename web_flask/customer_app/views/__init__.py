#!/usr/bin/python3
from flask import Blueprint

customer_views = Blueprint("customer_views", __name__)
from web_flask.customer_app.views import customer_dashboard, login_signup, site_views