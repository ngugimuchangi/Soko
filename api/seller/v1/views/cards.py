#!/usr/bin/python3
"""Card endpoint module
"""
from api.seller.v1.views import seller_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.seller import Seller
from models.seller_card import SellerCard


@seller_views.route("/cards/<card_id>",
                    methods=["GET", "DELETE", "PUT"],
                    strict_slashes=False)
def manage_card(card_id):
    """Card endpoint for get, update and delete
       payment
       Args: card_id (str) - payment card's id
       Return: jsonified dictionary representation of
               card object on get or update. Empty
               dictionary representation on delete
        file: seller_card.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Payment card search and validation
    card = storage.search(SellerCard, card_id)
    if not card:
        abort(404)

    # Get card
    if request.method == 'GET':
        return jsonify(modify_card_output(card))

    # Delete payment card
    if request.method == 'DELETE':
        storage.delete(card)
        return jsonify({})

    # Update card
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)
    for key, value in data.items():
        if hasattr(card, key) and key not in attr_ignore:
            setattr(card, key, value)
    storage.save()
    return jsonify(modify_card_output(card))


@seller_views.route("/sellers/<seller_id>/card", methods=["GET",
                    "POST"], strict_slashes=False)
def create_and_view_payment_cards(seller_id):
    """Card endpoint for getting all cards for a
       specified user and adding a new card to their
       card
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all payment
               cards belonging to specified user
       file: seller_card.yml
    """
    # Seller search and validation
    seller = storage.search(Seller, seller_id)
    if not seller:
        abort(404)

    # Get all payment cards
    if request.method == "GET":
        card = seller.card[0]
        card = modify_card_output(card)
        return jsonify(card)

    # Create new payment card
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(SellerCard, key)}
    try:
        new_card = SellerCard(**kwargs)
    except Exception:
        abort(400)
    new_card.save()
    return make_response(jsonify(modify_card_output(new_card)), 201)


def modify_card_output(card):
    """ Formats dictionary representation of each
        payment card
        Args: card (object) - card object
        Return: dictionary represention of payment card
    """
    card_dict = card.to_dict()
    card_dict.pop("seller_id")
    card_dict.pop("cvv")
    card_number = card_number.split()[-1]
    card_dict.update({"card_number": card_number})
    return card_dict
