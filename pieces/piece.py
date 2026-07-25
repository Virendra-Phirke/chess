import pygame
from constants import SQUARE_SIZE

class Piece:
    def __init__(self, color, name):
        self.color = color  # "w" or "b"
        self.name = name    # "p", "r", "n", "b", "q", "k"
        self.image = None
        self.has_moved = False
        self.load_image()

    def load_image(self):
        try:
            img = pygame.image.load(f"assets/pieces/{self.color}{self.name}.svg")
            # Scale image to fit the square
            self.image = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
        except FileNotFoundError:
            # Fallback if image not found: just draw a colored circle later or leave None
            print(f"Warning: Image not found for {self.color}{self.name}")

    def draw(self, screen, x, y):
        if self.image:
            screen.blit(self.image, (x * SQUARE_SIZE, y * SQUARE_SIZE))
        else:
            # Placeholder drawing if no image
            pygame.draw.circle(
                screen,
                (255, 255, 255) if self.color == "w" else (0, 0, 0),
                (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2),
                SQUARE_SIZE // 3
            )

    def get_valid_moves(self, board, x, y):
        """To be implemented by subclasses in Level 2."""
        return []
