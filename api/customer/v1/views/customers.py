#!/usr/bin/python3
""" customer endpoint
"""
from api.customer.v1.views import customer_views
from flask import abort, jsonify, make_response, request, url_for
from hashlib import sha256
from models import storage
from models.customer import Customer


@customer_views.route("/customers/<customer_id>",
                      methods=["GET", "PUT"],
                      strict_slashes=False)
def manage_customer(customer_id):
    """Customer endpoint for read and update ops related
       to customer details
       Args: customer_id
       Return: jsonified dictionary representation of
               customer on success
       file: customer.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Customer search and validation
    customer = storage.search(Customer, customer_id)
    if not customer:
        abort(404)

    # Get specific customer
    if request.method == "GET":
        return make_response(jsonify(modify_customer_output(customer)), 200)

    # Update customer account
    data = request.get_json()
    if not data:
        abort(400)

    # a. Updated password
    if "new_password" in data.keys():
        new_password = data.get("new_password")
        old_password = data.get("old_password")
        if not new_password or not old_password:
            abort(401)

        old_password = sha256("{}{}".format(old_password, customer.salt).
                              encode('utf-8')).hexdigest()
        if old_password != customer.password:
            abort(401)
        customer.password = sha256("{}{}".format(new_password, customer.salt).
                                   encode('utf-8')).hexdigest()
        storage.save()
        return jsonify({"status": "Success"})

    # b. Update other attributes
    for key, value in data.items():
        if hasattr(customer, key) and key not in attr_ignore:
            setattr(customer, key, value)
    storage.save()
    return jsonify(modify_customer_output(customer))


@customer_views.route("/customers", strict_slashes=False)
def get_all_customers():
    """Customer endpoint for creating new customer
       Args: None
       Return: jsonified dictionary representation of
               created customer
    file: customer.yml
    """
    customers = storage.all(Customer)
    customers = {"count": len(customers), "customers":
                 [modify_customer_output(customer)
                  for customer in customers]}
    return jsonify(customers)


def modify_customer_output(customer):
    """ Formats dictionary representation of each
        customer
        Args: customer (object) - customer object
        Return: dictionary represention of customer
    """

    customer_dict = customer.to_dict()
    customer_dict.pop("id")
    addresses = [url_for("views.manage_address", address_id=address.id)
                 for address in customer.addresses]
    cards = [url_for("views.manage_card", card_id=card.id)
             for card in customer.cards]
    customer_dict.update({"shipping addresseses": addresses, "cards": cards})
    return customer_dict
