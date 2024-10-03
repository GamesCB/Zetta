import json
import sys

import pygame
pygame.init()

from pygame.locals import *
from random import randint



SIZE = [1280, 720]
with open('data/maindata.json', encoding='utf-8') as file:
    if json.load(file)['FullScreen']:
        window = pygame.display.set_mode(SIZE, pygame.FULLSCREEN|DOUBLEBUF|SCALED)
    else:
        window = pygame.display.set_mode(SIZE, pygame.DOUBLEBUF|SCALED)


screen = pygame.Surface(SIZE)
scroll = [0,0]
true_scroll = scroll

main_ico = pygame.image.load('sprites/icons/main.png').convert_alpha()
pygame.display.set_icon(main_ico)
pygame.display.set_caption('Zetta')

clock = pygame.time.Clock()
FPS = 60

CAMERA_SPEED_DIVISION = 4

timegame = '00:00'



class Animation():
    def __init__(self, list_sprites:list, delay:int):
        self.list_sprites = list_sprites
        self.anim_count = 0
        self.delay = delay
        for i in self.list_sprites:
            i.convert_alpha()

    def show_anim(self, x, y):
        if self.anim_count < (len(self.list_sprites) * self.delay - 1):
            window.blit(self.list_sprites[self.anim_count//self.delay], (x - scroll[0], y - scroll[1]))
            self.anim_count += 1
        else:
            window.blit(self.list_sprites[self.anim_count // self.delay], (x - scroll[0], y - scroll[1]))
            self.anim_count = 0
            return True

        return False

    def show_anim_static(self, x, y):
        if self.anim_count < (len(self.list_sprites) * self.delay - 1):
            window.blit(self.list_sprites[self.anim_count//self.delay], (x, y))
            self.anim_count += 1
        else:
            window.blit(self.list_sprites[self.anim_count // self.delay], (x, y))
            self.anim_count = 0
            return True

        return False

def load_tiles(path):
    with open(path + '.txt', 'r', encoding='utf-8') as file:
        game_map = [i.split(',') for i in file.readlines()]

    for i in game_map:
        if '\n' in i: i.remove('\n')
        elif '' in i: i.remove('')

    return game_map

def create_sound(path, typeof = 's'):
    with open('data/maindata.json', 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    sound = pygame.mixer.Sound(path)
    if typeof == 's':
        sound.set_volume(data['volume_sound'])
    else:
        sound.set_volume(data['volume_music'])
    return sound





pygame.mouse.set_visible(False)

save_animation = Animation([pygame.transform.scale(
    pygame.image.load(f'sprites/icons/save anim/{i}.png'), (64, 64)) for i in range(1, 10)], 2
)
saved = False

def blit_multilines(size:tuple, text:str, pos:tuple, font:pygame.font.Font, color=pygame.Color('black'), surface=window):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = size
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def loading():
    from textures import mouse_cursor
    delay = randint(150, 200)
    while delay > 0:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        delay -= 1
        window.blit(screen, (0,0))

        screen.fill((0,0,0))

        window.blit(mouse_cursor, (mouse[0], mouse[1]))

        pygame.display.update()
        clock.tick(FPS)


