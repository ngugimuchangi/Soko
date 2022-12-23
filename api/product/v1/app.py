#!/usr/bin/python3
"""Products RESTful API v.1
"""
from api.product.v1.views import product_views
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv

load_dotenv()


app = Flask(__name__)
app.register_blueprint(product_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"]
CORS(app, resources={r"/api/*": {"origins": getenv("ORIGINS")}})
Swagger(app)


@app.errorhandler(404)
def not_found(error):
    """Object not found
    """
    search_response = {"error": "Not found"}
    return make_response(jsonify(search_response), 404)


@app.errorhandler(400)
def invalid_format(error):
    """Invalid format provided
    """
    validation_response = {"error": "Invalid format"}
    return make_response(jsonify(validation_response), 400)


@app.teardown_appcontext
def teardown(error):
    """Close database session
       when the app closes
    """
    storage.close()


if __name__ == "__main__":
    port = getenv("PRODUCT_API_PORT")
    host = getenv("PRODUCT_API_HOST")
    app.run(host=host, port=port, threaded=True)
