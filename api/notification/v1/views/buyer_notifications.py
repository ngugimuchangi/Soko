#!/usr/bin/python3
"""Buyer notifications endpoint module
"""
from api.notification.v1.views import notification_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.buyer import Buyer
from models.buyer_notification import BuyerNotification


@notification_views.route("/buyernotifications/<notification_id>",
                          methods=["GET", "PUT"],
                          strict_slashes=False)
def manage_notification(notification_id):
    """Notification endpoint for get and update user
       notifications
       Args: notification_id (str) - notification id
       Return: jsonified dictionary representation of
               notification object on get or update.
        file: notifications.yml
    """
    attr_ignore = ["id", "created_at", "message", "updated_at"]

    # Notification search and validation
    notification = storage.search(BuyerNotification, notification_id)
    if not notification:
        abort(404)

    # Get notification
    if request.method == 'GET':
        return jsonify(modify_notification_output(notification))

    # Update notification status
    data = request.get_json()
    for key, value in data.items():
        if hasattr(BaseException, key) and key not in attr_ignore:
            setattr(notification, key, value)
    storage.save()
    return jsonify(modify_notification_output(notification))


@notification_views.route("/buyers/<buyer_id>/notifications",
                          methods=["GET", "POST"],
                          strict_slashes=False)
def create_and_view_payment_notifications(buyer_id):
    """Notifications endpoint for getting all notifications for a
       specified user and adding a new notification
       Args: buyer_id (str) - buyer's id
       Return: jsonified dictionary with a list of all notification
               belonging to specified user
       file: buyer_notifications.yml
    """
    # Buyer search and validation
    buyer = storage.search(Buyer, buyer_id)
    if not buyer:
        abort(404)

    # Get all notifications
    if request.method == "GET":
        notifications = buyer.notifications
        notifications = {"count": len(notifications), "notifications":
                         [modify_notification_output(notification)
                          for notification in notifications]}
        return jsonify(notifications)

    # Create new notification
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(BuyerNotification, key)}
    kwargs.update({"buyer_id": buyer_id})
    try:
        new_notification = BuyerNotification(**kwargs)
    except Exception:
        abort(400)
    new_notification.save()
    return make_response(jsonify(modify_notification_output(
                         new_notification)), 201)


def modify_notification_output(notification):
    """ Formats dictionary representation of each
        notification
        Args: notification (object) - notification object
        Return: dictionary represention of notification
    """
    notification_dict = notification.to_dict()
    notification_dict.pop("buyer_id")
    return notification_dict
