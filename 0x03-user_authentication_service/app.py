#!/usr/bin/env python3
"""sets up a basic flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """simple flask app route that returns
    a jsonified message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """makes new users"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            abort(400)
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Handles login request"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            abort(400)
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    except Exception as e:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """finds the user using the session_id cookie and
    destroys the session_id"""
    try:
        session_id = request.cookies.get('session_id')
        if not session_id:
            abort(403)
        user = AUTH.get_user_from_session_id(session_id=session_id)
        if not user:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception as e:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """use the session_id to find user and return a
    jsonfied response else return a 403 http status"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        if not user:
            abort(403)
        return jsonify({"email": user.email}), 200
    except Exception as e:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """finds user generates token and returns a
    jsonified repsonse containing email and reset_token"""
    try:
        email = request.form.get("email")
        reset_token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception as e:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update the users password based on the reset token"""
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        password = request.form.get("new_password")
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
