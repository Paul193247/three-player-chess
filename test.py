import json

board = json.load(open("board.json"))

with open("board.json", "w") as file:
  json.dump(board, file)