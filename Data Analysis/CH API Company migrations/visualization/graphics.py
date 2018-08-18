import pygame
from pygame.locals import *

class Graphics:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height

        pygame.init()

        self.bg = pygame.Surface((self.width, self.height))
        #self.bg.fill(pygame.Color('#0b3954'))
        self.bg.fill((255, 255, 255))
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.blit(self.bg, (0, 0))

        self.temp_surf = pygame.Surface((self.width, self.height))
        #self.surf.set_colorkey((0, 0, 0))
        #self.flip()


    def clear(self):
        self.surf = pygame.Surface((self.width, self.height))

    def flip(self):
        #self.screen.blit(self.surf, (0, 0))
        pygame.display.flip()

    def draw_point(self, x, y, r):
        pygame.draw.circle(self.surf, (0, 0, 0), (x, y), r)

    def draw_line(self, x, y, x_, y_, c, alpha):
        temp = pygame.Surface((self.width, self.height))
        temp.blit(self.bg, (0, 0))
        pygame.draw.aaline(temp, pygame.Color(c), (x, y), (x_, y_))
        temp.set_colorkey((255, 255, 255))
        temp.set_alpha(alpha)
        self.surf.blit(temp, (0, 0))
        #self.surf.set_alpha(255)


    def save_to_file(self, file):
        pygame.image.save(self.surf, file)

    def should_quit(self):
        for e in pygame.event.get():
            return e.type == QUIT
    def quit(self):
        pygame.quit()
