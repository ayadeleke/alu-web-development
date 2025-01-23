#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON
    """
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200


class SessionAuth:
    """Session-based authentication class"""

    def __init__(self):
        """Initialize session authentication"""
        pass

    def get_user_id_from_session(self, request):
        """Get user ID from session cookie"""
        if request is None:
            return None
        session_cookie = request.cookies.get('session_id')
        if session_cookie is None:
            return None
        # Add logic to fetch user ID using session_cookie, e.g., from a session store
        # For now, let's assume session_cookie itself is the user_id.
        return session_cookie

    def current_user(self, request=None):
        """Returns the current user based on the session cookie"""
        user_id = self.get_user_id_from_session(request)
        if user_id:
            return User.get(user_id)  # Assuming you have a method to fetch user by ID
        return None
