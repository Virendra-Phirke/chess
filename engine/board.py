import pygame
from constants import ROWS, COLS, LIGHT_SQUARE, DARK_SQUARE, SQUARE_SIZE
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from engine.move import Move

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        
        # Castling rights
        self.current_castling_rights = {'wks': True, 'wqs': True, 'bks': True, 'bqs': True}
        self.castle_rights_log = [self.current_castling_rights.copy()]
        
        self.en_passant_possible = () # coordinates where en passant is possible
        
        self._setup_board()

    def _setup_board(self):
        for c in range(COLS):
            self.grid[1][c] = Pawn("b")
            self.grid[6][c] = Pawn("w")

        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c in range(COLS):
            self.grid[0][c] = placement[c]("b")
            self.grid[7][c] = placement[c]("w")

    def make_move(self, move):
        self.grid[move.start_row][move.start_col] = None
        self.grid[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)

        # Update king location
        if move.piece_moved.name == 'k':
            if move.piece_moved.color == 'w':
                self.white_king_location = (move.end_row, move.end_col)
            else:
                self.black_king_location = (move.end_row, move.end_col)

        # Pawn Promotion
        if move.is_pawn_promotion:
            self.grid[move.end_row][move.end_col] = Queen(move.piece_moved.color)

        # En Passant Move
        if move.is_en_passant_move:
            self.grid[move.start_row][move.end_col] = None # capture the pawn behind
            
        # Update En Passant variable
        if move.piece_moved.name == 'p' and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.en_passant_possible = ()
            
        # Castle Move
        if move.is_castle_move:
            if move.end_col - move.start_col == 2: # kingside
                self.grid[move.end_row][move.end_col - 1] = self.grid[move.end_row][move.end_col + 1]
                self.grid[move.end_row][move.end_col + 1] = None
            else: # queenside
                self.grid[move.end_row][move.end_col + 1] = self.grid[move.end_row][move.end_col - 2]
                self.grid[move.end_row][move.end_col - 2] = None

        self.update_castle_rights(move)
        self.castle_rights_log.append(self.current_castling_rights.copy())

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.grid[move.start_row][move.start_col] = move.piece_moved
            self.grid[move.end_row][move.end_col] = move.piece_captured

            if move.piece_moved.name == 'k':
                if move.piece_moved.color == 'w':
                    self.white_king_location = (move.start_row, move.start_col)
                else:
                    self.black_king_location = (move.start_row, move.start_col)

            # Undo En Passant
            if move.is_en_passant_move:
                self.grid[move.end_row][move.end_col] = None
                self.grid[move.start_row][move.end_col] = move.piece_captured
                self.en_passant_possible = (move.end_row, move.end_col)

            # Undo a 2 square pawn advance
            if move.piece_moved.name == 'p' and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()

            # Undo Castle Rights
            self.castle_rights_log.pop()
            self.current_castling_rights = self.castle_rights_log[-1].copy()

            # Undo Castle Move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2: # Kingside
                    self.grid[move.end_row][move.end_col + 1] = self.grid[move.end_row][move.end_col - 1]
                    self.grid[move.end_row][move.end_col - 1] = None
                else: # Queenside
                    self.grid[move.end_row][move.end_col - 2] = self.grid[move.end_row][move.end_col + 1]
                    self.grid[move.end_row][move.end_col + 1] = None

    def update_castle_rights(self, move):
        if move.piece_moved.name == 'k':
            if move.piece_moved.color == 'w':
                self.current_castling_rights['wks'] = False
                self.current_castling_rights['wqs'] = False
            else:
                self.current_castling_rights['bks'] = False
                self.current_castling_rights['bqs'] = False
        elif move.piece_moved.name == 'r':
            if move.piece_moved.color == 'w':
                if move.start_row == 7:
                    if move.start_col == 0:
                        self.current_castling_rights['wqs'] = False
                    elif move.start_col == 7:
                        self.current_castling_rights['wks'] = False
            else:
                if move.start_row == 0:
                    if move.start_col == 0:
                        self.current_castling_rights['bqs'] = False
                    elif move.start_col == 7:
                        self.current_castling_rights['bks'] = False
        
        # Also need to check if a rook is captured on its starting square
        if move.piece_captured and move.piece_captured.name == 'r':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights['wqs'] = False
                elif move.end_col == 7:
                    self.current_castling_rights['wks'] = False
            elif move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights['bqs'] = False
                elif move.end_col == 7:
                    self.current_castling_rights['bks'] = False

    def get_valid_moves(self, turn_color):
        temp_en_passant = self.en_passant_possible
        temp_castle = self.current_castling_rights.copy()

        moves = self.get_all_possible_moves(turn_color)
        
        if turn_color == 'w':
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, turn_color)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves, turn_color)

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            if self.in_check(turn_color):
                moves.remove(moves[i])
            self.undo_move()
            
        if len(moves) == 0:
            if self.in_check(turn_color):
                # Checkmate
                pass 
            else:
                # Stalemate
                pass

        self.en_passant_possible = temp_en_passant
        self.current_castling_rights = temp_castle
        return moves
        
    def change_turn(self, turn_color):
        return 'b' if turn_color == 'w' else 'w'

    def in_check(self, color):
        if color == 'w':
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1], color)
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1], color)

    def square_under_attack(self, r, c, color):
        enemy_color = 'b' if color == 'w' else 'w'
        enemy_moves = self.get_all_possible_moves(enemy_color)
        for move in enemy_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def get_all_possible_moves(self, color):
        moves = []
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.grid[r][c]
                if piece and piece.color == color:
                    piece_moves = piece.get_possible_moves(r, c, self.grid)
                    for end_r, end_c in piece_moves:
                        moves.append(Move((r, c), (end_r, end_c), self))
                        
                    if piece.name == 'p':
                        # Check En Passant
                        if self.en_passant_possible:
                            er, ec = self.en_passant_possible
                            if abs(c - ec) == 1 and (r + (-1 if color == 'w' else 1)) == er:
                                mv = Move((r, c), (er, ec), self)
                                mv.is_en_passant_move = True
                                mv.piece_captured = self.grid[er - (-1 if color == 'w' else 1)][ec]
                                moves.append(mv)
        return moves

    def get_castle_moves(self, r, c, moves, color):
        if self.square_under_attack(r, c, color):
            return
        if (color == 'w' and self.current_castling_rights['wks']) or (color == 'b' and self.current_castling_rights['bks']):
            self.get_kingside_castle_moves(r, c, moves, color)
        if (color == 'w' and self.current_castling_rights['wqs']) or (color == 'b' and self.current_castling_rights['bqs']):
            self.get_queenside_castle_moves(r, c, moves, color)

    def get_kingside_castle_moves(self, r, c, moves, color):
        if self.grid[r][c + 1] is None and self.grid[r][c + 2] is None:
            if not self.square_under_attack(r, c + 1, color) and not self.square_under_attack(r, c + 2, color):
                mv = Move((r, c), (r, c + 2), self)
                mv.is_castle_move = True
                moves.append(mv)

    def get_queenside_castle_moves(self, r, c, moves, color):
        if self.grid[r][c - 1] is None and self.grid[r][c - 2] is None and self.grid[r][c - 3] is None:
            if not self.square_under_attack(r, c - 1, color) and not self.square_under_attack(r, c - 2, color):
                mv = Move((r, c), (r, c - 2), self)
                mv.is_castle_move = True
                moves.append(mv)

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
