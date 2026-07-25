import pygame
from constants import SQUARE_SIZE, HIGHLIGHT_COLOR
from engine.board import Board
from engine.move import Move

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.turn = "w"
        self.selected_pos = None
        self.valid_moves = self.board.get_valid_moves(self.turn)
        self.game_over = False

    def update(self):
        self.board.draw(self.screen)
        self.draw_highlight()
        pygame.display.update()

    def draw_highlight(self):
        # Highlight selected square
        if self.selected_pos:
            r, c = self.selected_pos
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(HIGHLIGHT_COLOR)
            self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            
            # Highlight valid moves for selected piece
            for move in self.valid_moves:
                if move.start_row == r and move.start_col == c:
                    pygame.draw.circle(
                        self.screen, 
                        HIGHLIGHT_COLOR, 
                        (move.end_col * SQUARE_SIZE + SQUARE_SIZE // 2, move.end_row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                        SQUARE_SIZE // 6
                    )

    def handle_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        
        if self.selected_pos:
            if (row, col) == self.selected_pos:
                self.selected_pos = None
            else:
                start_row, start_col = self.selected_pos
                # Find if move is valid
                move_attempt = Move((start_row, start_col), (row, col), self.board)
                
                # Check for pawn promotion (UI will eventually handle this)
                if move_attempt.piece_moved and move_attempt.piece_moved.name == "p":
                    if (move_attempt.piece_moved.color == "w" and row == 0) or \
                       (move_attempt.piece_moved.color == "b" and row == 7):
                        move_attempt.is_pawn_promotion = True

                made_move = False
                for valid_move in self.valid_moves:
                    # Need to check equality and copy over special flags 
                    # because move_attempt won't have en_passant or castle flags set correctly by itself
                    if move_attempt == valid_move:
                        self.board.make_move(valid_move)
                        made_move = True
                        break

                if made_move:
                    self.change_turn()
                    self.selected_pos = None
                else:
                    # Select new piece if it's our color
                    piece = self.board.get_piece(row, col)
                    if piece and piece.color == self.turn:
                        self.selected_pos = (row, col)
                    else:
                        self.selected_pos = None
        else:
            # Try to select a piece
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.turn:
                self.selected_pos = (row, col)

    def change_turn(self):
        self.turn = "b" if self.turn == "w" else "w"
        self.valid_moves = self.board.get_valid_moves(self.turn)
        
        if len(self.valid_moves) == 0:
            self.game_over = True
            if self.board.in_check(self.turn):
                print(f"Checkmate! {'Black' if self.turn == 'w' else 'White'} wins!")
            else:
                print("Stalemate! It's a draw.")
