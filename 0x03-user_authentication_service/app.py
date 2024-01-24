#!/usr/bin/env python3
"""sets up a basic flask app"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def welcome():
    """simple flask app route that returns
    a jsonified message"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
