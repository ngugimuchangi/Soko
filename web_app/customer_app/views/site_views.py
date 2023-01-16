#!/usr/bin/python3
from datetime import datetime
from flask import abort, make_response, redirect, render_template, request, url_for
from flask_login import login_required
from models import storage
from uuid import uuid4
from web_app.customer_app.views import customer_views


@customer_views.route("/", strict_slashes=True)
def home():
    """ Soko home route. Accessible without login
        Args: none
        Return: home page
    """
    print(request.path)
    return render_template("index.html", title="Home", cache_id=uuid4().hex)


@customer_views.route("/home", strict_slashes=True)
def redirect_home():
    """ Redirect to home page
        Args: none
        Return: home page
    """
    return redirect(url_for('customer_views.home'))


@customer_views.route("/about", strict_slashes=True)
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


@customer_views.route("/faq", strict_slashes=True)
def faq():
    """ About route
        Args: none
        Return: FAQ page
    """
    return render_template("faq.html", title="FAQ", cache_id=uuid4().hex)


@customer_views.route("/product/<product_name>", strict_slashes=True)
def view_product(product_name):
    """ Product view route
        Args: product_name(str): name of the product
        Return: product information page
    """
    
    response = make_response(render_template("view_product.html",
                             title=product_name, cache_id=uuid4().hex))
    expiry_date = datetime.now()
    expiry_date = expiry_date.replace(year = expiry_date.year + 1)
    response.set_cookie("uprod", product_name, expires=expiry_date)
    return response


@customer_views.route("/search", strict_slashes=False)
def search_products():
    """ Product search route
        Args: none
        Return: page with items that match search criteria
    """
    response = make_response(render_template("product_search.html",
                             title="Search",cache_id=uuid4().hex))
    if not request.args.get("q"):
        return response
    response.set_cookie("search", request.args.get("q"))
    return response


@customer_views.route("/<category_name>", strict_slashes=True)
def get_products_by_category(category_name):
    """ Route for getting all products belonging
        to a selected category
        Args: category_name(str): product subcategory name 
    """
    category = category_name.replace('-', " ").title()
    return render_template("product_by_categories.html", title=category,cache_id=uuid4().hex)

@customer_views.route("/<category_name>/<subcategory_name>", strict_slashes=True)
def get_products_by_subcategory(category_name, subcategory_name):
    """ Route for getting all products belonging
        to a selected category
        Args: category_name(str): product subcategory name 
    """
    subcategory = subcategory_name.replace('-', " ").title()
    return render_template("product_by_categories.html", title=subcategory,cache_id=uuid4().hex)

@customer_views.route("/checkout", strict_slashes=True)
def checkout():
    """ Checkout route
        Args: none
        Return: checkout page
    """
    return render_template("checkout.html", title="Checkout",
    cache_id=uuid4().hex)


@customer_views.route("/order/<order_number>", strict_slashes=True)
@login_required
def confirming_new_orders(order_number):
    """ Order confirmation route
        Args: order_number
        Return: order confirmation page
    """
    return render_template("order-confirmed.html",
                           order_number=order_number,
                           title="Order " + order_number,
                           cache_id=uuid4().hex)