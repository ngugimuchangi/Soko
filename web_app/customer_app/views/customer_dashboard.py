#!/usr/bin/python3
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from models import storage
from models.customer import Customer
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
    if section == "profile":
        return render_template("profile.html", title="Profile",
                               cache_id=uuid4().hex, section=section)
    elif section == "notifications":
        return render_template("notifications.html", title="Notifications",
                               cache_id=uuid4().hex, section=section)
    elif section == "messages":
        return render_template("messages.html", title="Messages",
                               cache_id=uuid4().hex, section=section)
    elif section == "saved-items":
        return render_template("saved-items.html", title="Saved Items",
                               cache_id=uuid4().hex, section=section)
    elif section == "orders":
        return render_template("orders.html", title="Orders",
                               cache_id=uuid4().hex, section=section)
    elif section == "pending-reviews":
        return render_template("pending-reviews.html", title="Pending Reviews",
                               cache_id=uuid4().hex, section=section)
    elif section == "settings":
        return render_template("settings.html", title="Settings",
                               cache_id=uuid4().hex, section=section)
    else:
        abort(404)

@customer_views.route("/delete")
@login_required
def delete():
    """ Delete user account
    """
    customer = storage.search(Customer, current_user.id)
    storage.delete(customer)
    logout_user()
    return redirect(url_for("customer_views.home"))