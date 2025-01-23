#!/usr/bin/env python3
""" Module for Session Authentication Views
"""
from flask import Blueprint, request, jsonify, abort
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Handles POST /api/v1/auth_session/login for session authentication."""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
@app_views.route('/auth_session/logout/',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """Handles DELETE /api/v1/auth_session/logout for session logout."""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)

    return jsonify({}), 200
