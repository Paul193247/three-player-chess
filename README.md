# three-player-chess

## how to use the api

base url: https://three-player-chess.vercel.app

### commands:

/version: returns the version of the api

/creategame: creates a new game, returns the key of the generated game

/newplayer (POST): adds a new player to the game, returns an array with the key of the new player at the first position and the player number at second position, expects list with following parameters:
id: str, id of the game

/validmoves (POST): returns a list of all valid moves for a given position, expects list with following parameters:
id: str, id of the game,
startpos: str, Position of the Figur being moved e.g: A1,

/initialize (POST): resets the board, expects list with following parameters:
id: str, id of the game

/getboard (POST): returns the board e.g: {"A1":"R1", "A2":"N1", ..., }, expects list with following parameters:
id: str, id of the game

/setboard (POST): moves a Figure, expects list with following parameters:  
player: int, Number of the player making the move,  
startpos: str, Position of the Figur being moved e.g: A1,  
endpos: str, position where the Figur moves to e.g: A1,
id: str, id of the game,
playerid: str, id of the player

### player numbers:

1: white  
2: brown  
3: black

### abbreviations of the figures

R: Rook  
N: Knight  
B: Bishop  
Q: Queen  
K: King  
P: Pawn

## To Do

- optional web GUI fot the API in which you can create and play games
