#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """Home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create user function"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Login function"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["GET"], strict_slashes=False)
def get_session_user():
    """Retrieve user from session ID"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(401)
    return jsonify({"email": user.email})


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    response = make_response(redirect("/"))
    response.delete_cookie("session_id")
    return response


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Retrieve user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Generate a reset password token"""
    email = request.form.get("email")
    if not email or not AUTH.is_registered_email(email):
        abort(403)

    reset_token = AUTH.generate_reset_token(email)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Update user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if not email or not reset_token or not new_password:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
