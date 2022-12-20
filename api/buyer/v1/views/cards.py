#!/usr/bin/python3
"""card endpoint module
"""
from api.buyer.v1.views import user_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.buyer import Buyer
from models.buyer_card import BuyerCard


@user_views.route("/card/<card_id>",
                  methods=["GET", "DELETE", "PUT"],
                  strict_slashes=False)
def manage_card(card_id):
    """card endpoint for get, update and delete
       payment
       Args: card_id (str) - payment card's id
       Return: jsonified dictionary representation of
               card object on get or update. Empty
               dictionary representation on delete
        file: card.yml
    """
    attr_ignore = ["id", "created_at", "updated_at"]

    # Payment card search and validation
    card = storage.search(BuyerCard, card_id)
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


@user_views.route("/buyer/<buyer_id>/card", methods=["GET", "POST"],
                  strict_slashes=False)
def create_and_view_payment_cards(buyer_id):
    """Card endpoint for getting all cards for a
       specified user and adding a new card under
       their profile
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all payment
               cards belonging to specified user
       file: card.yml
    """
    # Buyer search and validation
    buyer = storage.search(Buyer, buyer_id)
    if not buyer:
        abort(404)

    # Get all payment cards
    if request.method == "GET":
        cards = buyer.cards
        cards = {"count": len(cards), "card":
                 [modify_card_output(card) for card in cards]}
        return jsonify(cards)

    # Create new payment card
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(BuyerCard, key)}
    kwargs.update({"buyer_id": buyer_id})
    try:
        new_card = BuyerCard(**kwargs)
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
    card_dict.pop("buyer_id")
    card_dict.pop("cvv")
    card_number = card_number.split()[-1]
    card_dict.update({"card_number": card_number})
    return card_dict
