#!/usr/bin/python3
from hashlib import sha256
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from models import storage
from models.customer import Customer
from uuid import uuid4
from web_app.customer_app.views import customer_views


@customer_views.route("/login", methods=["GET", "POST"])
def login():
    """ Customer log in page
    """
    # Post request
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = True if request.form.get("remember-me") else False
        customer = storage.session.query(Customer).filter_by(email=email).first()
        # Customer doesn't exist, i.e, wrong email
        if not customer:
            flash("Please check your login details and try again")
            return render_template("login.html", title="Login", cache_id=uuid4().hex)
        password = sha256("{}{}".format(password, customer.salt).
        encode("utf-8")).hexdigest()
        # Correct email and password
        if password == customer.password:
            login_user(customer, remember=remember_me)
            return redirect(url_for("customer_views.home"))
        # Wrong password
        flash("Please check your login details and try again")
        return render_template("login.html", title="Login",
                               cache_id=uuid4().hex)
    # Get request
    return render_template("login.html", title="Login",
                           cache_id=uuid4().hex)


@customer_views.route("/signup", methods=["GET", "POST"])
def signup():
    """ Customer sign up page
    """
    if request.method == "GET":
        return render_template("signup.html",
                               cache_id=uuid4().hex)
    email = request.form.get("email", None)
    if storage.session.query(Customer).filter_by(email=email).first():
        flash("An account associated with this email already exists")
        return redirect(url_for("customer_views.signup"))
    new_customer = Customer(**request.form)
    new_customer.save()
    return redirect(url_for("customer_views.login"))


@customer_views.route("/reset", methods=["GET", "POST"])
def reset():
    """ Customer password reset page
    """
    if request.method == "GET":
        return render_template("reset.html",
                               cache_id=uuid4().hex)
    return redirect(url_for("customer_views.login"))

@customer_views.route("/logout")
@login_required
def logout():
    """ Customer logout
    """
    logout_user()
    return redirect(url_for("customer_views.home"))