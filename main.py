import pygame
import sys
from constants import WIDTH, HEIGHT, FPS
from engine.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess - Level 1")
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    game.handle_click(pos)
                    
            if event.type == pygame.KEYDOWN:
                game.handle_keydown(event.key)

        game.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
