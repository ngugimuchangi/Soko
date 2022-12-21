#!/usr/bin/python3
"""customer notifications endpoint module
"""
from api.notification.v1.views import notification_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.customer import Customer
from models.customer_notification import CustomerNotification


@notification_views.route("/customer_notifications/<notification_id>",
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
    notification = storage.search(CustomerNotification, notification_id)
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


@notification_views.route("/customers/<customer_id>/notifications",
                          methods=["GET", "POST"],
                          strict_slashes=False)
def create_and_view_payment_notifications(customer_id):
    """Notifications endpoint for getting all notifications for a
       specified user and adding a new notification
       Args: customer_id (str) - customer's id
       Return: jsonified dictionary with a list of all notification
               belonging to specified user
       file: customer_notifications.yml
    """
    # Customer search and validation
    customer = storage.search(Customer, customer_id)
    if not customer:
        abort(404)

    # Get all notifications
    if request.method == "GET":
        notifications = customer.notifications
        notifications = {"count": len(notifications), "notifications":
                         [modify_notification_output(notification)
                          for notification in notifications]}
        return jsonify(notifications)

    # Create new notification
    data = request.get_json()
    if not data or type(data) is not dict:
        abort(400)

    kwargs = {key: value for key, value in data.items()
              if hasattr(CustomerNotification, key)}
    try:
        new_notification = CustomerNotification(**kwargs)
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
    notification_dict.pop("customer_id")
    return notification_dict
