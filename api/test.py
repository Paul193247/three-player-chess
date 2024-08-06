def get_valid_moves(position, board):
    def position_to_coords(pos):
        col = pos[0]
        row = int(pos[1:])
        col_num = ord(col) - ord('A')
        return col_num, row

    def coords_to_position(coords):
        col_num, row = coords
        col = chr(col_num + ord('A'))
        return f"{col}{row}"
    
    # Jetzt kannst du sicher auf den Wert zugreifen
    thirds = []

    row = []
    
    for c in range(1, 5):
        col = []
        for r in range(0, 8):
            key =coords_to_position((r, c))
            col.append(board[key])
        row.append(col)
    thirds.append(row)

    row = []
    for c in range(9, 13):
        col = []
        for r in range(4, 11):
            key =coords_to_position((r, c))
            col.append(board[key])
        row.append(col)
    thirds.append(row)
    
    #for c in range(5, 9):
    #    for r in range(0, 4):
    #        key =coords_to_position((r, c))
    #        third[key] = board[key]

    #for c in range(5, 9):
    #    for r in range(8, 12):
    #        key =coords_to_position((r, c))
    #        third[key] = board[key]
    #thirds.append(row)
    print(thirds)

    def move_piece(position, d):
        x, y = position_to_coords(position)
        new_x = x + d[0]
        new_y = y + d[1]
        return coords_to_position((new_x, new_y))
    
    return move_piece(position, (0,1))

    

print(get_valid_moves("A2", {
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
    }))