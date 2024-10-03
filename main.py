import pygame
pygame.init()
from pygame.locals import *
from UI import *
from steps import *



render_start_window()

class Main():
    def __init__(self):
        global saved

        self.menu = Menu(saved)
        if self.menu.scroll_saves >= len(self.menu.total_saves): self.menu.scroll_saves -= 1


        self.gameplay = Gameplay(self.menu.total_saves[self.menu.scroll_saves])

        if not self.gameplay.maindata['tutorial']:
            self.tutorial = Tutorial(self.menu.total_saves[self.menu.scroll_saves])

        # self.gameplay = Gameplay('save2')
        #
        # if not self.gameplay.maindata['tutorial']:
        #     self.tutorial = Tutorial('save2')




        if self.tutorial.exit_menu:
            saved = self.tutorial.saved
            self.__init__()
        self.gameplay.render_world()




if __name__ == '__main__':
    game = Main()
