#!/usr/bin/python3
"""Orders endpoints
"""
from api.order.v1.views import order_views
from flask import abort, jsonify, make_response, request, url_for
from models import storage
from models.customer import Customer
from models.order import Order
from models.order_detail import OrderDetail
from models.seller import Seller
from os import getenv


@order_views.route("/order/<order_id>",
                   methods=["GET", "PUT" "DELETE"],
                   strict_slashes=False)
def manage_order(order_id):
    """Orders endpoint for get specific orders
       Args: order_id (str) - order item id
       Return: jsonified dictionary representation of
               order object
        file: order.yml
    """
    attr_ignore = ["id", "order_id", "product_id",
                   "created_at", "updated_at"]
    # Order item search and validation
    order = storage.search(Order, order_id)
    if not order:
        abort(404)

    # Get cart item
    if request.method == "GET":
        return jsonify(modify_order_output(order))

    if request.method == "DELETE":
        if order.status == "awaiting payment":
            storage.delete(order)
            jsonify("{}")
        else:
            abort(403)

    # Update order and order details
    data = request.get_json()
    if not data:
        abort(400)
    order_status = data.get("(order_status")
    order_details = data.get("product_details")

    # a. Update order status
    if order_status:
        order.status = order_status

    # b. Update item details
    if not order_details:
        storage.save()
        return jsonify(modify_order_output(order))

    for item in order_details:
        order_item = storage.search(OrderDetail, item.get("id"))
        if not order_item:
            continue
        for key, value in item.items():
            if hasattr(OrderDetail, key) and key not in attr_ignore:
                setattr(order_item, key, value)
    storage.save()
    return jsonify(modify_order_output(order))


@order_views.route("/customers/<customer_id>/orders", strict_slashes=False)
def customer_view_orders(customer_id):
    """Order endpoint for getting all order items for a
       specified user
       Args: customer_id (str) - customer's id
       Return: jsonified dictionary with a list of all orders
               belonging to specified user
       file: orders.yml
    """
    # Customer search and validation
    customer = storage.search(Customer, customer_id)
    if not customer:
        abort(404)

    # Get all orders
    orders = storage.session.query(Order).filter_by(
        customer_id=customer.id).all()
    orders = {"count": len(orders), "orders":
              [modify_order_output(order) for order in orders]}
    return jsonify(orders)


@order_views.route("/sellers/<seller_id>/orders", strict_slashes=False)
def seller_view_orders(seller_id):
    """Order endpoint for getting all order items for a
       specified seller
       Args: customer_id (str) - customer's id
       Return: jsonified dictionary with a list of all orders
               belonging to specified seller
       file: orders.yml
    """
    # Seller search and validation
    seller = storage.search(Seller, seller_id)
    if not seller:
        abort(404)

    # Get all orders
    # Violation of abstraction to be fixed
    orders = storage.session.query(OrderDetail).filter_by(
             seller_id=seller.id).all()
    orders = {"count": len(orders), "orders":
              [order.to_dict() for order in orders]}
    return jsonify(orders)


@order_views.route("/order", method=["POST"],
                   strict_slashes=False)
def create_order():
    """Order endpoint for creating new orders
       Useful in the creation of setup orders
       by sellers from their dashboards
       Args: None
       Return: jsonified representation of new order
       file: order.yml
    """
    # Create new order item
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    if not data.get("order_details"):
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(Order, key)}
    try:
        new_order = Order(**kwargs)
    except Exception:
        abort(400)
    new_order.save()
    for order_item in data.get("order_details"):
        try:
            new_order_item = OrderDetail(**order_item)
        except Exception:
            abort(400)
        new_order_item.save()

    new_order_details = modify_order_output(new_order)
    new_order_details.update("{}{}".format(getenv("HOST_DOMAIN"),
                             {"url": url_for("order_views.manage_order",
                              order_id=new_order.id)}))
    return make_response(jsonify(new_order_details), 201)


def modify_order_output(order):
    """ Formats dictionary representation of each
        order
        Args: item (object) - order object
        Return: dictionary represention of order
    """
    order_dict = order.to_dict()
    order_items = []

    # Get order details
    for order_item in order.details:
        item_dict = order_item.to_dict()
        item_dict.pop("order_id")
        order_items.append(item_dict)

    order_dict.update({"order_details": order_items})
    return order_dict
