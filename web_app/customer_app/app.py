#!/usr/bin/python3
""" Soko Customer App
"""
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from models import storage
from models.customer import Customer
from uuid import uuid4
from os import getenv
from web_app.customer_app.views import customer_views

load_dotenv()

app = Flask(__name__)
app.register_blueprint(customer_views)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config["SECRET_KEY"] = getenv("SOKO_CUSTOMER_APP_SECRET_KEY")
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = "customer_views.login"

@login_manger.user_loader
def load_user(user_id):
    """ Finds user associated with id and adds them
        to flask-login session
    """
    return storage.search(Customer, user_id)


@app.teardown_appcontext
def teardown(error):
    """Close database session
       when the app closes
    """
    storage.close()

if __name__ == "__main__":
    host = getenv("SOKO_CUSTOMER_APP_HOST")
    port = getenv("SOKO_CUSTOMER_APP_PORT")
    app.run(host=host, port=port, debug=True, threaded=True)