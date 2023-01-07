#!/usr/bin/python3
from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from models import storage
from uuid import uuid4
from web_app.customer_app.views import customer_views

@customer_views.route("/dashboard", methods=["GET", "POST", "DELETE"])
@login_required
def customer_dashboard():
    """ Customer dashboard route
        Args: none
        Return: Customer dashboard
    """
    return render_template("dashboard.html", title="Customer Dashboard",
                           cache_id=uuid4().hex)
                