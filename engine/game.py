import pygame
from constants import SQUARE_SIZE, HIGHLIGHT_COLOR
from engine.board import Board

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.turn = "w"
        self.selected_pos = None

    def update(self):
        self.board.draw(self.screen)
        self.draw_highlight()
        pygame.display.update()

    def draw_highlight(self):
        if self.selected_pos:
            r, c = self.selected_pos
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(HIGHLIGHT_COLOR)
            self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

    def handle_click(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        
        if self.selected_pos:
            # We already have a selected piece, try to move it
            start_row, start_col = self.selected_pos
            if (row, col) == self.selected_pos:
                # Deselect if clicking the same square
                self.selected_pos = None
            else:
                # Basic move without validation (Level 1)
                # To prevent moving own pieces on top of each other
                target_piece = self.board.get_piece(row, col)
                if target_piece and target_piece.color == self.turn:
                    # Select the new piece instead
                    self.selected_pos = (row, col)
                else:
                    self.board.move_piece(self.selected_pos, (row, col))
                    self.change_turn()
                    self.selected_pos = None
        else:
            # Try to select a piece
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.turn:
                self.selected_pos = (row, col)

    def change_turn(self):
        self.turn = "b" if self.turn == "w" else "w"
