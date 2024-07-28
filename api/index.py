# /api/index.py

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Flask Vercel Example - Hello World", 200

@app.route("/api")
def api():
    return "api"