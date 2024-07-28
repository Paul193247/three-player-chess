from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    with open("index.html") as f:
        return f.read()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404