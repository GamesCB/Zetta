import pygame
pygame.init()
from pygame.locals import *

from textures import *
from engine import *

class Light():
    light_mid = pygame.transform.scale(
        pygame.image.load('sprites/lights/light_mid.png').convert_alpha(), (256, 256)
    )

    def render_mid_mini(self, x, y, time_type=(int(timegame[0:2]) * 60 + int(timegame[3::]))):
        if time_type in range(1200, 1441) or time_type in range(0, 300):
            window.blit(self.light_mid, (x - 16 - 80 - scroll[0], y - 80 - 16 - scroll[1]))
            window.blit(self.light_mid, (x - 16 - 80 + 64 - scroll[0], y - 80 - 16 - scroll[1]))
        window.blit(double_flashlights, (x - scroll[0], y - scroll[1]))



