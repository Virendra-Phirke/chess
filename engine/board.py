import pygame
from constants import ROWS, COLS, LIGHT_SQUARE, DARK_SQUARE, SQUARE_SIZE
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self._setup_board()

    def _setup_board(self):
        # Setup pawns
        for c in range(COLS):
            self.grid[1][c] = Pawn("b")
            self.grid[6][c] = Pawn("w")

        # Setup other pieces
        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c in range(COLS):
            self.grid[0][c] = placement[c]("b")
            self.grid[7][c] = placement[c]("w")

    def draw_squares(self, screen):
        screen.fill(LIGHT_SQUARE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(
                    screen, 
                    DARK_SQUARE, 
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen, col, row)

    def draw(self, screen):
        self.draw_squares(screen)
        self.draw_pieces(screen)

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.grid[row][col]
        return None

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.grid[start_row][start_col]
        if piece:
            self.grid[end_row][end_col] = piece
            self.grid[start_row][start_col] = None
            piece.has_moved = True
            return True
        return False
