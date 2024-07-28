from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return open("../index.html").read()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404