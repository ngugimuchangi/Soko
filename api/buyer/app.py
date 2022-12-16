#!/usr/bin/python3
"""Buyer API module
"""
from api.buyer.views import app_views
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from models import storage
from os import getenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(app_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"]
cors = CORS(app, resources={r"/api/*": {"origins": getenv("ORIGINS")}})

@app.teardown_appcontext
def teardown(error):
    """Close database session
       when the app closes
    """
    storage.close()

if __name__ == "__main__":
    port = getenv("BUYER_API_PORT")
    host = getenv("BUYER_API_HOST")
    app.run(host=host, port=port)