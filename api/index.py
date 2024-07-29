#curl https://three-player-chess.vercel.app/board
#curl https://three-player-chess.vercel.app/inizialize
#curl -X POST -H "Content-Type: application/json" -d '{"player": 2, "startpos": "A2", "endpos": "A3"}' https://three-player-chess.vercel.app/board

import json
from flask import Flask, jsonify, request
from vercel_kv import KV
from dotenv import load_dotenv
import logging
import random

logging.basicConfig(level=logging.DEBUG)


load_dotenv(dotenv_path='.env.development.local')

app = Flask(__name__)

def setboard(board: dict, player: int, key):
    kv = KV()
    kv.set(f"{key}:board", json.dumps(board))
    kv.set(f"{key}:player", player)

def get_valid_moves(position, board):

    def letter_to_position(letter):
        return ord(letter.upper()) - ord('A') + 1

    if position not in board.keys():
        return f"Invalid Position, given position: {position} board: {board.keys()}"

    figure = board[position]

    if figure == "":
        return f"No Figure at position {position}"
    
    row, col = position[0], int(position[1:])
    moves = []

    if figure.startswith("P"):  # Pawn logic
        next_col = 0
        if int(figure[1]) == 1:
            if col == 4 and letter_to_position(row) > 4: 
                next_col = 9
                capture_positions = [
                    (chr(ord(row) + 1) + 9),
                    (chr(ord(row) - 1) + 9)
                ]
            else:
                next_col = col + 1
                capture_positions = [
            (chr(ord(row) + 1) + str(col + 1)),
            (chr(ord(row) - 1) + str(col + 1))
        ]
            
        if int(figure[1]) == 2:
            if col == 5 and letter_to_position(row) > 4: 
                next_col = 9
                if letter_to_position(row) == 5:
                    capture_positions = [
                        (chr(ord(row) + 1) + str(col + 1)),
                        ("d9")
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + str(col + 1)),
                        (chr(ord(row) - 1) + str(col + 1))
                    ]
            elif col > 8 and letter_to_position(row) > 4:
                next_col = col + 1
                if letter_to_position(row) == 5:
                    capture_positions = [
                        (chr(ord(row) + 1) + "9"),
                        ("d9")
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + str(col - 1)),
                        (chr(ord(row) - 1) + str(col - 1))
                    ]
            else:
                next_col = col - 1
                if letter_to_position(row) == 4:
                    capture_positions = [
                        ("i" + str(col - 1)),
                        (chr(ord(row) - 1) + str(col - 1))
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + str(col - 1)),
                        (chr(ord(row) - 1) + str(col - 1))
                    ]

        if int(figure[1]) == 3:
            if col == 9 and letter_to_position(row) < 9:
                next_col = 4
                if row == "E":
                    capture_positions = [
                        ("I9"),
                        (chr(ord(row) - 1) + "9")
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + "9"),
                        (chr(ord(row) - 1) + "9")
                    ]
            elif col == 9 and letter_to_position(row) > 8:
                next_col = 5
                if row == "I":
                    capture_positions = [
                        ("D9"),
                        (chr(ord(row) + 1) + "9")
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + "9"),
                        (chr(ord(row) - 1) + "9")
                    ]
            elif col < 8 and letter_to_position(row) > 8:
                next_col = col + 1
                if row == "I":
                    capture_positions = [
                        ("D" + str(col + 1)),
                        (chr(ord(row) + 1) + str(col + 1))
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + str(col + 1)),
                        (chr(ord(row) - 1) + str(col + 1))
                    ]
            else:
                next_col = col - 1
                if row == "E" == 4:
                    capture_positions = [
                        ("i" + str(col - 1)),
                        (chr(ord(row) - 1) + str(col - 1))
                    ]
                else:
                    capture_positions = [
                        (chr(ord(row) + 1) + str(col - 1)),
                        (chr(ord(row) - 1) + str(col - 1))
                    ]
                

        forward_pos = row + str(next_col)
        if forward_pos in board.keys() and board[forward_pos] == "":
            moves.append(forward_pos)

        for pos in capture_positions:
            if pos in board and not board[pos].endswith(figure[1]) and not board[pos].endswith(""):
                moves.append(pos)

    if figure.startswith("R"):  # Rook logic
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for d in directions:
            for i in range(1, 8):
                new_row = chr(ord(row) + i * d[0])
                new_col = col + i * d[1]
                endpos = new_row + str(new_col)
                if endpos in board:
                    if board[endpos] == "":
                        moves.append(endpos)
                    elif not board[endpos].endswith(figure[1]):
                        moves.append(endpos)
                        break
                    else:
                        break
                else:
                    break

    if figure.startswith("B"):  # Bishop logic
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in directions:
            for i in range(1, 8):
                new_row = chr(ord(row) + i * d[0])
                new_col = col + i * d[1]
                endpos = new_row + str(new_col)
                if endpos in board:
                    if board[endpos] == "":
                        moves.append(endpos)
                    elif not board[endpos].endswith(figure[1]):
                        moves.append(endpos)
                        break
                    else:
                        break
                else:
                    break

    if figure.startswith("N"):  # Knight logic
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for move in knight_moves:
            new_row = chr(ord(row) + move[0])
            new_col = col + move[1]
            endpos = new_row + str(new_col)
            if endpos in board:
                if board[endpos] == "" or not board[endpos].endswith(figure[1]):
                    moves.append(endpos)

    if figure.startswith("Q"):  # Queen logic
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for d in directions:
            for i in range(1, 8):
                new_row = chr(ord(row) + i * d[0])
                new_col = col + i * d[1]
                endpos = new_row + str(new_col)
                if endpos in board:
                    if board[endpos] == "":
                        moves.append(endpos)
                    elif not board[endpos].endswith(figure[1]):
                        moves.append(endpos)
                        break
                    else:
                        break
                else:
                    break

    if figure.startswith("K"):  # King logic
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for move in king_moves:
            new_row = chr(ord(row) + move[0])
            new_col = col + move[1]
            endpos = new_row + str(new_col)
            if endpos in board:
                if board[endpos] == "" or not board[endpos].endswith(figure[1]):
                    moves.append(endpos)

    return moves




