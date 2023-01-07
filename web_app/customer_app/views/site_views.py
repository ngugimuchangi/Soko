#!/usr/bin/python3
from flask import redirect, render_template, request, url_for
from models import storage
from uuid import uuid4
from web_app.customer_app.views import customer_views


@customer_views.route("/")
def home():
    """ Soko home route. Accessible without login
        Args: none
        Return: home page
    """
    return render_template("index.html", title="Home", cache_id=uuid4().hex)


@customer_views.route("/about", strict_slashes=False)
def about():
    """ About route
        Args: none
        Return: About page
    """
    return render_template("about.html", title="About", cache_id=uuid4().hex)


@customer_views.route("/contacts", strict_slashes=False)
def contacts():
    """ About route
        Args: none
        Return: Contacts page
    """
    return render_template("contact.html", title="Contacts", cache_id=uuid4().hex)


@customer_views.route("/faq", strict_slashes=False)
def faq():
    """ About route
        Args: none
        Return: FAQ page
    """
    return render_template("faq.html", title="FAQ", cache_id=uuid4().hex)


@customer_views.route("/product/<product_name>", strict_slashes=False)
def view_product(product_name):
    """ Product view route
        Args: product_name(str): name of the product
        Return: product information page
    """
    return render_template("view_product.html", title=product_name, cache_id=uuid4().hex)


@customer_views.route("/search", strict_slashes=False)
def search_products():
    """ Product search route
        Args: none
        Return: page with items that match search criteria
    """
    return render_template("product_search.html", title="Search",cache_id=uuid4().hex)


@customer_views.route("/<subcategory_name>", strict_slashes=False)
def get_products_by_category(subcategory_name):
    """ Route for getting all products belonging
        to a selected category
        Args: category_name(str): product subcategory name 
    """
    return render_template("product_by_categories.html", title=subcategory_name,cache_id=uuid4().hex)


@customer_views.route("/checkout", strict_slashes=False)
def checkout():
    """ Checkout route
        Args: none
        Return: checkout page
    """
    return render_template("product_by_categories.html", title="Checkout",cache_id=uuid4().hex)
