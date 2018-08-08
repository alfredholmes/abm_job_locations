import pygame
from pygame.locals import QUIT, BLEND_ADD

class Graphics:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill((0, 0, 0))

        self.surf = pygame.Surface((self.width, self.height))
        self.screen.blit(self.bg, (0, 0))

        self.temp_surf = pygame.Surface((self.width, self.height))

    def clear(self):
        self.surf = pygame.Surface((self.width, self.height))

    def flip(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.surf, (0, 0))
        pygame.display.flip()

    def draw_point(self, x, y, r):
        pygame.draw.circle(self.surf, (255, 255, 255), (x, y), r)

    def draw_line(self, x, y, x_, y_):
        pygame.draw.aaline(self.temp_surf, (255, 255, 255), (x, y), (x_, y_))

    def draw_temp_surf_with_alpha(self, alpha):
        self.temp_surf.set_alpha(alpha)
        self.surf.blit(self.temp_surf, (0, 0), special_flags=BLEND_ADD)
        self.temp_surf = pygame.Surface((self.width, self.height))

    def should_quit(self):
        for e in pygame.event.get():
            return e.type == QUIT
    def quit(self):
        pygame.quit()
