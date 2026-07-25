import sys
import pygame
from constants import WIDTH, HEIGHT, FPS
from engine.game import Game
from network import Network

def main():
    online = "--online" in sys.argv
    ai_mode = "--ai" in sys.argv
    network = None
    player_color = "w"

    if online:
        network = Network()
        if network.color:
            player_color = network.color
            print(f"Connected to server as {player_color}")
        else:
            print("Failed to connect to server. Falling back to local.")
            online = False

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Chess - {'Online (' + player_color + ')' if online else 'Local'}")
    clock = pygame.time.Clock()

    game = Game(screen, online_mode=online, player_color=player_color, network=network, ai_mode=ai_mode)

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    game.handle_click(pos)
                    
            if event.type == pygame.KEYDOWN:
                game.handle_keydown(event.key)

        game.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