@app.route('/validmoves', methods=["POST"])
def validmoves():
    data = request.get_json()
    key = data["key"]
    position = data["startpos"]
    
    board, player = getboard(key)
    
    return jsonify(get_valid_moves(position, board))

def check_move(changes, board, curr_player):
    
    startpos = changes["startpos"]
    endpos = changes["endpos"]
    
    if(int(changes["player"])>3):
        return "Invalid Player Number"
    
    next_player = int(curr_player) + 1

    if next_player > 3:
        next_player = 1
    
    if int(changes["player"]) != next_player:
        return "Wrong player"
    
    if startpos not in board.keys():
        return "Invalid start position"
    
    if endpos not in board.keys():
        return "Invalid end position"
    
    if board[startpos] == "" :
        return "Start position is empty"

    return True


def getboard(key: str):
    kv = KV()
    board_str = kv.get(f"{key}:board")
    player = kv.get(f"{key}:player")
    
    if board_str is None:
        raise ValueError("Invalid key provided or no board data found for the given key")
    
    board = json.loads(board_str)
    
    return board, player

def initialize_board(key):

    board = {'A1': 'R1', 'A2': 'P1', 'A3': '', 'A4': '', 'A5': '', 'A6': '', 'A7': 'P2', 'A8': 'R2', 'B1': 'N1', 'B2': 'P1', 'B3': '', 'B4': '', 'B5': '', 'B6': '', 'B7': 'P2', 'B8': 'N2', 'C1': 'B1', 'C2': 'P1', 'C3': '', 'C4': '', 'C5': '', 'C6': '', 'C7': 'P2', 'C8': 'B2', 'D1': 'Q1', 'D2': 'P1', 'D3': '', 'D4': '', 'D5': '', 'D6': '', 'D7': 'P2', 'D8': 'Q2', 'E1': 'K1', 'E2': 'P1', 'E3': '', 'E4': '', 'E5': '', 'E6': '', 'E9': '', 'E10': '', 'E11': 'P3', 'E12': 'K3', 'F1': 'B1', 'F2': 'P1', 'F3': '', 'F4': '', 'F9': '', 'F10': '', 'F11': 'P1', 'F12': 'B3', 'G1': 'N1', 'G2': 'P1', 'G3': '', 'G4': '', 'G9': '', 'G10': '', 'G11': 'P3', 'G12': 'N3', 'H1': 'R1', 'H2': 'P1', 'H3': '', 'H4': '', 'H9': '', 'H10': '', 'H11': 'P3', 'H12': 'R3', 'I5': '', 'I6': '', 'I7': 'P2', 'I8': 'K2', 'I9': '', 'I10': '', 'I11': 'P2', 'I12': 'Q3', 'J5': '', 'J6': '', 'J7': 'P2', 'J8': 'B2', 'J9': '', 'J10': '', 'J11': 'P3', 'J12': 'B3', 'K5': '', 'K6': '', 'K7': 'P2', 'K8': 'N2', 'K9': '', 'K10': '', 'K11': 'P3', 'K12': 'N3', 'L5': '', 'L6': '', 'L7': 'P2', 'L8': 'R2', 'L9': '', 'L10': '', 'L11': 'P3', 'L12': 'R3'}
    setboard(board, 3, key)
    return board

@app.route('/initialize', methods=["POST"])
def initialize():
    key = request.get_json()["key"]

    board = initialize_board(key)

    return board



@app.route("/")
def index():
    return "Three Player Chess API"

@app.route("/version")
def version():
    version = "2.1.0"
    return jsonify(version)

@app.route('/getboard', methods=["POST"])
def returnboard():

    key = request.get_json()["key"]

    board , player = getboard(key)
    return [board, player]

@app.route('/setboard', methods=['POST'])
def change_board():
    changes = request.get_json()
    board, player = getboard(changes["key"])

    check = check_move(changes, json.loads(board), int(player))

    if check != True:
        return check

    board[changes["endpos"]] = board[changes["startpos"]]
    board[changes["startpos"]] = ""

    setboard(board, changes["player"], changes["key"])

    return "", 204

@app.route('/creategame')
def createGame():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    key = "".join(random.choice(chars) for _ in range(40))
    initialize_board(key)
    return key

if __name__ == '__main__':
    app.run(debug=False)
