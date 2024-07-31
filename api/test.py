import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Farben und Symbole für die Figuren
figures = {
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟'
}
colors = {
    '1': 'white', '2': 'black', '3': 'red'
}

# Hilfsfunktionen für die Koordinatenkonvertierung
def position_to_coords(pos):
    col = pos[0]
    row = int(pos[1:])
    col_num = ord(col) - ord('A')
    return col_num, row

def coords_to_position(coords):
    col_num, row = coords
    col = chr(col_num + ord('A'))
    return f"{col}{row}"

# Funktion zur Visualisierung des Schachbretts
def visualize_board(board):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 13)
    
    # Zeichne das sechseckige Brett
    for i in range(12):
        for j in range(12):
            if (i + j) % 2 == 0:
                hex_color = 'tan'
            else:
                hex_color = 'brown'
            x = i + (j % 2) * 0.5
            y = j * np.sqrt(3) / 2
            hex = patches.RegularPolygon((x, y), numVertices=6, radius=0.5, orientation=np.radians(30), 
                                         edgecolor='k', facecolor=hex_color)
            ax.add_patch(hex)

    # Zeichne die Figuren
    for pos, piece in board.items():
        if piece:
            x, y = position_to_coords(pos)
            x += (y % 2) * 0.5
            y = y * np.sqrt(3) / 2
            figure_color = colors[piece[-1]]
            figure_symbol = figures[piece[0]]
            ax.text(x, y, figure_symbol, ha='center', va='center', fontsize=20, color=figure_color)
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()

# Beispiel-Board
board = {
    'A1': 'R1', 'A2': 'P1', 'A3': '', 'A4': '', 'A5': '', 'A6': '', 'A7': 'P2', 'A8': 'R2', 
    'B1': 'N1', 'B2': 'P1', 'B3': '', 'B4': '', 'B5': '', 'B6': '', 'B7': 'P2', 'B8': 'N2', 
    'C1': 'B1', 'C2': 'P1', 'C3': '', 'C4': '', 'C5': '', 'C6': '', 'C7': 'P2', 'C8': 'B2', 
    'D1': 'Q1', 'D2': 'P1', 'D3': '', 'D4': '', 'D5': '', 'D6': '', 'D7': 'P2', 'D8': 'Q2', 
    'E1': 'K1', 'E2': 'P1', 'E3': '', 'E4': '', 'E5': '', 'E6': '', 'E9': '', 'E10': '', 
    'E11': 'P3', 'E12': 'K3', 'F1': 'B1', 'F2': 'P1', 'F3': '', 'F4': '', 'F9': '', 
    'F10': '', 'F11': 'P1', 'F12': 'B3', 'G1': 'N1', 'G2': 'P1', 'G3': '', 'G4': '', 
    'G9': '', 'G10': '', 'G11': 'P3', 'G12': 'N3', 'H1': 'R1', 'H2': 'P1', 'H3': '', 
    'H4': '', 'H9': '', 'H10': '', 'H11': 'P3', 'H12': 'R3', 'I5': '', 'I6': '', 
    'I7': 'P2', 'I8': 'K2', 'I9': '', 'I10': '', 'I11': 'P2', 'I12': 'Q3', 'J5': '', 
    'J6': '', 'J7': 'P2', 'J8': 'B2', 'J9': '', 'J10': '', 'J11': 'P3', 'J12': 'B3', 
    'K5': '', 'K6': '', 'K7': 'P2', 'K8': 'N2', 'K9': '', 'K10': '', 'K11': 'P3', 
    'K12': 'N3', 'L5': '', 'L6': '', 'L7': 'P2', 'L8': 'R2', 'L9': '', 'L10': '', 
    'L11': 'P3', 'L12': 'R3'
}

visualize_board(board)
