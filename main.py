#curl http://192.168.188.39:4242/board
#curl http://192.168.188.39:4242/inizialize
#curl -X POST -H "Content-Type: application/json" -d '{
#  "player": 2, "a1": "QB", "a2": "QW"
#}' http://192.168.188.39:4242/board

import json
from flask import Flask
from flask import jsonify, request
from vercel_kv import KV


app = Flask(__name__)

@app.route('/inizialize')
def inizialize_board():
    board = {
    "player": 1, 
    # Spieler 1 (rot)
    "A1": "R1", "B1": "N1", "C1": "B1", "D1": "Q1", "E1": "K1", "F1": "B1", "G1": "N1", "H1": "R1",
    "A2": "P1", "B2": "P1", "C2": "P1", "D2": "P1", "E2": "P1", "F2": "P1", "G2": "P1", "H2": "P1",
    # Spieler 2 (weiß)
    "L3": "R2", "L4": "N2", "L5": "B2", "L6": "Q2", "L7": "K2", "L8": "B2", "L9": "N2", "L10": "R2",
    "K3": "P2", "K4": "P2", "K5": "P2", "K6": "P2", "K7": "P2", "K8": "P2", "K9": "P2", "K10": "P2",
    # Spieler 3 (schwarz)
    "A11": "R3", "B11": "N3", "C11": "B3", "D11": "Q3", "E11": "K3", "F11": "B3", "G11": "N3", "H11": "R3",
    "A10": "P3", "B10": "P3", "C10": "P3", "D10": "P3", "E10": "P3", "F10": "P3", "G10": "P3", "H10": "P3",
    # Leere Felder
    "I3": "", "J3": "", "I4": "", "J4": "", "I5": "", "J5": "", "I6": "", "J6": "", 
    "I7": "", "J7": "", "I8": "", "J8": "", "I9": "", "J9": "", "I10": "", "J10": "",
    # Mittlere Felder
    "C5": "", "D5": "", "E5": "", "F5": "", "G5": "", "H5": "", "C6": "", "D6": "", 
    "E6": "", "F6": "", "G6": "", "H6": "", "C7": "", "D7": "", "E7": "", "F7": "", 
    "G7": "", "H7": "", "C8": "", "D8": "", "E8": "", "F8": "", "G8": "", "H8": "", 
    "C9": "", "D9": "", "E9": "", "F9": "", "G9": "", "H9": ""
} 
    with open("board.json", "w") as file:
        json.dump(board, file)
    return '', 204

@app.route("/")
def index():
    return open("index.html").read()

@app.route('/board')
def get_board():
    
    board = json.load(open("board.json"))

    return jsonify(board)


@app.route('/board', methods=['POST'])
def change_board():
    newboard = request.get_json()

    board = json.load(open("board.json"))

    newplayer = board["player"] + 1

    if newplayer > 3:
        newplayer = 1

    if newboard["player"] == newplayer:
        with open("board.json", "w") as file:
            json.dump(newboard, file)

    return '', 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4242, debug=True)