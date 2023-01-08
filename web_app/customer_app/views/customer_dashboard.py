#!/usr/bin/python3
from flask import abort, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from models import storage
from uuid import uuid4
from web_app.customer_app.views import customer_views

@customer_views.route("/dashboard/<section>", methods=["GET", "POST", "DELETE"])
@login_required
def customer_dashboard(section):
    """ Customer dashboard route
        Args: none
        Return: Customer dashboard
    """
    if section not in ['saved-items', 'profile', 'orders',
                       'pending-reviews', 'messages',
                       'notifications', 'settings']:
        abort(404)
    return render_template("dashboard.html", title="Customer Dashboard",
                           cache_id=uuid4().hex, section=section)
                