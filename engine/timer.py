import pygame

class ChessTimer:
    def __init__(self, time_in_seconds):
        self.time_left = time_in_seconds * 1000  # milliseconds
        self.last_tick = pygame.time.get_ticks()
        self.active = False
        
    def start(self):
        self.active = True
        self.last_tick = pygame.time.get_ticks()
        
    def stop(self):
        self.active = False
        self.update()
        
    def update(self):
        if self.active:
            current_tick = pygame.time.get_ticks()
            delta = current_tick - self.last_tick
            self.time_left -= delta
            self.last_tick = current_tick
            if self.time_left < 0:
                self.time_left = 0
                
    def get_time_string(self):
        seconds = max(0, self.time_left) // 1000
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def is_flagged(self):
        return self.time_left <= 0
