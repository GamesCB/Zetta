import pygame
pygame.init()
from pygame.locals import *

from engine import *

class Train():

    train_text = pygame.transform.scale(
        pygame.image.load('sprites/vehicle/train_day-long.png').convert_alpha(), (4016, 296)
    ).convert_alpha()

    def __init__(self):
        self.rect_train = Rect(0, 4230, self.train_text.get_width(), self.train_text.get_height())
        self.next = False

    def move(self):
        window.blit(self.train_text, (self.rect_train.x - scroll[0], self.rect_train.y - scroll[1]))
        if self.rect_train.x < 2764:
            self.rect_train.x += 12
            if self.rect_train.x > 2000:
                self.rect_train.x -= 4
            if self.rect_train.x > 2300:
                self.rect_train.x -= 2
            if self.rect_train.x > 2500:
                self.rect_train.x -= 2
            if self.rect_train.x % 576 == 0:
                self.screen_shake()

            return False
        else:
            if not self.next:
                self.rect_train.x = 2764


        return True

    def move_next(self):
        self.next = True
        self.rect_train.x += 8
        if self.rect_train.x > 2864:
            self.rect_train.x += 2
        if self.rect_train.x > 3000:
            self.rect_train.x += 4

    def screen_shake(self):
        global scroll
        scroll[1] -= 10