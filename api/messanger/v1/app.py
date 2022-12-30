#!/usr/bin/python3
""" Messanger/Chat API v.1
"""
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, make_response
from flask_socketio import SocketIO
from models import storage
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("CHAT_API_SECRET_KEY")
swagger = Swagger(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_message(data):
    print(data)

@app.errorhandler(404)
def not_found(error):
    """Chat Object not found
    """
    search_response = {"error": "Not found"}
    return make_response(jsonify(search_response), 404)


@app.errorhandler(400)
def invalid_format(error):
    """Invalid format provided
    """
    validation_response = {"error": "Invalid format"}
    return make_response(jsonify(validation_response), 400)


@app.errorhandler(401)
def invalid_format(error):
    """Unauthorized operations
    """
    validation_response = {"error": "Unauthorized"}
    return make_response(jsonify(validation_response), 401)


@app.teardown_appcontext
def teardown(error):
    """Close database session
       when the app closes
    """
    storage.close()


if __name__ == "__main__":
    host = getenv("CHAT_API_HOST")
    port = getenv("CHAT_API_PORT")
    socketio.run(app, host=host, port=port, debug=True)