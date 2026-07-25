from pieces.piece import Piece
from constants import ROWS, COLS

def get_sliding_moves(r, c, board_grid, color, directions):
    moves = []
    for d in directions:
        for i in range(1, 8):
            end_r = r + d[0] * i
            end_c = c + d[1] * i
            if 0 <= end_r < ROWS and 0 <= end_c < COLS:
                end_piece = board_grid[end_r][end_c]
                if end_piece is None:
                    moves.append((end_r, end_c))
                elif end_piece.color != color:
                    moves.append((end_r, end_c))
                    break
                else:
                    break
            else:
                break
    return moves

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "p")

    def get_possible_moves(self, r, c, board_grid):
        moves = []
        direction = -1 if self.color == "w" else 1
        start_row = 6 if self.color == "w" else 1

        # Move forward 1
        if 0 <= r + direction < ROWS and board_grid[r + direction][c] is None:
            moves.append((r + direction, c))
            # Move forward 2 (only if hasn't moved / is at start row and forward 1 is clear)
            if r == start_row and board_grid[r + 2 * direction][c] is None:
                moves.append((r + 2 * direction, c))

        # Captures
        for dc in [-1, 1]:
            if 0 <= c + dc < COLS and 0 <= r + direction < ROWS:
                target = board_grid[r + direction][c + dc]
                if target and target.color != self.color:
                    moves.append((r + direction, c + dc))
        
        # En passant moves will be handled by the board since they need move_log
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "r")
        self.directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def get_possible_moves(self, r, c, board_grid):
        return get_sliding_moves(r, c, board_grid, self.color, self.directions)

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "n")
        self.jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def get_possible_moves(self, r, c, board_grid):
        moves = []
        for j in self.jumps:
            end_r, end_c = r + j[0], c + j[1]
            if 0 <= end_r < ROWS and 0 <= end_c < COLS:
                target = board_grid[end_r][end_c]
                if not target or target.color != self.color:
                    moves.append((end_r, end_c))
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "b")
        self.directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_possible_moves(self, r, c, board_grid):
        return get_sliding_moves(r, c, board_grid, self.color, self.directions)

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "q")
        self.directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_possible_moves(self, r, c, board_grid):
        return get_sliding_moves(r, c, board_grid, self.color, self.directions)

class King(Piece):
    def __init__(self, color):
        super().__init__(color, "k")
        self.directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_possible_moves(self, r, c, board_grid):
        moves = []
        for d in self.directions:
            end_r, end_c = r + d[0], c + d[1]
            if 0 <= end_r < ROWS and 0 <= end_c < COLS:
                target = board_grid[end_r][end_c]
                if not target or target.color != self.color:
                    moves.append((end_r, end_c))
        # Castling is handled by the board since it needs complex logic
        return moves
