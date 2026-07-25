import pygame
from constants import SQUARE_SIZE, HIGHLIGHT_COLOR, BOARD_WIDTH, PANEL_WIDTH, HEIGHT, LIGHT_SQUARE, DARK_SQUARE, FPS
from engine.board import Board
from engine.move import Move
from engine.timer import ChessTimer
from engine.save_manager import save_game, load_game
from engine.ai import find_best_move

class Game:
    def __init__(self, screen, online_mode=False, player_color="w", network=None, ai_mode=False):
        self.screen = screen
        self.board = Board()
        self.turn = "w"
        self.selected_pos = None
        self.valid_moves = self.board.get_valid_moves(self.turn)
        self.game_over = False
        
        self.online_mode = online_mode
        self.player_color = player_color
        self.network = network
        
        self.ai_mode = ai_mode
        self.ai_color = "b" # Assume AI is black for now
        
        # Undo / Redo
        self.undone_moves = []
        
        # Timers (e.g. 10 minutes = 600 seconds)
        self.white_timer = ChessTimer(600)
        self.black_timer = ChessTimer(600)
        self.white_timer.start() # White starts

        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont("Consolas", 18)
        self.large_font = pygame.font.SysFont("Consolas", 32, bold=True)

    def update(self):
        # Network receive
        if self.online_mode and self.turn != self.player_color:
            data = self.network.receive()
            if data:
                if data.startswith("move:"):
                    move_id = int(data.split(":")[1])
                    for valid_move in self.valid_moves:
                        if valid_move.move_id == move_id:
                            self.board.make_move(valid_move)
                            self.animate_move(valid_move)
                            self.undone_moves.clear()
                            self.change_turn()
                            break

        # Update active timer
        if not self.game_over:
            if self.turn == "w":
                self.white_timer.update()
                if self.white_timer.is_flagged():
                    self.game_over = True
                    print("Black wins on time!")
            else:
                self.black_timer.update()
                if self.black_timer.is_flagged():
                    self.game_over = True
                    print("White wins on time!")

        self.board.draw(self.screen)
        self.draw_highlight()
        self.draw_panel()
        pygame.display.update()
        
        # AI Logic
        if self.ai_mode and self.turn == self.ai_color and not self.game_over:
            ai_move = find_best_move(self.board, self.valid_moves, self.turn)
            if ai_move:
                self.board.make_move(ai_move)
                self.animate_move(ai_move)
                self.undone_moves.clear()
                self.change_turn()

    def draw_panel(self):
        panel_rect = pygame.Rect(BOARD_WIDTH, 0, PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, (48, 46, 43), panel_rect)
        
        # Draw Timers
        wt_text = self.large_font.render(self.white_timer.get_time_string(), True, (255, 255, 255))
        bt_text = self.large_font.render(self.black_timer.get_time_string(), True, (255, 255, 255))
        
        # Black timer at top
        self.screen.blit(bt_text, (BOARD_WIDTH + 20, 20))
        # White timer at bottom
        self.screen.blit(wt_text, (BOARD_WIDTH + 20, HEIGHT - 60))
        
        # Draw Move History
        history_text = self.font.render("Move History", True, (200, 200, 200))
        self.screen.blit(history_text, (BOARD_WIDTH + 20, 80))
        
        y_offset = 120
        move_texts = []
        for i in range(0, len(self.board.move_log), 2):
            move_num = i // 2 + 1
            w_move = self.board.move_log[i].get_chess_notation()
            b_move = self.board.move_log[i+1].get_chess_notation() if i+1 < len(self.board.move_log) else ""
            move_texts.append(f"{move_num}. {w_move: <7} {b_move}")
            
        # Display only last 20 moves to avoid overflow
        for text in move_texts[-25:]:
            rendered = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(rendered, (BOARD_WIDTH + 20, y_offset))
            y_offset += 24

    def animate_move(self, move):
        dR = move.end_row - move.start_row
        dC = move.end_col - move.start_col
        frames_per_square = 3
        frame_count = max(abs(dR), abs(dC)) * frames_per_square
        if frame_count == 0:
            return
            
        clock = pygame.time.Clock()
        for frame in range(frame_count + 1):
            self.board.draw(self.screen)
            
            # Hide the piece at destination
            color = LIGHT_SQUARE if (move.end_row + move.end_col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(self.screen, color, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Redraw captured piece
            if move.piece_captured:
                move.piece_captured.draw(self.screen, move.end_col, move.end_row)
                
            # Draw moving piece
            r = move.start_row + dR * (frame / frame_count)
            c = move.start_col + dC * (frame / frame_count)
            if move.piece_moved and move.piece_moved.image:
                self.screen.blit(move.piece_moved.image, (c * SQUARE_SIZE, r * SQUARE_SIZE))

            # Keep start square highlighted
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(HIGHLIGHT_COLOR)
            self.screen.blit(s, (move.start_col * SQUARE_SIZE, move.start_row * SQUARE_SIZE))

            self.draw_panel()
            pygame.display.update()
            clock.tick(FPS * 2)

    def draw_highlight(self):
        if self.selected_pos:
            r, c = self.selected_pos
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(HIGHLIGHT_COLOR)
            self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            
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

        if self.online_mode and self.turn != self.player_color:
            return # Not your turn!
            
        if self.ai_mode and self.turn == self.ai_color:
            return # AI's turn

        x, y = pos
        if x > BOARD_WIDTH:
            return # Clicked in panel

        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        
        if self.selected_pos:
            if (row, col) == self.selected_pos:
                self.selected_pos = None
            else:
                start_row, start_col = self.selected_pos
                move_attempt = Move((start_row, start_col), (row, col), self.board)
                
                if move_attempt.piece_moved and move_attempt.piece_moved.name == "p":
                    if (move_attempt.piece_moved.color == "w" and row == 0) or \
                       (move_attempt.piece_moved.color == "b" and row == 7):
                        move_attempt.is_pawn_promotion = True

                made_move = False
                for valid_move in self.valid_moves:
                    if move_attempt == valid_move:
                        self.board.make_move(valid_move)
                        self.animate_move(valid_move)
                        self.undone_moves.clear()
                        made_move = True
                        
                        if self.online_mode:
                            self.network.send(f"move:{valid_move.move_id}")
                        break

                if made_move:
                    self.change_turn()
                    self.selected_pos = None
                else:
                    piece = self.board.get_piece(row, col)
                    if piece and piece.color == self.turn:
                        self.selected_pos = (row, col)
                    else:
                        self.selected_pos = None
        else:
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.turn:
                self.selected_pos = (row, col)

    def handle_keydown(self, key):
        if self.online_mode:
            return # Disable undo/redo in online play to prevent desync
            
        if key == pygame.K_z or key == pygame.K_LEFT:
            self.undo()
        elif key == pygame.K_r or key == pygame.K_RIGHT:
            self.redo()
        elif key == pygame.K_s:
            save_game(self.board.move_log)
            print("Game Saved!")
        elif key == pygame.K_l:
            move_ids = load_game()
            if move_ids is not None:
                self.load_from_ids(move_ids)
                print("Game Loaded!")

    def undo(self):
        if len(self.board.move_log) > 0:
            move = self.board.move_log[-1]
            self.board.undo_move()
            self.undone_moves.append(move)
            self.change_turn()
            self.selected_pos = None

    def redo(self):
        if len(self.undone_moves) > 0:
            move = self.undone_moves.pop()
            self.board.make_move(move)
            self.animate_move(move)
            self.change_turn()
            self.selected_pos = None

    def load_from_ids(self, move_ids):
        self.board = Board()
        self.turn = "w"
        self.game_over = False
        self.undone_moves.clear()
        
        for move_id in move_ids:
            self.valid_moves = self.board.get_valid_moves(self.turn)
            for valid_move in self.valid_moves:
                if valid_move.move_id == move_id:
                    self.board.make_move(valid_move)
                    self.turn = "b" if self.turn == "w" else "w"
                    break
                    
        self.valid_moves = self.board.get_valid_moves(self.turn)

    def change_turn(self):
        if self.turn == "w":
            self.white_timer.stop()
            self.turn = "b"
            if not self.game_over:
                self.black_timer.start()
        else:
            self.black_timer.stop()
            self.turn = "w"
            if not self.game_over:
                self.white_timer.start()

        self.valid_moves = self.board.get_valid_moves(self.turn)
        
        if len(self.valid_moves) == 0:
            self.game_over = True
            if self.board.in_check(self.turn):
                print(f"Checkmate! {'Black' if self.turn == 'w' else 'White'} wins!")
            else:
                print("Stalemate! It's a draw.")
