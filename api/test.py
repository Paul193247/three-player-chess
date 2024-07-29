board = {}

letters = "ABCDEFGHIJKL"

for letter in letters:
  for number in range(1, 12):
    if number == 2:
        board[letter + str(number)] = "P1"
    elif number == 7:
        board[letter + str(number)] = "P2"
    elif number == 11:
        board[letter + str(number)] = "P1"
    else:
       board[letter + str(number)] = ""

print(board)