import pygame
pygame.init()
from pygame.locals import *
import json
import datetime
from textures import *
from engine import *
from Shaders import *
from Time import *
from player import Player

class StreetMap():

    tiles = {
        '1': pygame.image.load('sprites/street/tiles/grass/1.png').convert_alpha(),
        '2': pygame.image.load('sprites/street/tiles/grass/2.png').convert_alpha(),
        '3': pygame.image.load('sprites/street/tiles/grass/3.png').convert_alpha(),
        '4': pygame.image.load('sprites/street/tiles/grass/4.png').convert_alpha(),
        't': pygame.image.load('sprites/street/tiles/railway/t.png').convert_alpha(),
        'd': pygame.image.load('sprites/street/tiles/railway/d.png').convert_alpha(),
        'm': pygame.image.load('sprites/street/tiles/street/m.png').convert_alpha(),
        'u': pygame.image.load('sprites/street/tiles/railway_station/u.png').convert_alpha(),
        'i': pygame.image.load('sprites/street/tiles/railway_station/i.png').convert_alpha(),
        'o': pygame.image.load('sprites/street/tiles/railway_station/o.png').convert_alpha(),
        'h': pygame.image.load('sprites/street/tiles/railway_station/h.png').convert_alpha(),
        'j': pygame.image.load('sprites/street/tiles/railway_station/j.png').convert_alpha(),
        'k': pygame.image.load('sprites/street/tiles/railway_station/k.png').convert_alpha(),
        'b': pygame.image.load('sprites/street/tiles/railway_station/b.png').convert_alpha(),
        'p': pygame.image.load('sprites/street/tiles/railway_station/p.png').convert_alpha(),
        'l': pygame.image.load('sprites/street/tiles/railway_station/l.png').convert_alpha(),
        'r': pygame.image.load('sprites/street/tiles/railway_station/r.png').convert_alpha(),
        'n': pygame.image.load('sprites/street/tiles/railway_station/n.png').convert_alpha(),
        'w': pygame.image.load('sprites/street/tiles/street/w.png').convert_alpha(),
        '5': pygame.image.load('sprites/street/tiles/street/5.png').convert_alpha(),
        '6': pygame.image.load('sprites/street/tiles/street/6.png').convert_alpha(),
        '7': pygame.image.load('sprites/street/tiles/street/7.png').convert_alpha(),
        '8': pygame.image.load('sprites/street/tiles/street/8.png').convert_alpha(),
        '9': pygame.image.load('sprites/street/tiles/street/9.png').convert_alpha(),
        'z': pygame.image.load('sprites/street/tiles/street/z.png').convert_alpha(),
        's' : pygame.image.load('sprites/street/tiles/street/s.png').convert_alpha(),
        'a' : pygame.image.load('sprites/street/tiles/street/a.png').convert_alpha(),
        '+' : pygame.image.load('sprites/street/tiles/street/+.png').convert_alpha(),
        '-' : pygame.image.load('sprites/street/tiles/street/-.png').convert_alpha(),
        ')' : pygame.image.load('sprites/street/tiles/street/).png').convert_alpha(),
        'й' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/+.png').convert_alpha(), 270
        ).convert_alpha(),
        'ц' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/m.png').convert_alpha(), 90
        ).convert_alpha(),
        'у' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/+.png').convert_alpha(), 90
        ).convert_alpha(),
        'к' : pygame.image.load('sprites/street/tiles/street/к.png').convert_alpha(),
        'е' : pygame.image.load('sprites/street/tiles/street/е.png').convert_alpha(),
        'н' : pygame.image.load('sprites/street/tiles/street/н.png').convert_alpha(),
        'ф' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/8.png'), 270
        ).convert_alpha(),
        ';' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/к.png'), 90
        ).convert_alpha(),
        ']': pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/н.png'), 90
        ).convert_alpha(),
        'я': pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/е.png'), 90
        ).convert_alpha(),
        'з' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/z.png'), 180
        ).convert_alpha(),
        'ч' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/z.png'), 270
        ),
        'г' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/н.png'), 180
        ).convert_alpha(),
        'ж' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/н.png'), 270
        ),
        'э' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/к.png'), 270
        ).convert_alpha(),
        'т' : pygame.transform.rotate(
            pygame.image.load('sprites/street/tiles/street/е.png'), 270
        ).convert_alpha(),
        'ё' : pygame.image.load('sprites/street/tiles/street/ё.png').convert_alpha()

    }

    '''
        обустроить дальнейшую часть города
        сделать надпись отелю HOTEL
        сделать тайлсет для переулков
    '''



    meeting_house_station = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/meeting_house_station.png').convert_alpha(), (464 * 1.5, 364 * 1.5)
    ).convert_alpha()

    hotel2 = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/hotel2.png').convert_alpha(), (280 * 2.5, 308 * 2.5)
    ).convert_alpha()

    hotel1 = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/hotel1.png').convert_alpha(), (280 * 2.5, 308 * 2.5)
    ).convert_alpha()

    bar_excluse = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/bar-excluse.png').convert_alpha(), (280 * 2.5, 354 * 2.5)
    ).convert_alpha()

    cafe_hoo = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/cafe_hoo.png').convert_alpha(), (235 * 2.5, 577 * 2.5)
    ).convert_alpha()

    hoo_stand = pygame.transform.scale(
        pygame.image.load('sprites/street/urbs/hoo_stand.png').convert_alpha(), (15 * 2.5, 21 * 2.5)
    ).convert_alpha()

    quarters = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/quarters.png').convert_alpha(), (240 * 2.5, 327 * 2.5)
    ).convert_alpha()

    fence = pygame.image.load('sprites/street/urbs/fence-horisontal.png').convert_alpha()

    fence_one = pygame.image.load('sprites/street/urbs/fence_one.png').convert_alpha()

    hotdoghouse = pygame.transform.scale(
        pygame.image.load('sprites/street/houses/hotdoghouse.png').convert_alpha(), (160 * 3, 121 * 3)
    ).convert_alpha()

    hotdogstand = pygame.transform.scale(
        pygame.image.load('sprites/street/urbs/hotdogstand.png').convert_alpha(), (15 * 2.5, 22 * 2.5)
    ).convert_alpha()

    grid = pygame.transform.scale(
        pygame.image.load('sprites/street/urbs/grid.png').convert_alpha(), (66 * 3, 37 * 3)
    ).convert_alpha()

    container = pygame.transform.scale(
        pygame.image.load('sprites/street/urbs/containter.png').convert_alpha(), (133 * 1.5, 256 * 1.5)
    ).convert_alpha()

    def __init__(self, save):
        with open(f'data/{save}/data.json', 'r', encoding='utf-8') as jsonfile:
            self.data = json.load(jsonfile)
        self.tiles_map = load_tiles('static/tiles_station')



        self.tree = Trees(self.data['season'])

        self.light_flashlight = Light()
        print(save, 'savedfsdafdsg')
        self.filters = TimeGame(save)

    def render_filter(self):
        self.filters.render()

    def render_tiles_station(self):

        y = 11
        for row in self.tiles_map:
            x = 0
            for tile in row:

                window.blit(self.tiles[tile], (x * 64 - scroll[0], y * 64 - scroll[1]))

                x += 1

            y += 1

    def render_tiles_zetta(self):

        y = 11
        for row in self.tiles_map:
            x = 0
            for tile in row:
                window.blit(self.tiles[tile], (x * 64 - scroll[0], y * 64 - scroll[1]))

                x += 1

            y += 1


    def render_trees_station(self):
        self.tree.render_trees()
        window.blit(watercastle, (3050 - scroll[0], 2400 - scroll[1]))

    def set_time_game(self, timeg):
        self.timegame = timeg

    def render_station_under(self, pl_y):
        '''
            попробовать воплотить идею в отрисовке столкновений Rectов
            (если квадрат объекта сталкивается с квадратом экрана, можно отрисовать)
        '''

        # if pl_y >= 3843:
        #     self.light_flashlight.render_mid_mini(4290, 3770, self.timegame)

        if pl_y >= 3520:
            self.light_flashlight.render_mid_mini(3650, 3440, self.timegame)
            # self.light_flashlight.render_mid_mini(4290, 3440, self.timegame)

        # if pl_y >= 3190:
        #     self.light_flashlight.render_mid_mini(4290, 3110, self.timegame)
        if pl_y >= 2860:
            self.light_flashlight.render_mid_mini(3650, 2780, self.timegame)
            # self.light_flashlight.render_mid_mini(4290, 2780, self.timegame)

        if pl_y >= 3909:
            window.blit(self.meeting_house_station, (3708 - scroll[0], 3625 - scroll[1]))

        if pl_y >= 4180 - 45:
            self.light_flashlight.render_mid_mini(3650, 4100 - 45, self.timegame)
            # self.light_flashlight.render_mid_mini(4290, 4100, self.timegame)

        window.blit(bench_right_rotated, (4300 - scroll[0], 4250 - scroll[1]))

    def render_station_above(self, pl_y):


        # if pl_y < 3843:
        #     self.light_flashlight.render_mid_mini(4290, 3770, self.timegame)

        if pl_y < 3520:
            self.light_flashlight.render_mid_mini(3650, 3440, self.timegame)
            # self.light_flashlight.render_mid_mini(4290, 3440, self.timegame)

        # if pl_y < 3190:
        #     self.light_flashlight.render_mid_mini(4290, 3110, self.timegame)

        if pl_y < 2860:
            self.light_flashlight.render_mid_mini(3650, 2780, self.timegame)
            # self.light_flashlight.render_mid_mini(4290, 2780, self.timegame)

        if pl_y < 3909:
            window.blit(self.meeting_house_station, (3708 - scroll[0], 3625 - scroll[1]))

        if pl_y < 4180 - 45:
            self.light_flashlight.render_mid_mini(3650, 4100 - 45, self.timegame)
            # self.light_flashlight.render_mid_mini(4290, 4100, self.timegame)

    def render_station_above_above(self):
        window.blit(self.meeting_house_station, (3720 - scroll[0], 3625 - scroll[1]))

    def render_powers_station_under(self):
        window.blit(powers_railway_top, (100 - scroll[0], 4100 - scroll[1]))

    def render_powers_station_above(self):
        window.blit(powers_railway_down, (100 - scroll[0], 4150 - scroll[1]))

    def check_position(self, x_obj:int, y_obj:int, img:pygame.image):
        if Rect(0, 0, 1280, 720).colliderect(Rect(x_obj - scroll[0], y_obj - scroll[1], img.get_width(), img.get_height())):
            return True
        return False

    def prechecked_zetta(self):
        self.hoo_stand_result = self.check_position(1298 + 32, 2749 + 28, self.hoo_stand)

    def render_zetta_location(self, player:Player):
        self.render_tiles_zetta()
        self.render_zetta_under(player.player_rect.y)
        player.render()
        self.render_zetta_above(player.player_rect.y)

    def render_zetta_under(self, pl_y:int):

        if pl_y > 2000:
            window.blit(self.hotdogstand, (1330 - scroll[0], 2047 - scroll[1]))

        if pl_y > 2016:
            window.blit(self.grid, (1810 - scroll[0], 1992 - scroll[1]))

        if pl_y > 2016 and self.check_position(1390, 1950, self.hotdoghouse):
            window.blit(self.hotdoghouse, (1376 - scroll[0], 1750 - scroll[1]))

        if pl_y > 2030 and self.check_position(1720 + 80 + 16 + 120, 1000 + 24 + 463, self.quarters):
            window.blit(self.quarters, (1720 + 80 + 16 + 48 * 2.5 - scroll[0], 1000 + 24 + 185 * 2.5 - scroll[1]))

        if pl_y > 2489:
            window.blit(self.fence, (2312 - scroll[0], 2500 - scroll[1]))
            window.blit(self.fence, (2312 + self.fence.get_width() - 17 - scroll[0], 2500 - scroll[1]))
            window.blit(self.fence, (2312 + self.fence.get_width() * 2 - 17 * 2 - scroll[0], 2500 - scroll[1]))
            window.blit(self.fence, (2312 + self.fence.get_width() * 4 - 17 * 4 - scroll[0], 2500 - scroll[1]))

        if pl_y > 2489:
            window.blit(self.fence_one, (2312 - scroll[0], 2550 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 2 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 3 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 4 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 5 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 6 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 7 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 8 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 9 - scroll[1]))


        if self.check_position(1968, 2240 + 50 * 18, self.fence_one) or\
                self.check_position(1968, 2240 + 50 * 10, self.fence_one) or\
            self.check_position(1968, 2240, self.fence_one):
            window.blit(self.fence_one, (1968 - scroll[0], 2240 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 2 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 3 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 4 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 5 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 6 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 7 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 8 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 9 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 10 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 11 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 12 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 13 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 14 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 15 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 16 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 17 - scroll[1]))
            window.blit(self.fence_one, (1968 - scroll[0], 2240 + 50 * 18 - scroll[1]))

        if pl_y > 2740 and self.check_position(1298 + 32, 2749 + 28, self.hoo_stand):
            window.blit(self.hoo_stand, (1298 + 32 - scroll[0], 2749 + 28 - scroll[1]))

        if pl_y > 3412 and self.check_position(1288, 2100, self.cafe_hoo):
            window.blit(self.cafe_hoo, (1288 - scroll[0], 2100 - scroll[1]))

        if pl_y > 3609 and self.check_position(1406 - 20, 3135, self.hotel2):
            window.blit(self.hotel2, (1406 - 20 - scroll[0], 3135 - scroll[1]))

        if pl_y > 3525 and self.check_position(2250, 3020, self.bar_excluse):
            window.blit(self.bar_excluse, (2250 - scroll[0], 3020 - scroll[1]))

    def render_zetta_above(self, pl_y:int):

        window.blit(self.container, (2727 - 5 * 1.5 - scroll[0], 2801 - 256 * 3 - scroll[1]))
        window.blit(self.container, (2727 - 5 * 1.5 - scroll[0], 2801 - 256 * 2 - scroll[1]))
        window.blit(self.container, (2727 - 5 * 1.5 - scroll[0], 2801 - 256 * 1 - scroll[1]))
        window.blit(self.container, (2727 - 5 * 1.5 - scroll[0], 2801 - scroll[1]))

        if pl_y <= 2000:
            window.blit(self.hotdogstand, (1330 - scroll[0], 2047 - scroll[1]))

        if pl_y <= 2016:
            window.blit(self.grid, (1810 - scroll[0], 1992 - scroll[1]))

        if pl_y <= 2016 and self.check_position(1390, 1950, self.hotdoghouse):
            window.blit(self.hotdoghouse, (1376 - scroll[0], 1750 - scroll[1]))

        if pl_y <= 2030 and self.check_position(1720 + 80 + 16 + 120, 1000 + 24 + 463, self.quarters):
            window.blit(self.quarters, (1720 + 80 + 16 + 48 * 2.5 - scroll[0], 1000 + 24 + 185 * 2.5 - scroll[1]))

        if pl_y <= 2489:
            window.blit(self.fence, (2312 - scroll[0], 2500 - scroll[1]))
            window.blit(self.fence, (2312 + self.fence.get_width() - 17 - scroll[0], 2500 - scroll[1]))
            window.blit(self.fence, (2312 + self.fence.get_width() * 2 - 17 * 2 - scroll[0], 2500 - scroll[1]))
            window.blit(self.fence, (2312 + self.fence.get_width() * 4 - 17 * 4 - scroll[0], 2500 - scroll[1]))

        if pl_y <= 2489:
            window.blit(self.fence_one, (2312 - scroll[0], 2550 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 2 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 3 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 4 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 5 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 6 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 7 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 8 - scroll[1]))
            window.blit(self.fence_one, (2312 - scroll[0], 2550 + 50 * 9 - scroll[1]))



        if pl_y <= 2740 and self.check_position(1298 + 32, 2749 + 28, self.hoo_stand):
            window.blit(self.hoo_stand, (1330 - scroll[0], 2749 + 28 - scroll[1]))

        if pl_y <= 3412 and self.check_position(1288, 2100, self.cafe_hoo):
            window.blit(self.cafe_hoo, (1288 - scroll[0], 2100 - scroll[1]))

        if pl_y <= 3609 and self.check_position(1406 - 20, 3135, self.hotel2):
            window.blit(self.hotel2, (1406 - 20 - scroll[0], 3135 - scroll[1]))

        if pl_y <= 3525 and self.check_position(2250, 3020, self.bar_excluse):
            window.blit(self.bar_excluse, (2250 - scroll[0], 3020 - scroll[1]))

class Trees():
    def __init__(self, season):
        if season == 'summer':
            self.tree1 = pygame.image.load('sprites/street/trees/summer/1.png').convert_alpha()
            self.tree2 = pygame.image.load('sprites/street/trees/summer/2.png').convert_alpha()
            self.tree3 = pygame.image.load('sprites/street/trees/summer/3.png').convert_alpha()

        self.trees_collect = {
            '1' : self.tree1,
            '2' : self.tree2,
            '3' : self.tree3
        }

        with open('static/trees station.txt', 'r') as file:
            self.total = list(file.read().split('\n'))

        self.trees = []
        self.cords = []
        for trees in self.total:
            if trees.isdigit():
                self.trees.append(trees)
            else:
                self.cords.append(tuple(map(int, trees.split())))



    def render_trees(self):
        for i in range(len(self.trees)):
            window.blit(self.trees_collect[self.trees[i]],
                        (self.cords[i][0] - scroll[0], self.cords[i][1] - scroll[1]))

