#!/usr/bin/python3
from flask import redirect, render_template, request, url_for
from models import storage
from uuid import uuid4
from web_app.customer_app.views import customer_views


@customer_views.route("/")
def home():
    return render_template("index.html", title="Home", cache_id=uuid4().hex)