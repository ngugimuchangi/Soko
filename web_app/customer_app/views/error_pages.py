from flask import render_template
from uuid import uuid4
from web_app.customer_app.views import customer_views


@customer_views.app_errorhandler(404)
def not_found(error):
    """ 404 error handler
    """
    return render_template("404.html", title="Not Found",
                           cache_id=uuid4().hex), 404
