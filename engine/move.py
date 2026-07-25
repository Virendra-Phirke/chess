class Move:
    def __init__(self, start_pos, end_pos, board):
        self.start_row, self.start_col = start_pos
        self.end_row, self.end_col = end_pos
        self.piece_moved = board.grid[self.start_row][self.start_col]
        self.piece_captured = board.grid[self.end_row][self.end_col]
        
        # Flags for special moves
        self.is_pawn_promotion = False
        self.is_en_passant_move = False
        self.is_castle_move = False

        # If pawn promotion
        if self.piece_moved and self.piece_moved.name == "p":
            if (self.piece_moved.color == "w" and self.end_row == 0) or \
               (self.piece_moved.color == "b" and self.end_row == 7):
                self.is_pawn_promotion = True

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        if self.is_castle_move:
            return 'O-O' if self.end_col == 6 else 'O-O-O'
        piece = self.piece_moved.name.upper() if self.piece_moved.name != 'p' else ''
        end_square = self.get_rank_file(self.end_row, self.end_col)
        capture = 'x' if self.piece_captured or self.is_en_passant_move else ''
        if self.piece_moved.name == 'p' and capture:
            piece = self.get_rank_file(self.start_row, self.start_col)[0]
        promotion = '=Q' if self.is_pawn_promotion else ''
        return f'{piece}{capture}{end_square}{promotion}'

    def get_rank_file(self, r, c):
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
        return files[c] + ranks[r]

