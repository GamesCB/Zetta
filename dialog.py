import pygame
pygame.init()
from pygame.locals import *

from engine import *

class Dialogs():

    black_surface = pygame.Surface((1280, 144))
    white_surface = pygame.Surface((4, 144))

    def __init__(self, text, size = 32):
        self.word = text

        self.text = pygame.font.Font('fonts/Hardpixel-nn51.otf', size)
        self.font_name = pygame.font.Font('fonts/Hardpixel-nn51.otf', 16)
        self.var_render = 5
        self.text_word = ''
        self.iter = 0
        self.list_word = list(self.word)

        self.blit_click = False
        self.exit_dialog = False



        # self.play_var = 16

    def render_text(self, x = 180, color = (255, 255, 255), print = True, y = 600, sound = True, texture=None, name='None', monolog=False):
        # window.blit(self.black_surface, (0, 720 - 144))

        # self.black_surface.fill((0, 0, 0))
        # self.white_surface.fill((180, 180, 180))
        if not monolog:
            window.blit(self.font_name.render(f'{name}', True, (20, 20, 20)), (32 + 16, 720 - 144 - 24 + 10))

        if self.var_render == 0:
            self.var_render = 4
            self.text_word += self.list_word[self.iter]
            self.iter += 1
            # self.play_var += 1

            if self.iter >= len(self.list_word):
                self.blit_click = True
                # if sound:
                #     self.sound_dialog.stop()

                self.var_render = 10000000000000



        window.blit(self.text.render(self.text_word, True, color), (x, y))
        self.var_render -= 1

    def render_nowait(self, x = 180, color = (194, 147, 54), print = True, y = 600, sound = True, texture = None):
        if not self.exit_dialog:
            if self.var_render == 0:

                self.var_render = 4
                self.text_word += self.list_word[self.iter]
                self.iter += 1
                # self.play_var += 1

                if self.iter >= len(self.list_word):
                    self.blit_click = True
                    # if sound:
                    #     self.sound_dialog.stop()

                    self.var_render = 10000000000000



            window.blit(self.text.render(self.text_word, True, color), (x, y))
            if self.blit_click and print:
                if self.var_render in range(10000, 10000000000000 - 100):
                    self.exit_dialog = True
                    return True

            self.var_render -= 1
        return False

    def __str__(self):
        return self.word

class Dialog(Dialogs):

    dialog_window = pygame.image.load('sprites/icons/dialog bar.png').convert_alpha()
    dialog_port = pygame.image.load('sprites/icons/dialog port.png').convert_alpha()

    def __init__(self, text, size = 32):
        super(Dialog, self).__init__(text, size)


    def render(self, x = 220, color = (102, 57, 49), print = True, y = 580, sound = True, texture = None, name='None'):
        window.blit(self.dialog_port, (32, 720 - 144 - 24))
        window.blit(self.dialog_window, (32 + self.dialog_port.get_width() + 8, 720 - 144 - 24))
        self.render_text(x, color, print, y, sound, texture, name)



class Monolog(Dialogs):

    monolog_window = pygame.image.load('sprites/icons/monolog bar.png').convert_alpha()

    def __init__(self, text, size=32):
        super(Monolog, self).__init__(text, size)



    def render(self, color=(102, 57, 49), print=True, y=600, sound=True):
        window.blit(self.monolog_window, (32, 720 - 144 - 24))

        self.render_text(100, color, print, y, sound, monolog=True)