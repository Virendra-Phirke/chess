from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "p")

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "r")

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "n")

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "b")

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "q")

class King(Piece):
    def __init__(self, color):
        super().__init__(color, "k")
