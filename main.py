import sys
import pygame
from constants import WIDTH, HEIGHT, FPS
from engine.game import Game
from network import Network

def draw_text_centered(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (WIDTH // 2, y)
    surface.blit(textobj, textrect)
    return textrect

def main_menu(screen, clock):
    pygame.font.init()
    font = pygame.font.SysFont("Consolas", 60, bold=True)
    small_font = pygame.font.SysFont("Consolas", 30)
    
    while True:
        screen.fill((48, 46, 43)) # PANEL_COLOR
        draw_text_centered("CHESS", font, (255, 255, 255), screen, HEIGHT // 4)
        
        btn_local = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 50)
        btn_ai = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 10, 300, 50)
        btn_online = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 80, 300, 50)
        
        # Hover effects
        pos = pygame.mouse.get_pos()
        c_local = (100, 100, 100) if btn_local.collidepoint(pos) else (70, 70, 70)
        c_ai = (100, 100, 100) if btn_ai.collidepoint(pos) else (70, 70, 70)
        c_online = (100, 100, 100) if btn_online.collidepoint(pos) else (70, 70, 70)
        
        pygame.draw.rect(screen, c_local, btn_local, border_radius=5)
        pygame.draw.rect(screen, c_ai, btn_ai, border_radius=5)
        pygame.draw.rect(screen, c_online, btn_online, border_radius=5)
        
        draw_text_centered("Play Local", small_font, (255,255,255), screen, HEIGHT//2 - 35)
        draw_text_centered("Play vs AI", small_font, (255,255,255), screen, HEIGHT//2 + 35)
        draw_text_centered("Play Online", small_font, (255,255,255), screen, HEIGHT//2 + 105)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_local.collidepoint(pos):
                        return False, False # online=False, ai=False
                    elif btn_ai.collidepoint(pos):
                        return False, True  # online=False, ai=True
                    elif btn_online.collidepoint(pos):
                        return True, False  # online=True, ai=False
                        
        pygame.display.update()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess - Main Menu")
    clock = pygame.time.Clock()

    online, ai_mode = main_menu(screen, clock)
    
    network = None
    player_color = "w"

    if online:
        pygame.display.set_caption("Chess - Connecting to Server...")
        network = Network()
        if getattr(network, 'color', None):
            player_color = network.color
            print(f"Connected to server as {player_color}")
        else:
            print("Failed to connect to server. Falling back to local.")
            online = False

    game = Game(screen, online_mode=online, player_color=player_color, network=network, ai_mode=ai_mode)
    pygame.display.set_caption(f"Chess - {'Online (' + player_color + ')' if online else ('vs AI' if ai_mode else 'Local (Pass & Play)')}")

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
