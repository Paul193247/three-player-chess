# /api/index.py

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return open("../index.html").read()

@app.route("/api")
def api():
    return "api"