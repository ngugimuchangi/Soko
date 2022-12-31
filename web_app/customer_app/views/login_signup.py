#!/usr/bin/python3
from hashlib import sha256
from flask import redirect, render_template, request, url_for
from models import storage
from models.customer import Customer
from uuid import uuid4
from web_app.customer_app.views import customer_views


@customer_views.route("/login", methods=["GET", "POST"])
def login():
    """ Customer log in page
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        customer = storage.session.query(Customer).filter_by(email=email).first()
        if not customer:
            return render_template("login.html", title="Login", cache_id=uuid4().hex)
        password = sha256("{}{}".format(password, customer.salt).encode("utf-8")).hexdigest()
        if password == customer.password:
            return redirect(url_for("customer_views.home"))
        return render_template("login.html", title="Login", cache_id=uuid4().hex)
    return render_template("login.html", title="Login", cache_id=uuid4().hex)


@customer_views.route("/signup", methods=["GET", "POST"])
def signup():
    """ Customer sign up page
    """
    if request.method == "GET":
        return render_template("signup.html",
                               cache_id=uuid4().hex)
    new_customer = Customer(**request.form)
    new_customer.save()
    return redirect(url_for("customer_views.login"))


@customer_views.route("/reset", methods=["GET", "POST"])
def reset():
    """ Customer reset page
    """
    if request.method == "GET":
        return render_template("reset.html",
                               cache_id=uuid4().hex)
    return redirect(url_for("customer_views.login"))