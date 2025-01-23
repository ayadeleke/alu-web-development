#!/usr/bin/env python3
"""
Route module for the API
"""
from logging import exception
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


if getenv("AUTH_TYPE") == "auth":
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()


@app.before_request
def authentication_handler() -> None:
    """Auth handler

    Returns:
        [type]: creates an instance of auth
    """
    exceptions = ['/api/v1/status/',
                  '/api/v1/unauthorized/',
                  '/api/v1/forbidden/',
                  '/api/v1/auth_session/login/']
    if not auth or not auth.require_auth(request.path, exceptions):
        return None
    if not auth.authorization_header(request)\
            and not auth.session_cookie(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized error handler

    Args:
        error ([type]): [description]

    Returns:
        str: [description]
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """user is authenticate but not allowed

    Args:
        error ([type]): error

    Returns:
        str: {"error": "Forbidden"}
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
