# three-player-chess  
  
##how to use the api  
base url: https://three-player-chess.vercel.app  
  
###commands:  
/version: returns the version of the api  
  
/initialize: resets the board  
  
/board: returns the board e.g: {"A1":"R1", "A2":"N1", ..., }  
  
/board (POST): moves a Figure, expects list with following parameters:  
player: int, Number of the player making the move,  
startpos: str, Position of the Figur being moved e.g: A1,  
endpos: str, position wherw the Figur moves to e.g: A1  
  
###player numbers:  
1: white  
2: brown  
3: black  
  
###abbreviations of the figures  
R: Rook  
N: Knight  
B: Bishop  
Q: Queen  
K: King  
P: Pawn  
