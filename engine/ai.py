import random
from engine.evaluation import evaluate_board

CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3
next_move = None

def find_best_move(board, valid_moves, turn):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    
    # Basic move ordering: check captures and promotions first to maximize alpha-beta pruning
    valid_moves.sort(key=lambda m: m.piece_captured is not None or m.is_pawn_promotion, reverse=True)
    
    is_white = (turn == "w")
    minimax(board, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, is_white, turn)
    
    # Fallback to a random move if minimax failed to find a move (e.g. checkmate is forced)
    if next_move is None and len(valid_moves) > 0:
        next_move = valid_moves[0]
        
    return next_move

def minimax(board, valid_moves, depth, alpha, beta, is_maximizing, turn):
    global next_move
    
    if depth == 0:
        return evaluate_board(board)
        
    if is_maximizing:
        max_eval = -CHECKMATE
        for move in valid_moves:
            board.make_move(move)
            next_turn = "b" if turn == "w" else "w"
            next_moves = board.get_valid_moves(next_turn)
            
            if len(next_moves) == 0:
                if board.in_check(next_turn):
                    eval = CHECKMATE # White made a move resulting in black having no moves and in check
                else:
                    eval = STALEMATE
            else:
                eval = minimax(board, next_moves, depth - 1, alpha, beta, False, next_turn)
                
            board.undo_move()
            
            if eval > max_eval:
                max_eval = eval
                if depth == DEPTH:
                    next_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
        
    else:
        min_eval = CHECKMATE
        for move in valid_moves:
            board.make_move(move)
            next_turn = "b" if turn == "w" else "w"
            next_moves = board.get_valid_moves(next_turn)
            
            if len(next_moves) == 0:
                if board.in_check(next_turn):
                    eval = -CHECKMATE # Black made a move resulting in white having no moves and in check
                else:
                    eval = STALEMATE
            else:
                eval = minimax(board, next_moves, depth - 1, alpha, beta, True, next_turn)
                
            board.undo_move()
            
            if eval < min_eval:
                min_eval = eval
                if depth == DEPTH:
                    next_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
