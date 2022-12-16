#!/usr/bin/python3
"""Index view module"""
from api.buyer.views import app_views
from flask import jsonify


@app_views.route('/status', method='GET',
                 strict_slashes=False)
def status():
    """Returns OK for successful
        connection to Buyer API
    """
    return jsonify({"status": "OK"})