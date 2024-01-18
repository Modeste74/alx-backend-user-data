#!/usr/bin/env python3
"""defines flask views to handle route for
session authentification"""
from flask import abort, request, jsonify, make_response
from models.user import User
from api.v1.app import auth
from api.v1.views import app_views
from os import getenv


@app_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Handles user login and creates a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    usr_found = next((
        user for user in users if user.is_valid_password(password)), None)
    if not usr_found:
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(usr_found.id)
    session_cookie_name = getenv('SESSION_NAME')
    response = make_response(usr_found.to_json())
    response.set_cookie(session_cookie_name, session_id)
    return response

@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'], strict_slashes=False)
def session_logout():
    """deletes the user session/logout"""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
